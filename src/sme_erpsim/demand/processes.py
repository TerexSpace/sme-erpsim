"""Demand generation processes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class OrderArrivalProcess:
    """Base arrival process returning interarrival times."""

    def next_interarrival(self, rng: np.random.Generator) -> float:
        raise NotImplementedError


@dataclass
class PoissonOrderArrival(OrderArrivalProcess):
    rate_per_hour: float

    def next_interarrival(self, rng: np.random.Generator) -> float:
        return float(rng.exponential(1.0 / self.rate_per_hour))


@dataclass
class DeterministicArrival(OrderArrivalProcess):
    interarrival_time: float

    def next_interarrival(self, rng: np.random.Generator) -> float:
        return self.interarrival_time


@dataclass
class EmpiricalArrival(OrderArrivalProcess):
    samples: list[float]

    def next_interarrival(self, rng: np.random.Generator) -> float:
        return float(rng.choice(self.samples))


def arrival_from_config(process: str, rate_per_hour: float, deterministic_interarrival: Optional[float]) -> OrderArrivalProcess:
    if process == "deterministic" and deterministic_interarrival:
        return DeterministicArrival(deterministic_interarrival)
    return PoissonOrderArrival(rate_per_hour=rate_per_hour)


__all__ = [
    "OrderArrivalProcess",
    "PoissonOrderArrival",
    "DeterministicArrival",
    "EmpiricalArrival",
    "arrival_from_config",
]
