"""
Define the shared-backbone Actor-Critic neural network.

Architecture:
    - Two-layer backbone with 64 hidden units and Tanh activation.
    - Separate linear heads for the actor (action logits) and
      critic (state value estimate).
    - Orthogonal weight initialisation, which is standard practice
      for PPO and improves early training stability.

State dimension  : 8 (normalised queue lengths, waiting times, speeds,
                      current phase, and time-of-day fraction)
Action space     : 2 discrete actions (NS-green = 0, EW-green = 1)
"""

import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Compute device : {DEVICE}")


class ActorCritic(nn.Module):
    """
    Shared-backbone actor-critic network for discrete action spaces.

    Parameters
    ----------
    state_dim  : Dimension of the input state vector.
    action_dim : Number of discrete actions.
    hidden     : Width of each hidden layer.
    """

    def __init__(self, state_dim: int = 8,
                 action_dim: int = 2,
                 hidden: int = 64) -> None:
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
        )
        self.actor  = nn.Linear(hidden, action_dim)
        self.critic = nn.Linear(hidden, 1)
        self._init_weights()

    def _init_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.orthogonal_(module.weight, gain=np.sqrt(2))
                nn.init.zeros_(module.bias)
        nn.init.orthogonal_(self.actor.weight,  gain=0.01)
        nn.init.orthogonal_(self.critic.weight, gain=1.0)

    def forward(self, x: torch.Tensor):
        features = self.backbone(x)
        return self.actor(features), self.critic(features)

    def get_action(self, state: np.ndarray):
        """Sample one action from the current policy without gradient tracking."""
        with torch.no_grad():
            tensor        = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
            logits, value = self(tensor)
            dist          = Categorical(logits=logits)
            action        = dist.sample()
        return action.item(), dist.log_prob(action), value

    def evaluate(self, states: torch.Tensor, actions: torch.Tensor):
        """Evaluate a batch of state-action pairs for the PPO update step."""
        logits, values = self(states)
        dist           = Categorical(logits=logits)
        log_probs      = dist.log_prob(actions)
        entropy        = dist.entropy()
        return log_probs, values.squeeze(-1), entropy


n_params = sum(p.numel() for p in ActorCritic().parameters())
print(f"Network parameters : {n_params:,}")
print(f"Hidden width       : 64")
print(f"Activation         : Tanh")
print(f"Weight init        : Orthogonal")