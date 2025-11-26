"""Machine and work center abstractions."""
from __future__ import annotations

from dataclasses import dataclass
import simpy


@dataclass
class Machine:
    name: str
    setup_time: float = 0.0
    capacity: int = 1


class WorkCenter:
    """Resource representing one or more machines."""

    def __init__(self, name: str, machines: list[Machine]):
        self.name = name
        self.machines = machines
        self._resource: simpy.Resource | None = None

    def capacity(self) -> int:
        return sum(m.capacity for m in self.machines)

    def bind(self, env: simpy.Environment) -> simpy.Resource:
        if self._resource is None:
            self._resource = simpy.Resource(env, capacity=max(self.capacity(), 1))
        return self._resource
