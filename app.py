"""
FastAPI backend for the BanTRel web demo, served from a Hugging Face Gradio
Space running on ZeroGPU.

Flow: POST /simulate returns a job_id immediately; the actual SUMO run
happens in a background task. The frontend polls GET /simulate/{job_id}
until status == "done" or "error".

ZeroGPU notes
------------
* A never-called @spaces.GPU probe is retained for Space startup detection.
* The simulation itself (SUMO + PPO policy) deliberately runs on CPU and
  does not call the GPU probe or consume GPU allocation time.
* This module starts the mounted FastAPI + Gradio ASGI app with Uvicorn.
"""

# `spaces` must be imported before torch (which simulation/ imports below).
try:
    import spaces
except ImportError:  # local development without the `spaces` package
    class _NoSpaces:
        @staticmethod
        def GPU(*args, **kwargs):
            if args and callable(args[0]) and not kwargs:
                return args[0]

            def decorator(func):
                return func

            return decorator

    spaces = _NoSpaces()


@spaces.GPU(duration=1)
def _zerogpu_keepalive() -> None:
    """Never called. Only satisfies ZeroGPU's startup detection requirement."""
    return None


import os
import subprocess
import sys
import threading
import time
import traceback
import uuid
from typing import Literal, Optional

import gradio as gr
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

from download_checkpoint import ensure_checkpoint
from embedded_assets import ensure_assets
from simulation.runner import run_simulation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMO_CONFIG_DIR = os.path.join(BASE_DIR, "sumo_config")
NET_PATH = os.path.join(SUMO_CONFIG_DIR, "intersection.net.xml")
CHECKPOINT_PATH = os.environ.get(
    "BANTREL_CHECKPOINT", os.path.join(BASE_DIR, "model_files", "ppo_bangalore.pt")
)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FAVICON_PATH = os.path.join(ASSETS_DIR, "favicon.ico")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
ensure_assets(BASE_DIR)

MAX_N_RUNS = 3
MAX_CUSTOM_VEHICLES = 60_000
MAX_PENDING_JOBS = 4
JOB_TTL_SECONDS = 30 * 60


# --------------------------------------------------------------------------
# Startup: build SUMO network and fetch the checkpoint if missing.
# Failures are logged but do not prevent /health from reporting their status.
# --------------------------------------------------------------------------
if not os.path.exists(NET_PATH):
    try:
        os.makedirs(SUMO_CONFIG_DIR, exist_ok=True)
        print("Building SUMO network...")
        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "simulation", "build_network.py")],
            check=True,
        )
    except Exception:  # noqa: BLE001
        traceback.print_exc()

try:
    ensure_checkpoint(CHECKPOINT_PATH)
except Exception:  # noqa: BLE001
    traceback.print_exc()


# --------------------------------------------------------------------------
# FastAPI API — these endpoints remain unchanged for the React frontend.
# --------------------------------------------------------------------------
api = FastAPI(title="BanTRel Simulation API")
api.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("BANTREL_CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: dict[str, dict] = {}  # In-memory demo job store; lost on Space restart.
_jobs_lock = threading.Lock()
# SUMO/TraCI runs share process-level state, so run one simulation at a time.
_SIM_SLOT = threading.Semaphore(1)


class SimulateRequest(BaseModel):
    mode: Literal["preset", "custom"]
    policy: Literal["ppo", "fixed_cycle", "both"] = "both"
    period: Optional[Literal[
        "night", "morning_rush", "mid_morning", "afternoon", "evening_rush", "evening"
    ]] = None
    total_vehicles: Optional[int] = None
    car_pct: Optional[float] = None
    motorcycle_pct: Optional[float] = None
    autorickshaw_pct: Optional[float] = None
    n_runs: int = 1
    deterministic: bool = True
    seed: Optional[int] = None

    @field_validator("n_runs")
    @classmethod
    def _clamp_runs(cls, value):
        if not (1 <= value <= MAX_N_RUNS):
            raise ValueError(f"n_runs must be between 1 and {MAX_N_RUNS}")
        return value

    def resolve_mix(self) -> dict[str, float] | None:
        if self.mode != "custom":
            return None
        pcts = [self.car_pct, self.motorcycle_pct, self.autorickshaw_pct]
        if any(p is None for p in pcts):
            raise ValueError("custom mode requires car_pct, motorcycle_pct, autorickshaw_pct")
        if abs(sum(pcts) - 100) > 0.5:
            raise ValueError(f"vehicle mix percentages must sum to 100 (got {sum(pcts)})")
        return {
            "car": self.car_pct / 100,
            "bike": self.motorcycle_pct / 100,
            "auto": self.autorickshaw_pct / 100,
        }


def _set_job(job_id: str, **fields) -> None:
    with _jobs_lock:
        jobs[job_id].update(fields)


def _purge_old_jobs() -> None:
    now = time.time()
    with _jobs_lock:
        stale = [
            job_id for job_id, job in jobs.items()
            if job["status"] in ("done", "error")
            and now - job.get("created", now) > JOB_TTL_SECONDS
        ]
        for job_id in stale:
            del jobs[job_id]


def _run_job(job_id: str, req: SimulateRequest) -> None:
    with _SIM_SLOT:
        _set_job(job_id, status="running")
        try:
            mix = req.resolve_mix()
            if req.mode == "custom" and (req.total_vehicles or 0) > MAX_CUSTOM_VEHICLES:
                raise ValueError(f"total_vehicles capped at {MAX_CUSTOM_VEHICLES} for this demo")

            result = run_simulation(
                net_path=NET_PATH,
                sumo_config_dir=SUMO_CONFIG_DIR,
                checkpoint_path=CHECKPOINT_PATH,
                policy=req.policy,
                demand_mode=req.mode,
                total_vehicles=req.total_vehicles,
                period=req.period,
                mix=mix,
                n_runs=req.n_runs,
                deterministic=req.deterministic,
                seed=req.seed,
            )
            _set_job(job_id, status="done", result=result)
        except Exception as exc:  # noqa: BLE001
            _set_job(job_id, status="error", error=str(exc), trace=traceback.format_exc())


@api.post("/simulate")
async def start_simulation(req: SimulateRequest, background_tasks: BackgroundTasks):
    _purge_old_jobs()
    with _jobs_lock:
        pending = sum(1 for job in jobs.values() if job["status"] in ("queued", "running"))
        if pending >= MAX_PENDING_JOBS:
            raise HTTPException(status_code=429, detail="Server is busy, please try again shortly")
        job_id = str(uuid.uuid4())
        jobs[job_id] = {"status": "queued", "created": time.time()}
    background_tasks.add_task(_run_job, job_id, req)
    return {"job_id": job_id}


@api.get("/simulate/{job_id}")
async def get_status(job_id: str):
    with _jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="job not found")
        return {key: value for key, value in job.items() if key != "created"}


