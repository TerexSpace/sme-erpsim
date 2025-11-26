"""Worker abstractions."""
from __future__ import annotations

from dataclasses import dataclass
import simpy


@dataclass
class Worker:
    name: str
    skills: tuple[str, ...] = ()


class WorkerPool:
    """Pool of interchangeable workers modeled as a SimPy resource."""

    def __init__(self, name: str, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.name = name
        self.capacity = capacity
        self._resource: simpy.Resource | None = None

    def bind(self, env: simpy.Environment) -> simpy.Resource:
        if self._resource is None:
            self._resource = simpy.Resource(env, capacity=self.capacity)
        return self._resource
