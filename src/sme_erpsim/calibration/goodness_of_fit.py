"""Goodness-of-fit utilities."""
from __future__ import annotations

from typing import List, Tuple
import numpy as np

try:  # optional SciPy import
    from scipy import stats  # type: ignore
except Exception:  # pragma: no cover - fallback path
    stats = None


def ks_test(samples: List[float], dist: str = "expon") -> Tuple[float, float]:
    if stats is not None:
        d_stat, p_value = stats.kstest(samples, dist)
        return float(d_stat), float(p_value)
    # lightweight fallback: crude uniform comparison
    arr = np.array(samples)
    if len(arr) == 0:
        return 0.0, 0.5
    sorted_arr = np.sort(arr)
    cdf = np.arange(1, len(arr) + 1) / len(arr)
    d_stat = float(np.max(np.abs(cdf - sorted_arr / sorted_arr.max())))
    return d_stat, 0.5
