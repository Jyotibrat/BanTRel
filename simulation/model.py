"""
ActorCritic architecture — verbatim port of network.py, so `torch.load`ing
your `best_ppo_bangalore.pt` / HF checkpoint state_dict works unmodified.

PPOPolicy wraps it for serving:
  - deterministic=True  -> argmax over action logits (default for the web
    demo: reproducible, same input always gives the same output).
  - deterministic=False -> samples from Categorical(logits), matching the
    exact `run_evaluation` protocol used in BanTRel.py Cell 13. Pass a seed
    for reproducible sampling.
"""

import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical

DEVICE = torch.device("cpu")


class ActorCritic(nn.Module):
    def __init__(self, state_dim: int = 8, action_dim: int = 2, hidden: int = 64) -> None:
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.actor = nn.Linear(hidden, action_dim)
        self.critic = nn.Linear(hidden, 1)

    def forward(self, x: torch.Tensor):
        features = self.backbone(x)
        return self.actor(features), self.critic(features)


class PPOPolicy:
    """Inference-only wrapper. Has .choose_action(state) + .reset() like FixedCyclePolicy,
    so runner.py can treat both policies identically."""

    def __init__(self, checkpoint_path: str, deterministic: bool = True, seed: int | None = None):
        self.net = ActorCritic().to(DEVICE)
        state_dict = torch.load(checkpoint_path, map_location=DEVICE)
        self.net.load_state_dict(state_dict)
        self.net.eval()
        self.deterministic = deterministic
        self._rng = np.random.default_rng(seed) if seed is not None else None
        if seed is not None:
            torch.manual_seed(seed)

    def choose_action(self, state: np.ndarray) -> int:
        with torch.no_grad():
            tensor = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
            logits, _value = self.net(tensor)
            if self.deterministic:
                return int(torch.argmax(logits, dim=-1).item())
            dist = Categorical(logits=logits)
            return int(dist.sample().item())

    def reset(self) -> None:
        pass  # stateless across steps — nothing to reset
