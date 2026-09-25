"""
Route-file generation, generalized from BanTRel.py Cell 4.

The original notebook hardcoded one schedule (the 16,400 veh/day Bangalore
split) and one mix (60/30/10 car/bike/auto). This module keeps that as the
"preset" option, and adds a "custom" path that scales the SAME 7-period
day-shape (so the model still sees a realistic time-of-day pattern it was
trained on) by a user-chosen total volume, with a user-chosen vehicle mix.

Scaling the known shape (rather than inventing an arbitrary schedule) keeps
state normalisation (MAX_QUEUE=80, MAX_WAIT=600 in env.py) meaningful —
wildly different shapes would push the model into state regions it never
saw during training.
"""

import os
from typing import Literal

SECONDS_PER_HOUR = 3600

# Each entry: (begin_s, end_s, total_vehicles, label) — verbatim from BanTRel.py
DEFAULT_SCHEDULE = [
    (0,                     8  * SECONDS_PER_HOUR,  550, "Night (00:00-08:00)"),
    (8  * SECONDS_PER_HOUR, 11 * SECONDS_PER_HOUR, 4000, "Morning rush (08:00-11:00)"),
    (11 * SECONDS_PER_HOUR, 13 * SECONDS_PER_HOUR, 2850, "Mid-morning (11:00-13:00)"),
    (13 * SECONDS_PER_HOUR, 16 * SECONDS_PER_HOUR, 2100, "Afternoon (13:00-16:00)"),
    (16 * SECONDS_PER_HOUR, 20 * SECONDS_PER_HOUR, 4400, "Evening rush (16:00-20:00)"),
    (20 * SECONDS_PER_HOUR, 23 * SECONDS_PER_HOUR, 2500, "Evening (20:00-23:00)"),
    (23 * SECONDS_PER_HOUR, 86400,                   550, "Night (23:00-24:00)"),
]
DEFAULT_TOTAL = sum(t for _, _, t, _ in DEFAULT_SCHEDULE)  # 16,400
DEFAULT_MIX = {"car": 0.60, "bike": 0.30, "auto": 0.10}

PRESET_PERIOD_IDS = {
    "night":         DEFAULT_SCHEDULE[0],
    "morning_rush":  DEFAULT_SCHEDULE[1],
    "mid_morning":   DEFAULT_SCHEDULE[2],
    "afternoon":     DEFAULT_SCHEDULE[3],
    "evening_rush":  DEFAULT_SCHEDULE[4],
    "evening":       DEFAULT_SCHEDULE[5],
}

ALL_ROUTES = [
    ("route_ns", "N2C C2S"), ("route_nw", "N2C C2W"), ("route_ne", "N2C C2E"),
    ("route_sn", "S2C C2N"), ("route_sw", "S2C C2W"), ("route_se", "S2C C2E"),
    ("route_en", "E2C C2N"), ("route_ew", "E2C C2W"), ("route_es", "E2C C2S"),
    ("route_wn", "W2C C2N"), ("route_we", "W2C C2E"), ("route_ws", "W2C C2S"),
]

VEHICLE_TYPES_XML = (
    '    <vType id="car"  accel="2.6" decel="4.5" sigma="0.5" '
    'length="5" minGap="2.5" maxSpeed="13.89"/>\n'
    '    <vType id="bike" accel="3.0" decel="5.0" sigma="0.6" '
    'length="2" minGap="1.5" maxSpeed="11.11" vClass="motorcycle"/>\n'
    '    <vType id="auto" accel="2.0" decel="4.0" sigma="0.5" '
    'length="4" minGap="2.0" maxSpeed="11.11"/>'
)


