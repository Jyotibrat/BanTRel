"""
SUMO/TraCI environment — ported near-verbatim from BanTRel.py Cell 8
(BangaloreSumoEnv). Behaviour, state vector, reward, and metric definitions
are kept identical to the source notebook so the trained model sees exactly
the observation distribution it was trained on.

Only change from the original: phase strings (NS_GREEN/EW_GREEN/etc.) are
loaded from sumo_config/phases.json (built once by build_network.py) instead
of being recomputed via sumolib on every episode.
"""

import json
import os
import socket
import subprocess
import time
import xml.etree.ElementTree as ET

import numpy as np
import traci

STEP_LENGTH = 10  # simulated seconds per simulation step

FREE_FLOW_TIME = {
    "car": 500.0 / 13.89,
    "bike": 500.0 / 11.11,
    "auto": 500.0 / 11.11,
}
DEFAULT_FREE_FLOW = 500.0 / 13.89

_PHASES_CACHE = None


def _load_phases(sumo_config_dir: str) -> dict:
    global _PHASES_CACHE
    if _PHASES_CACHE is None:
        path = os.path.join(sumo_config_dir, "phases.json")
        with open(path) as f:
            _PHASES_CACHE = json.load(f)
    return _PHASES_CACHE


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class BangaloreSumoEnv:
    """SUMO gym-style environment for the single signalised intersection."""

    YELLOW_DURATION = 1   # 1 step = 10 s
    MIN_GREEN = 8          # 8 steps = 80 s

    MAX_QUEUE = 80.0
    MAX_WAIT = 600.0
    MAX_SPEED = 13.89

    INCOMING_EDGES = ("N2C", "S2C", "E2C", "W2C")

    def __init__(self, cfg_path: str, sumo_config_dir: str) -> None:
        self.cfg_path = os.path.abspath(cfg_path)
        phases = _load_phases(sumo_config_dir)
        self.tls_id = phases["tls_id"]
        self.PHASES = {
            0: (phases["NS_GREEN"], phases["NS_YELLOW"]),
            1: (phases["EW_GREEN"], phases["EW_YELLOW"]),
        }
        self.current_step = 0
        self.current_phase = 0
        self._running = False
        self._proc = None
        self.max_steps = self._parse_max_steps()
        self._reset_metric_buffers()

    def _parse_max_steps(self) -> int:
        tree = ET.parse(self.cfg_path)
        end_tag = tree.find(".//end")
        step_tag = tree.find(".//step-length")
        end_val = int(end_tag.get("value", 86400)) if end_tag is not None else 86400
        step_val = int(step_tag.get("value", 10)) if step_tag is not None else 10
        return end_val // step_val

    def _reset_metric_buffers(self) -> None:
        self._buf_total_stopped: list = []
        self._buf_total_waiting_time: list = []
        self._buf_mean_waiting_time: list = []
        self._buf_mean_speed: list = []
        self._buf_queue_length: list = []
        self._buf_throughput: list = []
        self._buf_avg_travel_time: list = []
        self._buf_delay: list = []
        self._vehicles_arrived: int = 0
        self._total_travel_time: float = 0.0
        self._vehicle_entry_step: dict = {}

    def reset(self) -> np.ndarray:
        self._safe_close()
        self._reset_metric_buffers()

        port = _get_free_port()
        cmd = [
            "sumo", "-c", self.cfg_path,
            "--no-step-log", "--no-warnings", "--random", "--quit-on-end",
            "--remote-port", str(port),
        ]
        self._proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(1.0)

        if self._proc.poll() is not None:
            stderr = self._proc.stderr.read().decode()
            raise RuntimeError(f"SUMO crashed on startup:\n{stderr}")

        traci.init(port=port, numRetries=10)
        self._running = True
        self.current_step = 0
        self.current_phase = 0
        traci.trafficlight.setRedYellowGreenState(self.tls_id, self.PHASES[0][0])
        return self._observe()

    def step(self, action: int):
        if action != self.current_phase:
            traci.trafficlight.setRedYellowGreenState(
                self.tls_id, self.PHASES[self.current_phase][1]
            )
            for _ in range(self.YELLOW_DURATION):
                traci.simulationStep()
                self._record()
                self.current_step += 1

        traci.trafficlight.setRedYellowGreenState(self.tls_id, self.PHASES[action][0])
        self.current_phase = action

        reward = 0.0
        for _ in range(self.MIN_GREEN):
            traci.simulationStep()
            self._record()
            self.current_step += 1
            reward -= sum(traci.edge.getWaitingTime(e) for e in self.INCOMING_EDGES)

        done = self.current_step >= self.max_steps
        return self._observe(), reward, done

    def close(self) -> None:
        self._safe_close()

    def _observe(self) -> np.ndarray:
        ns_queue = sum(traci.edge.getLastStepHaltingNumber(e) for e in ("N2C", "S2C"))
        ew_queue = sum(traci.edge.getLastStepHaltingNumber(e) for e in ("E2C", "W2C"))
        ns_wait = sum(traci.edge.getWaitingTime(e) for e in ("N2C", "S2C"))
        ew_wait = sum(traci.edge.getWaitingTime(e) for e in ("E2C", "W2C"))
        ns_speed = float(np.mean([traci.edge.getLastStepMeanSpeed(e) for e in ("N2C", "S2C")]))
        ew_speed = float(np.mean([traci.edge.getLastStepMeanSpeed(e) for e in ("E2C", "W2C")]))
        time_of_day = self.current_step / max(self.max_steps, 1)

        return np.array([
            min(ns_queue / self.MAX_QUEUE, 1.0),
            min(ew_queue / self.MAX_QUEUE, 1.0),
            min(ns_wait / self.MAX_WAIT, 1.0),
            min(ew_wait / self.MAX_WAIT, 1.0),
            min(ns_speed / self.MAX_SPEED, 1.0),
            min(ew_speed / self.MAX_SPEED, 1.0),
            float(self.current_phase),
            float(time_of_day),
        ], dtype=np.float32)

    def _record(self) -> None:
        incoming_vids: list = []
        for edge in self.INCOMING_EDGES:
            incoming_vids.extend(traci.edge.getLastStepVehicleIDs(edge))

        for vid in traci.vehicle.getIDList():
            if vid not in self._vehicle_entry_step:
                self._vehicle_entry_step[vid] = self.current_step

        arrived = traci.simulation.getArrivedIDList()
        for vid in arrived:
            if vid in self._vehicle_entry_step:
                travel = (self.current_step - self._vehicle_entry_step[vid]) * STEP_LENGTH
                self._total_travel_time += travel
                self._vehicles_arrived += 1
        self._buf_throughput.append(len(arrived))

        avg_travel = self._total_travel_time / max(self._vehicles_arrived, 1)
        n = len(incoming_vids)

        if n == 0:
            self._buf_total_stopped.append(0)
            self._buf_total_waiting_time.append(0.0)
            self._buf_mean_waiting_time.append(0.0)
            self._buf_mean_speed.append(0.0)
            self._buf_queue_length.append(0)
            self._buf_avg_travel_time.append(avg_travel)
            self._buf_delay.append(0.0)
            return

        speeds = [traci.vehicle.getSpeed(v) for v in incoming_vids]
        waits = [traci.vehicle.getWaitingTime(v) for v in incoming_vids]

        delays = []
        for vid in incoming_vids:
            try:
                ff = FREE_FLOW_TIME.get(traci.vehicle.getTypeID(vid), DEFAULT_FREE_FLOW)
                delays.append(max(0.0, traci.vehicle.getWaitingTime(vid) - ff))
            except Exception:
                delays.append(0.0)

        total_queue = sum(traci.edge.getLastStepHaltingNumber(e) for e in self.INCOMING_EDGES)

        self._buf_total_stopped.append(int(sum(1 for s in speeds if s < 0.1)))
        self._buf_total_waiting_time.append(float(sum(waits)))
        self._buf_mean_waiting_time.append(float(np.mean(waits)))
        self._buf_mean_speed.append(float(np.mean(speeds)))
        self._buf_queue_length.append(int(total_queue))
        self._buf_avg_travel_time.append(avg_travel)
        self._buf_delay.append(float(np.mean(delays)) if delays else 0.0)

    def _safe_close(self) -> None:
        if self._running:
            try:
                traci.close()
            except Exception:
                pass
            self._running = False
        if self._proc is not None:
            try:
                self._proc.kill()
                self._proc.wait()
            except Exception:
                pass
            self._proc = None
        subprocess.run(["pkill", "-9", "-f", "sumo"], capture_output=True)
        time.sleep(0.5)

    def get_metrics(self) -> dict:
        return {
            "system_total_stopped": np.array(self._buf_total_stopped),
            "system_total_waiting_time": np.array(self._buf_total_waiting_time),
            "system_mean_waiting_time": np.array(self._buf_mean_waiting_time),
            "system_mean_speed": np.array(self._buf_mean_speed),
            "avg_waiting_time": np.array(self._buf_mean_waiting_time),
            "avg_travel_time": np.array(self._buf_avg_travel_time),
            "queue_length": np.array(self._buf_queue_length),
            "throughput": np.array(self._buf_throughput),
            "delay": np.array(self._buf_delay),
        }

    @property
    def n_actions(self) -> int:
        return 2

    @property
    def state_dim(self) -> int:
        return 8
