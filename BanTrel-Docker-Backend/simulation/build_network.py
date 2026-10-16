"""
Builds the fixed 4-arm intersection network and derives the traffic-light
phase strings, exactly as done in BanTRel.py Cells 2-3.

This only depends on the intersection GEOMETRY (which never changes per
request), so it is run ONCE — at Docker image build time — rather than on
every simulation. Its output (sumo_config/intersection.net.xml and
sumo_config/phases.json) is committed into the image and just read by
env.py at request time. This avoids re-invoking netconvert + sumolib on
every single API call.

Run manually with:  python simulation/build_network.py
"""

import json
import os
import subprocess
import sys

SUMO_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "sumo_config")


def build_network() -> None:
    os.makedirs(SUMO_CONFIG_DIR, exist_ok=True)

    NODES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<nodes>
    <node id="center" x="0"    y="0"    type="traffic_light"/>
    <node id="north"  x="0"    y="500"  type="priority"/>
    <node id="south"  x="0"    y="-500" type="priority"/>
    <node id="east"   x="500"  y="0"    type="priority"/>
    <node id="west"   x="-500" y="0"    type="priority"/>
</nodes>"""

    EDGES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<edges>
    <edge id="N2C" from="north"  to="center" numLanes="2" speed="13.89"/>
    <edge id="S2C" from="south"  to="center" numLanes="2" speed="13.89"/>
    <edge id="E2C" from="east"   to="center" numLanes="2" speed="13.89"/>
    <edge id="W2C" from="west"   to="center" numLanes="2" speed="13.89"/>
    <edge id="C2N" from="center" to="north"  numLanes="2" speed="13.89"/>
    <edge id="C2S" from="center" to="south"  numLanes="2" speed="13.89"/>
    <edge id="C2E" from="center" to="east"   numLanes="2" speed="13.89"/>
    <edge id="C2W" from="center" to="west"   numLanes="2" speed="13.89"/>
</edges>"""

    nod_path = os.path.join(SUMO_CONFIG_DIR, "intersection.nod.xml")
    edg_path = os.path.join(SUMO_CONFIG_DIR, "intersection.edg.xml")
    net_path = os.path.join(SUMO_CONFIG_DIR, "intersection.net.xml")

    with open(nod_path, "w") as f:
        f.write(NODES_XML)
    with open(edg_path, "w") as f:
        f.write(EDGES_XML)

    result = subprocess.run(
        [
            "netconvert",
            f"--node-files={nod_path}",
            f"--edge-files={edg_path}",
            f"--output-file={net_path}",
            "--tls.guess=true",
            "--tls.guess-signals=true",
            "--no-warnings",
        ],
        capture_output=True,
        text=True,
    )

    net_size = os.path.getsize(net_path) if os.path.exists(net_path) else 0
    if net_size < 5000:
        raise RuntimeError(
            f"netconvert failed to produce a valid network "
            f"({net_size} bytes). stderr:\n{result.stderr[:600]}"
        )
    # NOTE: netconvert is known to segfault (-11) on some builds *after*
    # successfully writing the file — same caveat as the original notebook.
    print(f"netconvert return code: {result.returncode} "
          f"(-11 after a valid file is a known harmless segfault)")
    print(f"Network written: {net_path} ({net_size:,} bytes)")

    # ---- derive phase strings from the compiled network ----
    sumo_home = os.environ.get("SUMO_HOME", "/usr/share/sumo")
    sys.path.append(os.path.join(sumo_home, "tools"))
    import sumolib  # noqa: E402

    def _build_phase_strings(green_indices, length):
        green = ["r"] * length
        yellow = ["r"] * length
        for i in green_indices:
            green[i] = "G"
            yellow[i] = "y"
        return "".join(green), "".join(yellow)

    net = sumolib.net.readNet(net_path)
    tls = net.getTrafficLights()[0]
    conns = tls.getConnections()
    n = len(conns)

    ns_indices, ew_indices = [], []
    for idx, (from_lane, _to_lane, _link) in enumerate(conns):
        edge_id = from_lane.getEdge().getID()
        if edge_id in ("N2C", "S2C"):
            ns_indices.append(idx)
        elif edge_id in ("E2C", "W2C"):
            ew_indices.append(idx)

    ns_green, ns_yellow = _build_phase_strings(ns_indices, n)
    ew_green, ew_yellow = _build_phase_strings(ew_indices, n)

    phases = {
        "tls_id": tls.getID(),
        "NS_GREEN": ns_green, "NS_YELLOW": ns_yellow,
        "EW_GREEN": ew_green, "EW_YELLOW": ew_yellow,
    }
    phases_path = os.path.join(SUMO_CONFIG_DIR, "phases.json")
    with open(phases_path, "w") as f:
        json.dump(phases, f, indent=2)

    print(f"Phases written: {phases_path}")
    print(phases)


if __name__ == "__main__":
    build_network()