def build_schedule(
    mode: Literal["preset", "custom"],
    total_vehicles: int | None = None,
    period: str | None = None,
) -> list[tuple[int, int, int, str]]:
    """
    mode="preset", period=None        -> full 24h canonical Bangalore day
    mode="preset", period="morning_rush" -> just that one period, run in isolation
    mode="custom", total_vehicles=N   -> full 24h shape, each period scaled so
                                          the day sums to N vehicles instead of 16,400
    """
    if mode == "preset":
        if period is None:
            return DEFAULT_SCHEDULE
        if period not in PRESET_PERIOD_IDS:
            raise ValueError(f"Unknown period '{period}'. Options: {list(PRESET_PERIOD_IDS)}")
        begin, end, total, label = PRESET_PERIOD_IDS[period]
        # Re-anchor to start at t=0 so the episode is just this period's length.
        return [(0, end - begin, total, label)]

    if mode == "custom":
        if not total_vehicles or total_vehicles <= 0:
            raise ValueError("custom mode requires total_vehicles > 0")
        scale = total_vehicles / DEFAULT_TOTAL
        return [
            (begin, end, max(1, round(total * scale)), label)
            for begin, end, total, label in DEFAULT_SCHEDULE
        ]

    raise ValueError(f"Unknown mode '{mode}'")


def make_route_file(
    filepath: str,
    schedule: list[tuple[int, int, int, str]],
    mix: dict[str, float] | None = None,
) -> int:
    """Writes the SUMO route file. Returns the number of <flow> entries written."""
    mix = mix or DEFAULT_MIX
    total_pct = sum(mix.values())
    if abs(total_pct - 1.0) > 0.01:
        raise ValueError(f"Vehicle mix must sum to 1.0 (got {total_pct:.3f})")

    route_tags = "\n".join(
        f'    <route id="{rid}" edges="{edges}"/>' for rid, edges in ALL_ROUTES
    )

    flow_tags = []
    flow_id = 0
    for begin, end, total_veh, _label in schedule:
        duration_hr = max((end - begin) / SECONDS_PER_HOUR, 1e-6)
        total_per_hr = total_veh / duration_hr
        per_route_hr = total_per_hr / len(ALL_ROUTES)

        for route_id, _ in ALL_ROUTES:
            tag = route_id.removeprefix("route_")
            for vtype, proportion in mix.items():
                rate = per_route_hr * proportion
                if rate <= 0:
                    continue
                flow_tags.append(
                    f'    <flow id="f{flow_id:04d}_{vtype}_{tag}" '
                    f'route="{route_id}" type="{vtype}" '
                    f'begin="{begin}" end="{end}" '
                    f'vehsPerHour="{rate:.1f}" '
                    f'departSpeed="max" departPos="base" departLane="best"/>'
                )
                flow_id += 1

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<routes>\n'
        + VEHICLE_TYPES_XML + "\n\n"
        + route_tags + "\n\n"
        + "\n".join(flow_tags) + "\n</routes>"
    )
    with open(filepath, "w") as f:
        f.write(xml)
    return flow_id


def make_sumocfg(route_filename: str, net_filename: str, cfg_path: str,
                  duration: int, step_length: int = 10) -> None:
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_filename}"/>
        <route-files value="{route_filename}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="{duration}"/>
        <step-length value="{step_length}"/>
    </time>
</configuration>"""
    with open(cfg_path, "w") as f:
        f.write(xml)


def prepare_run_config(
    run_dir: str,
    net_path: str,
    mode: Literal["preset", "custom"],
    total_vehicles: int | None = None,
    period: str | None = None,
    mix: dict[str, float] | None = None,
    step_length: int = 10,
) -> str:
    """
    Builds a fresh .rou.xml + .sumocfg for one simulation run inside run_dir
    (a per-job temp directory, so concurrent requests never collide on files).
    Returns the .sumocfg path.
    """
    os.makedirs(run_dir, exist_ok=True)
    schedule = build_schedule(mode, total_vehicles, period)
    duration = schedule[-1][1]  # end time of the last period

    route_path = os.path.join(run_dir, "routes.rou.xml")
    cfg_path = os.path.join(run_dir, "sim.sumocfg")

    n_flows = make_route_file(route_path, schedule, mix)
    if n_flows == 0:
        raise ValueError("Generated route file has zero flows — check demand/mix inputs.")

    # sumocfg references the shared, pre-built network by relative path.
    net_filename = os.path.relpath(net_path, run_dir)
    make_sumocfg("routes.rou.xml", net_filename, cfg_path, duration, step_length)
    return cfg_path
