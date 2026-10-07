"""
FastAPI backend for the BanTRel web demo. Deployed as an HF Docker Space.

Flow: POST /simulate returns a job_id immediately; the actual SUMO run
happens in a background task (can take anywhere from a few seconds to
~1-2 min depending on n_runs and demand size). The frontend polls
GET /simulate/{job_id} until status == "done" or "error".
"""

import os
import traceback
import uuid
from typing import Literal, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

# Adaptive GPU decorator MUST be defined before importing simulation modules
# because spaces must be imported before CUDA is initialized by torch
try:
    import spaces
    gpu_decorator = spaces.GPU(duration=120)
except ImportError:
    def gpu_decorator(func):
        return func

from simulation.runner import run_simulation

BASE_DIR = os.path.dirname(__file__)
SUMO_CONFIG_DIR = os.path.join(BASE_DIR, "sumo_config")
NET_PATH = os.path.join(SUMO_CONFIG_DIR, "intersection.net.xml")
# Prefer an env var so you can swap checkpoints without a code change /
# point at a path where you've downloaded the HF model file at build time.
CHECKPOINT_PATH = os.environ.get(
    "BANTREL_CHECKPOINT", os.path.join(BASE_DIR, "model_files", "ppo_bangalore.pt")
)

import subprocess
import time

LOCK_PATH = os.path.join(SUMO_CONFIG_DIR, "build.lock")
if not os.path.exists(NET_PATH):
    try:
        os.makedirs(SUMO_CONFIG_DIR, exist_ok=True)
        # Atomic lock creation prevents multiple workers from building concurrently
        fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        print("Building SUMO network...")
        subprocess.run(["python", "simulation/build_network.py"], check=True)
    except FileExistsError:
        # Another worker is building it, wait for it to finish
        print("Waiting for SUMO network to be built by another worker...")
        while not os.path.exists(NET_PATH):
            time.sleep(0.5)

MAX_N_RUNS = 3
MAX_CUSTOM_VEHICLES = 60_000  # ~3.7x the default day, generous headroom before state clipping dominates

app = FastAPI(title="BanTRel Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("BANTREL_CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: dict[str, dict] = {}  # in-memory job store — fine for a single-container demo


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


@gpu_decorator
def run_simulation_gpu_wrapper(req_json: str) -> str:
    import json
    req_dict = json.loads(req_json)
    req = SimulateRequest(**req_dict)
    mix = req.resolve_mix()
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
    return json.dumps(result)


def _run_job(job_id: str, req: SimulateRequest) -> None:
    jobs[job_id]["status"] = "running"
    try:
        mix = req.resolve_mix()
        if req.mode == "custom" and (req.total_vehicles or 0) > MAX_CUSTOM_VEHICLES:
            raise ValueError(f"total_vehicles capped at {MAX_CUSTOM_VEHICLES} for this demo")

        if os.environ.get("SPACE_ID"):
            from gradio_client import Client
            import json
            client = Client("http://127.0.0.1:7860/")
            res_str = client.predict(req.model_dump_json(), api_name="/run_sim")
            result = json.loads(res_str)
        else:
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
        jobs[job_id] = {"status": "done", "result": result}
    except Exception as exc:  # noqa: BLE001 — surface any failure to the client
        jobs[job_id] = {"status": "error", "error": str(exc), "trace": traceback.format_exc()}


@app.post("/simulate")
async def start_simulation(req: SimulateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued"}
    background_tasks.add_task(_run_job, job_id, req)
    return {"job_id": job_id}


@app.get("/simulate/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "network_built": os.path.exists(NET_PATH),
        "checkpoint_found": os.path.exists(CHECKPOINT_PATH),
    }

import gradio as gr
demo = gr.Blocks()
with demo:
    gr.Markdown("BanTRel Backend API is running on ZeroGPU.")
    in_box = gr.Textbox(visible=False)
    out_box = gr.Textbox(visible=False)
    btn = gr.Button("Run", visible=False)
    btn.click(fn=run_simulation_gpu_wrapper, inputs=in_box, outputs=out_box, api_name="run_sim")

app = gr.mount_gradio_app(app, demo, path="/")

