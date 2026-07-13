"""
Define the PPO agent and the Fixed-Cycle baseline policy.

PPO hyperparameters (matched to the 2WSI-RL benchmark where applicable):
    gamma        = 0.95   discount factor
    lr           = 3e-4   Adam learning rate (equivalent role to alpha)
    eps_clip     = 0.2    clipping range (analogous to epsilon)
    gae_lambda   = 0.95   generalised advantage estimation lambda
    k_epochs     = 8      update passes per collected rollout
    rollout_len  = 1024   steps collected before each update

Reward normalisation:
    The raw reward (negative sum of edge waiting times) can reach -50,000
    per step under heavy traffic. It is divided by 1,000 and clipped to
    [-10, 0] to keep gradient magnitudes stable across traffic periods.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class PPOAgent:
    """
    Proximal Policy Optimisation agent with clipped surrogate objective,
    Generalised Advantage Estimation (GAE), and mini-batch updates.
    """

    def __init__(
        self,
        state_dim:    int   = 8,
        action_dim:   int   = 2,
        lr:           float = 3e-4,
        gamma:        float = 0.95,
        eps_clip:     float = 0.2,
        gae_lambda:   float = 0.95,
        k_epochs:     int   = 8,
        rollout_len:  int   = 1024,
        entropy_coef: float = 0.05,
        vf_coef:      float = 0.5,
        mini_batch:   int   = 256,
    ) -> None:
        self.gamma        = gamma
        self.eps_clip     = eps_clip
        self.gae_lambda   = gae_lambda
        self.k_epochs     = k_epochs
        self.rollout_len  = rollout_len
        self.entropy_coef = entropy_coef
        self.vf_coef      = vf_coef
        self.mini_batch   = mini_batch

        self.net     = ActorCritic(state_dim, action_dim).to(DEVICE)
        self.opt     = optim.Adam(self.net.parameters(), lr=lr, eps=1e-5)
        self.lr_init = lr
        self.lr_now  = lr

        self._clear_buffer()
        self.total_steps:  int  = 0
        self.update_count: int  = 0
        self.policy_losses: list = []
        self.value_losses:  list = []
        self.entropy_hist:  list = []

    # ------------------------------------------------------------------
    # Rollout buffer
    # ------------------------------------------------------------------

    def _clear_buffer(self) -> None:
        self.buf_states:   list = []
        self.buf_actions:  list = []
        self.buf_logprobs: list = []
        self.buf_rewards:  list = []
        self.buf_dones:    list = []
        self.buf_values:   list = []

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def choose_action(self, state: np.ndarray) -> int:
        """Choose an action and store the transition in the rollout buffer."""
        action, log_prob, value = self.net.get_action(state)
        self.buf_states.append(state)
        self.buf_actions.append(action)
        self.buf_logprobs.append(log_prob.item())
        self.buf_values.append(value.item())
        self.total_steps += 1
        return action

    def store_reward(self, reward: float, done: bool) -> None:
        """Normalise and store the reward for the last action taken."""
        normalised = max(reward / 1000.0, -10.0)
        self.buf_rewards.append(normalised)
        self.buf_dones.append(float(done))

    # ------------------------------------------------------------------
    # Learning
    # ------------------------------------------------------------------

    def update(self) -> None:
        """Run a PPO update step when the rollout buffer is full."""
        if len(self.buf_rewards) < self.rollout_len:
            return

        rewards = np.array(self.buf_rewards, dtype=np.float32)
        dones   = np.array(self.buf_dones,   dtype=np.float32)
        values  = np.array(self.buf_values,  dtype=np.float32)

        # Generalised Advantage Estimation
        advantages = np.zeros_like(rewards)
        last_adv   = 0.0
        for t in reversed(range(len(rewards))):
            next_val      = values[t + 1] if t + 1 < len(values) else 0.0
            delta         = (
                rewards[t]
                + self.gamma * next_val * (1.0 - dones[t])
                - values[t]
            )
            advantages[t] = last_adv = (
                delta
                + self.gamma * self.gae_lambda * (1.0 - dones[t]) * last_adv
            )

        returns    = advantages + values
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        t_states  = torch.FloatTensor(np.array(self.buf_states)).to(DEVICE)
        t_actions = torch.LongTensor(self.buf_actions).to(DEVICE)
        t_old_lp  = torch.FloatTensor(self.buf_logprobs).to(DEVICE)
        t_adv     = torch.FloatTensor(advantages).to(DEVICE)
        t_ret     = torch.FloatTensor(returns).to(DEVICE)

        p_losses, v_losses, entropies = [], [], []

        for _ in range(self.k_epochs):
            indices = np.random.permutation(len(t_states))
            for start in range(0, len(indices), self.mini_batch):
                mb = indices[start : start + self.mini_batch]

                new_lp, val_pred, entropy = self.net.evaluate(
                    t_states[mb], t_actions[mb]
                )
                ratio = torch.exp(new_lp - t_old_lp[mb])
                surr1 = ratio * t_adv[mb]
                surr2 = torch.clamp(
                    ratio, 1.0 - self.eps_clip, 1.0 + self.eps_clip
                ) * t_adv[mb]

                p_loss = -torch.min(surr1, surr2).mean()
                v_loss = nn.MSELoss()(val_pred, t_ret[mb])
                e_loss = -entropy.mean()
                loss   = p_loss + self.vf_coef * v_loss + self.entropy_coef * e_loss

                self.opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.net.parameters(), 0.5)
                self.opt.step()

                p_losses.append(p_loss.item())
                v_losses.append(v_loss.item())
                entropies.append(entropy.mean().item())

        self.policy_losses.append(float(np.mean(p_losses)))
        self.value_losses.append(float(np.mean(v_losses)))
        self.entropy_hist.append(float(np.mean(entropies)))
        self.update_count += 1
        self._clear_buffer()

    def lr_decay(self, episode: int, total_episodes: int) -> None:
        """Linearly anneal the learning rate from lr_init to lr_init / 10."""
        frac = 1.0 - 0.9 * (episode / total_episodes)
        self.lr_now = self.lr_init * frac
        for group in self.opt.param_groups:
            group["lr"] = self.lr_now

    def stats(self) -> dict:
        """Return a summary of the current training state."""
        return {
            "updates"  : self.update_count,
            "steps"    : self.total_steps,
            "p_loss"   : round(self.policy_losses[-1], 4) if self.policy_losses else 0.0,
            "v_loss"   : round(self.value_losses[-1],  4) if self.value_losses  else 0.0,
            "entropy"  : round(self.entropy_hist[-1],  4) if self.entropy_hist  else 0.0,
            "lr"       : round(self.lr_now, 6),
        }


print("PPO agent defined.")
print(f"  gamma        : 0.95")
print(f"  lr           : 3e-4  (annealed to 3e-5 over training)")
print(f"  eps_clip     : 0.2")
print(f"  gae_lambda   : 0.95")
print(f"  k_epochs     : 8")
print(f"  rollout_len  : 1024")
print(f"  mini_batch   : 256")