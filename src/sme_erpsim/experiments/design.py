"""Design of experiments helpers."""
from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, List


def factor_grid(factors: Dict[str, Iterable]) -> List[Dict[str, object]]:
    keys = list(factors.keys())
    combos = []
    for vals in product(*factors.values()):
        combos.append({k: v for k, v in zip(keys, vals)})
    return combos
