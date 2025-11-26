"""Scenario helper utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Scenario:
    """Container for scenario parameters to override defaults."""

    name: str
    parameters: Dict[str, Any]

    def apply(self, base: Dict[str, Any]) -> Dict[str, Any]:
        merged = base.copy()
        merged.update(self.parameters)
        return merged
