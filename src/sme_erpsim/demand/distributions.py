"""Arrival and processing distributions."""
from __future__ import annotations

from typing import Callable
import numpy as np


def exponential(mean: float) -> Callable[[np.random.Generator], float]:
    return lambda rng: float(rng.exponential(mean))


def deterministic(value: float) -> Callable[[np.random.Generator], float]:
    return lambda rng: float(value)


def triangular(low: float, mode: float, high: float) -> Callable[[np.random.Generator], float]:
    return lambda rng: float(rng.triangular(low, mode, high))


__all__ = ["exponential", "deterministic", "triangular"]
