
<h1 align="center">
BanTRel — Bangalore Traffic Reinforcement Learning
</h1>

**BanTRel** (Bangalore Traffic Reinforcement Learning) is a reinforcement learning project that trains a Proximal Policy Optimisation (PPO) agent to control a single signalised intersection modelled on real Bangalore traffic demand data. The agent is trained and evaluated entirely within [SUMO (Simulation of Urban MObility)](https://sumo.dlr.de/), a microscopic open-source traffic simulator.

---

## Results

The trained PPO agent was evaluated against a Fixed-Cycle baseline over three independent runs (each run simulates a full 24-hour day). All metrics are averaged across runs.

| Metric | Unit | PPO | Fixed-Cycle | Delta | Outcome |
|---|---|---|---|---|---|
| **Total Stopped Vehicles** | vehicles | 6.773 | 6.997 | −0.224 | PPO |
| **Total Waiting Time** | seconds | 264.106 | 269.153 | −5.047 | PPO |
| **Mean Waiting Time** | s / vehicle | 15.691 | 14.968 | +0.723 | Fixed-Cycle |
| **Mean Speed** | m/s | 3.005 | 2.959 | +0.047 | PPO |
| Avg Waiting Time | s / vehicle | 15.691 | 14.968 | +0.723 | Fixed-Cycle |
| Avg Travel Time | seconds | 185.179 | 183.218 | +1.961 | Fixed-Cycle |
| Queue Length | vehicles | 6.773 | 6.997 | −0.224 | PPO |
| Throughput | veh / step | 1.974 | 1.973 | +0.000 | Tie |
| Delay vs Free-Flow | seconds | 7.039 | 6.217 | +0.822 | Fixed-Cycle |

**Final score — PPO: 4 / Fixed-Cycle: 4 / Ties: 1**

The PPO agent meaningfully reduces total congestion (fewer stopped vehicles, lower total waiting time, shorter queues) while the fixed-cycle policy edges ahead on per-vehicle averages due to the asymmetric traffic mix across Bangalore's rush-hour periods.

---

## Project Overview

### Problem Statement

Urban intersections in Bangalore experience severe congestion across multiple daily peaks — morning rush (08:00–11:00), lunch (13:00–16:00), and evening rush (16:00–20:00). A fixed-cycle traffic signal cannot adapt to real-time queue imbalances. This project investigates whether a PPO-based adaptive signal controller can reduce overall vehicle waiting time in a realistic simulation of that demand.

### Approach

1. A four-way intersection is modelled in SUMO with 12 turning movements (straight, left, right from each arm) and two lanes per edge.
2. Traffic demand is derived from observed Bangalore vehicle counts (16,400 vehicles per day) and split into six time periods using a 60 % car / 30 % motorcycle / 10 % auto-rickshaw vehicle mix.
3. A PPO agent with a shared actor-critic backbone observes an 8-dimensional state vector (queue lengths, waiting times, speeds, current phase, time of day) and selects between NS-green and EW-green at every decision step.
4. Training runs for 150 episodes (100 Phase 1 + 50 fine-tuning) on a 24-hour simulation with `step_length = 10 s`.
5. The trained agent is compared against a Fixed-Cycle baseline that alternates phases every 30 seconds.

---

## Traffic Data

Traffic volumes used in this project are based on average counts obtained from Google resources for a representative two-way intersection in Bangalore.

> **Disclaimer:** These figures represent approximate averages and have not been verified through direct field measurements. Actual traffic volumes at any specific Bangalore intersection may differ significantly depending on location, day of week, season, and local conditions.

| Period | Hours | Total vehicles |
|---|---|---|
| Night | 00:00 – 08:00 | 550 |
| Morning rush | 08:00 – 11:00 | 4,000 |
| Mid-morning | 11:00 – 13:00 | 2,850 |
| Afternoon | 13:00 – 16:00 | 2,100 |
| Evening rush | 16:00 – 20:00 | 4,400 |
| Evening | 20:00 – 23:00 | 2,500 |
| **Total** | **24 hours** | **16,400** |

---

## Simulation Environment

| Parameter | Value |
|---|---|
| Simulator | SUMO (Simulation of Urban MObility) |
| Intersection type | 4-way signalised, 2 lanes per edge |
| Turn movements | 12 (straight, left, right from each arm) |
| Vehicle types | Car (60 %), Motorcycle (30 %), Auto-rickshaw (10 %) |
| Simulation duration | 86,400 s (24 hours) |
| Step length | 10 s |
| Steps per episode | 8,640 |
| Minimum green phase | 80 s (8 steps) |
| Yellow phase | 10 s (1 step) |
| Interface | TraCI (Traffic Control Interface) |

---

## Agent Architecture

### Network

```
Input (8-dim state)
        |
  Linear(8 → 64) + Tanh
        |
  Linear(64 → 64) + Tanh
        |
   ┌────┴────┐
Actor       Critic
Linear(64→2) Linear(64→1)
(action     (state
 logits)     value)
```

Total parameters: ~9,000. Weight initialisation: Orthogonal.

### State Vector

| Index | Feature | Normalisation |
|---|---|---|
| 0 | NS halting vehicle count | / 80 |
| 1 | EW halting vehicle count | / 80 |
| 2 | NS total waiting time | / 600 s |
| 3 | EW total waiting time | / 600 s |
| 4 | NS mean speed | / 13.89 m/s |
| 5 | EW mean speed | / 13.89 m/s |
| 6 | Current phase | 0 or 1 |
| 7 | Time of day | fraction of episode |

### PPO Hyperparameters

| Parameter | Value | Notes |
|---|---|---|
| Discount factor γ | 0.95 | |
| Learning rate (Phase 1) | 3 × 10⁻⁴ | Adam optimiser |
| Learning rate (Phase 2) | 5 × 10⁻⁵ | Fine-tuning |
| Clip range ε | 0.2 | |
| GAE lambda | 0.95 | |
| Update epochs per rollout | 8 | |
| Rollout length | 1,024 steps | |
| Mini-batch size | 256 | |
| Entropy coefficient | 0.05 | |
| Value function coefficient | 0.5 | |
| Reward normalisation | ÷ 1000, clipped to [−10, 0] | |

---

## Evaluation Metrics

### Benchmark Metrics (2WSI-RL Protocol)

These four metrics directly match the evaluation protocol used in the reference repository:

- **Total Stopped Vehicles** — number of vehicles with speed < 0.1 m/s at the intersection per step
- **Total Waiting Time** — cumulative waiting time of all vehicles on incoming edges (seconds)
- **Mean Waiting Time** — average waiting time per vehicle on incoming edges (seconds)
- **Mean Speed** — average speed of vehicles on incoming edges (m/s)

### Additional Metrics

- **Average Waiting Time** — mean waiting time per vehicle (same measurement scope as above)
- **Average Travel Time** — mean time from network entry to exit per vehicle (seconds)
- **Queue Length** — total halting vehicles across all incoming edges
- **Throughput** — vehicles completing their trip per simulation step
- **Delay vs Free-Flow** — excess waiting time relative to the theoretical free-flow travel time, computed per vehicle type

---

## How to Run

### Requirements

- Google Colab (recommended) or Ubuntu 22.04+ with Python 3.10+
- SUMO ≥ 1.19 (installed automatically in the notebook)
- Python packages: `torch`, `traci`, `numpy`, `matplotlib`

### Steps

1. Open `BanTRel.ipynb` in Google Colab.
2. Run all cells in order from Cell 1 to Cell 17.
3. Cell 1 installs SUMO and all Python dependencies automatically.
4. Training (Cells 10 and 12) takes approximately 100–120 minutes on a standard Colab CPU runtime.
5. The final zip archives (`sumo_config.zip`, `results.zip`, `model.zip`) are downloaded automatically by the last cell.

> **Note:** To prevent the Colab session from going idle during training, open a second browser tab with the same notebook and run the keep-alive cell before starting training.

---

## Credits and Acknowledgements

### Reference Repository

This project's evaluation methodology, benchmark metrics, and traffic scenario design are directly inspired by:

> **2WSI-RL — 2-Way Signalised Intersection Reinforcement Learning**
> Chimisso, R. et al.
> [https://github.com/rChimisso/2WSI-RL](https://github.com/rChimisso/2WSI-RL)

The four benchmark metrics (system_total_stopped, system_total_waiting_time, system_mean_waiting_time, system_mean_speed), the fixed-cycle baseline design, and the Low Traffic / High Traffic evaluation protocol are all adapted from that repository. The traffic demand structure (12 turning movements, symmetric per-route flows) is also modelled on their network definition.

### SUMO

SUMO (Simulation of Urban MObility) is developed by the German Aerospace Center (DLR) and is available under the Eclipse Public License 2.0.
Website: [https://sumo.dlr.de](https://sumo.dlr.de)

### Traffic Data Source

Vehicle count data used to construct the Bangalore demand schedule was obtained from publicly available Google resources. These figures represent approximate daily averages for a representative urban intersection in Bangalore and **have not been verified through direct field observation**. Real-world traffic volumes at any specific location may differ substantially depending on road type, locality, season, and day of the week.

---

## Limitations

- The simulation models a single isolated intersection. Real urban networks involve interactions between multiple adjacent signals.
- The 12-turn-movement, 2-lane network is a simplified representation. Actual Bangalore intersections may have more lanes, dedicated turning bays, pedestrian phases, and non-motorised traffic.
- PPO training was conducted for 150 episodes. Additional training may improve performance, particularly on per-vehicle average metrics where the fixed-cycle currently holds an edge.
- The agent uses a 2-action discrete policy (NS-green or EW-green). A more granular action space with variable phase durations would more closely resemble a real adaptive signal controller.

---

## License

This project is released for academic and educational purposes. See `LICENSE` for details.