"""
BanTRel — Pure FastAPI backend for Docker / local self-hosted setup.

This is the Docker-friendly version of the BanTRel backend.
No Gradio, no HuggingFace Spaces dependency — just a clean REST API
that your frontend can talk to over HTTP.

Endpoints
---------
  GET  /health                   → liveness / readiness probe
  POST /simulate                 → start a simulation job, returns { job_id }
  GET  /simulate/{job_id}        → poll job status / fetch result
  GET  /docs                     → interactive Swagger UI
  GET  /redoc                    → ReDoc documentation

CORS
----
  Set the BANTREL_CORS_ORIGINS env var to a comma-separated list of allowed
  origins, e.g. "http://localhost:3000,https://yourdomain.com".
  Defaults to "*" (allow everything) which is fine for local dev.

Running locally (without Docker)
---------------------------------
  pip install -r requirements.txt
  uvicorn app:app --reload --host 0.0.0.0 --port 7860

Running with Docker
--------------------
  docker compose up --build
"""

import os
import subprocess
import sys
import threading
import time
import traceback
import uuid
from typing import Literal, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

from download_checkpoint import ensure_checkpoint
from simulation.runner import run_simulation

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMO_CONFIG_DIR = os.path.join(BASE_DIR, "sumo_config")
NET_PATH = os.path.join(SUMO_CONFIG_DIR, "intersection.net.xml")
_env_checkpoint = os.environ.get("BANTREL_CHECKPOINT", "").strip()
CHECKPOINT_PATH = (
    _env_checkpoint
    if _env_checkpoint
    else os.path.join(BASE_DIR, "model_files", "ppo_bangalore.pt")
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_N_RUNS = 3
MAX_CUSTOM_VEHICLES = 60_000
MAX_PENDING_JOBS = 4
JOB_TTL_SECONDS = 30 * 60

# ---------------------------------------------------------------------------
# Startup: build SUMO network if missing, download checkpoint if missing.
# Failures are logged but do NOT crash the server — /health will report them.
# ---------------------------------------------------------------------------
if not os.path.exists(NET_PATH):
    try:
        os.makedirs(SUMO_CONFIG_DIR, exist_ok=True)
        print("[BanTRel] Building SUMO intersection network …")
        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "simulation", "build_network.py")],
            check=True,
        )
        print("[BanTRel] SUMO network built successfully.")
    except Exception:
        traceback.print_exc()
        print("[BanTRel] WARNING: SUMO network build failed — simulations will error.")

try:
    ensure_checkpoint(CHECKPOINT_PATH)
    print(f"[BanTRel] Checkpoint ready at: {CHECKPOINT_PATH}")
except Exception:
    traceback.print_exc()
    print("[BanTRel] WARNING: checkpoint download failed — PPO policy unavailable.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
api = FastAPI(
    title="BanTRel Simulation API",
    description=(
        "REST API for the BanTRel AI-powered traffic signal control demo. "
        "Run a SUMO simulation comparing the PPO agent against a fixed-cycle baseline."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Alias for uvicorn app:app convention
app = api

_cors_raw = os.environ.get("BANTREL_CORS_ORIGINS", "").strip() or "*"
_cors_origins = [o.strip() for o in _cors_raw.split(",") if o.strip()]
api.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (lost on container restart — fine for a local demo).
jobs: dict[str, dict] = {}
_jobs_lock = threading.Lock()
# TraCI is process-level state, so only one simulation can run at a time.
_SIM_SLOT = threading.Semaphore(1)


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------
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
        total = sum(pcts)
        if abs(total - 100) > 0.5:
            raise ValueError(f"vehicle mix percentages must sum to 100 (got {total})")
        return {
            "car":  self.car_pct  / 100,
            "bike": self.motorcycle_pct / 100,
            "auto": self.autorickshaw_pct / 100,
        }


# ---------------------------------------------------------------------------
# Job helpers
# ---------------------------------------------------------------------------
def _set_job(job_id: str, **fields) -> None:
    with _jobs_lock:
        jobs[job_id].update(fields)


def _purge_old_jobs() -> None:
    now = time.time()
    with _jobs_lock:
        stale = [
            jid for jid, job in jobs.items()
            if job["status"] in ("done", "error")
            and now - job.get("created", now) > JOB_TTL_SECONDS
        ]
        for jid in stale:
            del jobs[jid]


def _run_job(job_id: str, req: SimulateRequest) -> None:
    with _SIM_SLOT:
        _set_job(job_id, status="running")
        try:
            mix = req.resolve_mix()
            if req.mode == "custom" and (req.total_vehicles or 0) > MAX_CUSTOM_VEHICLES:
                raise ValueError(
                    f"total_vehicles capped at {MAX_CUSTOM_VEHICLES:,} for this demo"
                )
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
        except Exception as exc:
            _set_job(job_id, status="error", error=str(exc), trace=traceback.format_exc())


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@api.get("/health", summary="Liveness / readiness probe")
async def health():
    """Returns the server status and whether the network + checkpoint are ready."""
    return {
        "status": "ok",
        "network_built": os.path.exists(NET_PATH),
        "checkpoint_found": os.path.exists(CHECKPOINT_PATH),
        "server_time_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }


@api.post("/simulate", summary="Start a simulation job")
async def start_simulation(req: SimulateRequest, background_tasks: BackgroundTasks):
    """
    Enqueue a simulation job. Returns a `job_id` immediately.
    Poll `GET /simulate/{job_id}` to check status and retrieve results.
    """
    _purge_old_jobs()
    with _jobs_lock:
        pending = sum(1 for job in jobs.values() if job["status"] in ("queued", "running"))
        if pending >= MAX_PENDING_JOBS:
            raise HTTPException(
                status_code=429,
                detail="Server is busy — too many concurrent jobs. Please retry shortly.",
            )
        job_id = str(uuid.uuid4())
        jobs[job_id] = {"status": "queued", "created": time.time()}
    background_tasks.add_task(_run_job, job_id, req)
    return {"job_id": job_id}


@api.get("/simulate/{job_id}", summary="Poll simulation job status")
async def get_status(job_id: str):
    """
    Returns the current status of a simulation job.

    Status values:
    - `queued`  — waiting for the simulation slot
    - `running` — simulation is in progress
    - `done`    — result is available in the `result` field
    - `error`   — see `error` and `trace` fields
    """
    with _jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return {k: v for k, v in job.items() if k != "created"}


@api.get("/", include_in_schema=False)
async def root():
    return JSONResponse({
        "name": "BanTRel Simulation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    })


# ---------------------------------------------------------------------------
# Entry point (local dev without Docker)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:api",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860)),
        reload=True,
    )
