"""HEX20 Milestone 5 - anti-replay protection."""

from __future__ import annotations


class ReplayGuard:
    """Accept only counters strictly newer than the last accepted counter."""

    def __init__(self, initial_counter: int = -1) -> None:
        self.last_counter = initial_counter

    def accept(self, counter: int) -> bool:
        if counter <= self.last_counter:
            return False
        self.last_counter = counter
        return True
