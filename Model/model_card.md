---
tags:
- reinforcement-learning
- ppo
- traffic-signal-control
- pytorch
- sumo
library_name: pytorch
---

# BanTRel

A PPO (Proximal Policy Optimization) agent trained to control a 4-way
traffic signal intersection, simulating Bangalore traffic conditions
(16,400 vehicles/day, 12 turning movements) in SUMO.

## Model Details

- **Algorithm:** PPO (clipped surrogate objective, GAE, orthogonal init)
- **Architecture:** Shared-backbone actor-critic — `Linear(8,64) → Tanh → Linear(64,64) → Tanh` with separate actor `Linear(64,2)` and critic `Linear(64,1)` heads
- **Parameters:** 4,931
- **Framework:** PyTorch 2.11.0+cpu
- **Training episodes:** 150 (100 Phase 1 + 50 Phase 2 fine-tuning)
- **Best episode reward:** -1937120
- **Final 10-episode mean reward:** -2086767.00
- **Overall mean reward:** -2101604.27

## Evaluation: PPO vs Fixed-Cycle Baseline

| Metric | Unit | PPO | Fixed-Cycle |
|---|---|---|---|
| Total Stopped Vehicles | vehicles | 6.77 | 7.00 |
| Mean Waiting Time | s/vehicle | 15.69 | 14.97 |
| Mean Speed | m/s | 3.01 | 2.96 |
| Avg Travel Time | seconds | 185.18 | 183.22 |
| Throughput | veh/step | 1.97 | 1.97 |
| Delay vs Free-Flow | seconds | 7.04 | 6.22 |

## Files

| File | Description |
|---|---|
| `ppo_bangalore.pt` | State dict only — recommended, load into `ActorCritic(state_dim=8, action_dim=2, hidden=64)` |
| `ppo_bangalore_full.pt` | Full pickled model — requires the `ActorCritic` class at load time |
| `ppo_bangalore_scripted.pt` | TorchScript — deployable without source code |
| `ppo_bangalore.onnx` | ONNX export — cross-framework/language inference |
| `config.json` | Architecture + hyperparameters |
| `training_history.json` | Reward, policy loss, value loss, entropy curves |
| `evaluation_results.json` | Full PPO vs Fixed-Cycle evaluation metrics |

## Usage

```python
import torch
import torch.nn as nn

class ActorCritic(nn.Module):
    def __init__(self, state_dim=8, action_dim=2, hidden=64):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.actor = nn.Linear(hidden, action_dim)
        self.critic = nn.Linear(hidden, 1)

    def forward(self, x):
        features = self.backbone(x)
        return self.actor(features), self.critic(features)

model = ActorCritic()
model.load_state_dict(torch.load("ppo_bangalore.pt", map_location="cpu"))
model.eval()

# Get an action for a given state
import torch
state = torch.randn(1, 8)  # replace with real 8-dim state
with torch.no_grad():
    logits, value = model(state)
    action = torch.argmax(logits, dim=-1).item()
```

Or without needing the class definition (TorchScript):

```python
import torch
model = torch.jit.load("ppo_bangalore_scripted.pt")
model.eval()
```

## Training Environment

- **Simulator:** SUMO (Simulation of Urban MObility)
- **Intersection:** 4-way, 2 lanes/edge, 12 turning movements, traffic-light-controlled center node
- **Traffic schedule:** Derived from observed Bangalore volumes across night / morning rush / mid-morning / afternoon / evening rush / evening periods
- **Vehicle mix:** 60% cars, 30% motorcycles, 10% auto-rickshaws
- **Reward:** Negative sum of edge waiting times, normalised to [-10, 0]
- **State space:** 8-dimensional (queue/wait features per approach)
- **Action space:** 2 discrete actions (NS-green / EW-green phase selection)

## Citation

If you use this model, please cite this repository.