@api.get("/health")
async def health():
    return {
        "status": "ok",
        "network_built": os.path.exists(NET_PATH),
        "checkpoint_found": os.path.exists(CHECKPOINT_PATH),
    }


@api.get("/favicon.ico", include_in_schema=False)
@api.get("/assets/favicon.ico", include_in_schema=False)
async def favicon():
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH, media_type="image/x-icon")
    raise HTTPException(status_code=404, detail="Favicon not found")


@api.get("/assets/logo.png", include_in_schema=False)
@api.get("/logo.png", include_in_schema=False)
async def logo():
    if os.path.exists(LOGO_PATH):
        return FileResponse(LOGO_PATH, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")


def _check_engine_status():
    with _jobs_lock:
        active_jobs = len(jobs)
    return {
        "status": "online",
        "server_time_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "network_built": os.path.exists(NET_PATH),
        "checkpoint_found": os.path.exists(CHECKPOINT_PATH),
        "active_jobs_in_memory": active_jobs,
        "max_pending_jobs": MAX_PENDING_JOBS,
    }


# --------------------------------------------------------------------------
# Gradio landing page.
# STITCH_HTML already contains its own <style> block so CSS travels with the
# HTML regardless of how Gradio routes the css= parameter.
# CUSTOM_CSS provides the container-level resets and is injected via head=.
# --------------------------------------------------------------------------
from stitch_frontend import CUSTOM_CSS, HEAD_HTML, STITCH_HTML

# In Gradio 6 css= was moved from gr.Blocks to launch(). Since we use
# mount_gradio_app we inject CUSTOM_CSS through the head= parameter instead.
FULL_HEAD = HEAD_HTML + f"<style>{CUSTOM_CSS}</style>"

with gr.Blocks(
    title="BanTRel — AI-Powered Traffic Signal Control",
) as demo:
    gr.HTML(STITCH_HTML)

    # Required for the ZeroGPU startup check. It is deliberately never invoked.
    gr.Button("keepalive", visible=False).click(_zerogpu_keepalive, api_name=False)

try:
    app = gr.mount_gradio_app(
        api,
        demo,
        path="/",
        ssr_mode=False,
        footer_links=[],
        head=FULL_HEAD,
        favicon_path=FAVICON_PATH,
        allowed_paths=[ASSETS_DIR],
    )
except TypeError:
    try:
        app = gr.mount_gradio_app(
            api,
            demo,
            path="/",
            ssr_mode=False,
            footer_links=[],
            head=FULL_HEAD,
            favicon_path=FAVICON_PATH,
        )
    except TypeError:
        try:
            app = gr.mount_gradio_app(
                api,
                demo,
                path="/",
                ssr_mode=False,
                footer_links=[],
                head=FULL_HEAD,
            )
        except TypeError:
            try:
                app = gr.mount_gradio_app(
                    api, demo, path="/", ssr_mode=False, footer_links=[]
                )
            except TypeError:
                app = gr.mount_gradio_app(api, demo, path="/", ssr_mode=False)

# Trigger ZeroGPU startup registration because this app uses mount_gradio_app
# instead of demo.launch(). Keep this block unchanged unless runtime testing
# shows the installed `spaces` version requires a different hook.
try:
    from spaces.zero import startup as zero_startup
    zero_startup()
except (ImportError, AttributeError):
    pass
except Exception:
    traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
