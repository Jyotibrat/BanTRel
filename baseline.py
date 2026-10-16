"""Fixed-cycle baseline controller — verbatim port of BanTRel.py Cell 9."""


class FixedCyclePolicy:
    """
    Deterministic fixed-cycle traffic signal controller.
    cycle_steps=3, step_length=10s -> 30s per phase, 60s full cycle.
    """

    def __init__(self, cycle_steps: int = 3) -> None:
        self.cycle_steps = cycle_steps
        self.step_counter = 0

    def choose_action(self, state) -> int:
        phase = (self.step_counter // self.cycle_steps) % 2
        self.step_counter += 1
        return int(phase)

    def reset(self) -> None:
        self.step_counter = 0
