"""Parameter estimation from ERP logs."""
from __future__ import annotations

from typing import List
import numpy as np


def estimate_service_time(samples: List[float]) -> dict:
    arr = np.array(samples, dtype=float)
    return {"mean": float(arr.mean()), "std": float(arr.std(ddof=1) if len(arr) > 1 else 0.0)}


def estimate_arrival_rate(timestamps: List[float]) -> float:
    if len(timestamps) < 2:
        return 0.0
    span = max(timestamps) - min(timestamps)
    return len(timestamps) / span if span > 0 else 0.0
