"""
Orchestrates one "simulate" job: builds demand -> runs the requested
policy/policies -> aggregates metrics -> (optionally) produces a
PPO-vs-Fixed-Cycle verdict table, using the exact metric definitions and
tie-thresholds from BanTRel.py Cell 17.
"""

import shutil
import tempfile
from typing import Literal

import numpy as np

from . import demand
from .baseline import FixedCyclePolicy
from .env import BangaloreSumoEnv
from .model import PPOPolicy

ALL_METRICS_DEF = [
    # (key, label, higher_is_better, unit)
    ("system_total_stopped",      "Total Stopped Vehicles", False, "vehicles"),
    ("system_total_waiting_time", "Total Waiting Time",     False, "seconds"),
    ("system_mean_waiting_time",  "Mean Waiting Time",      False, "s / vehicle"),
    ("system_mean_speed",         "Mean Speed",             True,  "m/s"),
    ("avg_waiting_time",          "Avg Waiting Time",       False, "s / vehicle"),
    ("avg_travel_time",           "Avg Travel Time",        False, "seconds"),
    ("queue_length",              "Queue Length",           False, "vehicles"),
    ("throughput",                "Throughput",             True,  "veh / step"),
    ("delay",                     "Delay vs Free-Flow",     False, "seconds"),
]

TIE_THRESHOLD = {
    "system_total_stopped": 0.05, "system_total_waiting_time": 1.0,
    "system_mean_waiting_time": 0.5, "system_mean_speed": 0.005,
    "avg_waiting_time": 0.5, "avg_travel_time": 1.0,
    "queue_length": 0.05, "throughput": 0.01, "delay": 0.5,
}


def _run_policy_episodes(policy, cfg_path: str, sumo_config_dir: str, n_runs: int) -> dict:
    """Ported from Cell 13's run_evaluation()."""
    buffers = {k: [] for k, *_ in ALL_METRICS_DEF}

    for _run in range(n_runs):
        env = BangaloreSumoEnv(cfg_path, sumo_config_dir)
        state = env.reset()
        if hasattr(policy, "reset"):
            policy.reset()
        done = False
        try:
            while not done:
                action = policy.choose_action(state)
                state, _reward, done = env.step(action)
            m = env.get_metrics()
            for k, *_ in ALL_METRICS_DEF:
                if k in m and len(m[k]):
                    buffers[k].append(m[k])
        finally:
            env.close()

    averaged = {}
    for k, runs in buffers.items():
        if not runs:
            continue
        min_len = min(len(r) for r in runs)
        averaged[k] = np.mean([r[:min_len] for r in runs], axis=0)
    return averaged


def _summarize(metrics: dict) -> dict:
    """Scalar table: mean of each per-step array (what Cell 17 prints)."""
    out = {}
    for key, label, higher_better, unit in ALL_METRICS_DEF:
        arr = metrics.get(key)
        if arr is None or not len(arr):
            continue
        out[key] = {
            "label": label, "unit": unit, "higher_is_better": higher_better,
            "value": round(float(np.mean(arr)), 3),
        }
    return out


def _verdict(ppo_summary: dict, fc_summary: dict) -> dict:
    wins_ppo = wins_fixed = ties = 0
    rows = []
    for key, label, higher_better, unit in ALL_METRICS_DEF:
        if key not in ppo_summary or key not in fc_summary:
            continue
        pm, fcm = ppo_summary[key]["value"], fc_summary[key]["value"]
        delta = pm - fcm
        threshold = TIE_THRESHOLD.get(key, 0.01)
        if abs(delta) < threshold:
            outcome = "tie"; ties += 1
        elif (delta > 0) if higher_better else (delta < 0):
            outcome = "ppo"; wins_ppo += 1
        else:
            outcome = "fixed_cycle"; wins_fixed += 1
        rows.append({"key": key, "label": label, "unit": unit,
                      "ppo": pm, "fixed_cycle": fcm, "delta": round(delta, 3),
                      "outcome": outcome})
    overall = ("ppo" if wins_ppo > wins_fixed
               else "fixed_cycle" if wins_fixed > wins_ppo else "draw")
    return {"rows": rows, "wins_ppo": wins_ppo, "wins_fixed_cycle": wins_fixed,
            "ties": ties, "overall": overall}


def run_simulation(
    *,
    net_path: str,
    sumo_config_dir: str,
    checkpoint_path: str,
    policy: Literal["ppo", "fixed_cycle", "both"],
    demand_mode: Literal["preset", "custom"],
    total_vehicles: int | None,
    period: str | None,
    mix: dict[str, float] | None,
    n_runs: int = 1,
    deterministic: bool = True,
    seed: int | None = None,
) -> dict:
    run_dir = tempfile.mkdtemp(prefix="bantrel_job_")
    try:
        cfg_path = demand.prepare_run_config(
            run_dir=run_dir, net_path=net_path, mode=demand_mode,
            total_vehicles=total_vehicles, period=period, mix=mix,
        )

        result = {"policy_requested": policy, "n_runs": n_runs}

        if policy in ("ppo", "both"):
            ppo_policy = PPOPolicy(checkpoint_path, deterministic=deterministic, seed=seed)
            ppo_metrics = _run_policy_episodes(ppo_policy, cfg_path, sumo_config_dir, n_runs)
            result["ppo"] = {
                "summary": _summarize(ppo_metrics),
                "timeseries": {k: v.tolist() for k, v in ppo_metrics.items()},
            }

        if policy in ("fixed_cycle", "both"):
            fc_policy = FixedCyclePolicy(cycle_steps=3)
            fc_metrics = _run_policy_episodes(fc_policy, cfg_path, sumo_config_dir, n_runs)
            result["fixed_cycle"] = {
                "summary": _summarize(fc_metrics),
                "timeseries": {k: v.tolist() for k, v in fc_metrics.items()},
            }

        if policy == "both":
            result["comparison"] = _verdict(
                result["ppo"]["summary"], result["fixed_cycle"]["summary"]
            )

        return result
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)
