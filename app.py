"""
FastAPI backend for the BanTRel web demo, served from a Hugging Face Gradio
Space running on ZeroGPU.

Flow: POST /simulate returns a job_id immediately; the actual SUMO run
happens in a background task (anywhere from a few seconds to ~1-2 min
depending on n_runs and demand size). The frontend polls
GET /simulate/{job_id} until status == "done" or "error".

ZeroGPU notes
-------------
* ZeroGPU refuses to start a Space with no @spaces.GPU function, so a tiny
  never-called function is declared below purely to satisfy that check.
* The simulation itself (SUMO + a small PPO policy) is CPU work and runs
  directly in the background task. It is deliberately NOT wrapped in
  @spaces.GPU, so it does not consume GPU quota.
* On a Gradio SDK Space the platform runs `python app.py`, so this file must
  start the server itself (see the uvicorn.run call at the bottom).
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
    """Never called. Only satisfies ZeroGPU's startup check."""
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
from pydantic import BaseModel, field_validator

from download_checkpoint import ensure_checkpoint
from simulation.runner import run_simulation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMO_CONFIG_DIR = os.path.join(BASE_DIR, "sumo_config")
NET_PATH = os.path.join(SUMO_CONFIG_DIR, "intersection.net.xml")
# Prefer an env var so you can swap checkpoints without a code change.
CHECKPOINT_PATH = os.environ.get(
    "BANTREL_CHECKPOINT", os.path.join(BASE_DIR, "model_files", "ppo_bangalore.pt")
)

MAX_N_RUNS = 3
MAX_CUSTOM_VEHICLES = 60_000  # ~3.7x the default day, generous headroom before state clipping dominates
MAX_PENDING_JOBS = 4          # queued + running; beyond this POST /simulate returns 429
JOB_TTL_SECONDS = 30 * 60     # finished jobs are discarded after this long


# --------------------------------------------------------------------------
# Startup: build the SUMO network and fetch the checkpoint if missing.
# Failures are printed but do not stop the server, so /health can report them.
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
# API
# --------------------------------------------------------------------------
api = FastAPI(title="BanTRel Simulation API")

api.add_middleware(
    CORSMiddleware,
    # Set BANTREL_CORS_ORIGINS=https://bantrel.becore.space in the Space
    # variables to lock this down; "*" is fine for a public demo.
    allow_origins=os.environ.get("BANTREL_CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: dict[str, dict] = {}  # in-memory job store; lost on restart
_jobs_lock = threading.Lock()
# SUMO/TraCI runs share process-level state, so run one simulation at a time.
_SIM_SLOT = threading.Semaphore(1)


class SimulateRequest(BaseModel):
    mode: Literal["preset", "custom"]
    policy: Literal["ppo", "fixed_cycle", "both"] = "both"
    period: Optional[Literal[
        "night", "morning_rush", "mid_morning", "afternoon", "evening_rush", "evening"
    ]] = None                      # preset-only; omit for the full 24h canonical day
    total_vehicles: Optional[int] = None       # custom-only
    car_pct: Optional[float] = None            # custom-only, 0-100
    motorcycle_pct: Optional[float] = None
    autorickshaw_pct: Optional[float] = None
    n_runs: int = 1
    deterministic: bool = True
    seed: Optional[int] = None

    @field_validator("n_runs")
    @classmethod
    def _clamp_runs(cls, v):
        if not (1 <= v <= MAX_N_RUNS):
            raise ValueError(f"n_runs must be between 1 and {MAX_N_RUNS}")
        return v

    def resolve_mix(self) -> dict[str, float] | None:
        if self.mode != "custom":
            return None
        pcts = [self.car_pct, self.motorcycle_pct, self.autorickshaw_pct]
        if any(p is None for p in pcts):
            raise ValueError("custom mode requires car_pct, motorcycle_pct, autorickshaw_pct")
        if abs(sum(pcts) - 100) > 0.5:
            raise ValueError(f"vehicle mix percentages must sum to 100 (got {sum(pcts)})")
        return {"car": self.car_pct / 100, "bike": self.motorcycle_pct / 100,
                "auto": self.autorickshaw_pct / 100}


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
        except Exception as exc:  # noqa: BLE001 - surface any failure to the client
            _set_job(job_id, status="error", error=str(exc), trace=traceback.format_exc())


@api.post("/simulate")
async def start_simulation(req: SimulateRequest, background_tasks: BackgroundTasks):
    _purge_old_jobs()
    with _jobs_lock:
        pending = sum(1 for j in jobs.values() if j["status"] in ("queued", "running"))
        if pending >= MAX_PENDING_JOBS:
            raise HTTPException(
                status_code=429, detail="Server is busy, please try again shortly"
            )
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
        return {k: v for k, v in job.items() if k != "created"}


@api.get("/health")
async def health():
    return {
        "status": "ok",
        "network_built": os.path.exists(NET_PATH),
        "checkpoint_found": os.path.exists(CHECKPOINT_PATH),
    }


# --------------------------------------------------------------------------
# Gradio shell (required for a Gradio SDK / ZeroGPU Space) + server start
# --------------------------------------------------------------------------
with gr.Blocks(title="BanTRel Backend") as demo:
    gr.Markdown("BanTRel backend API is running. See `/health` and `/docs`.")
    # Wires the keepalive function into Gradio so it is visible to ZeroGPU.
    gr.Button("keepalive", visible=False).click(_zerogpu_keepalive, api_name=False)

app = gr.mount_gradio_app(api, demo, path="/", ssr_mode=True)

# Trigger ZeroGPU startup registration since we bypass demo.launch()
try:
    from spaces.zero import startup as zero_startup
    zero_startup()
except Exception:
    pass

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7860)