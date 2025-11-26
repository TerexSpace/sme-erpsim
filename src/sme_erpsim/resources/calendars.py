"""Calendars for working time."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Calendar:
    """Simple shift calendar based on daily windows."""

    working_windows: List[Tuple[float, float]]

    def is_working(self, time: float) -> bool:
        day_time = time % 24.0
        return any(start <= day_time < end for start, end in self.working_windows)


DEFAULT_CALENDAR = Calendar(working_windows=[(0, 24)])

__all__ = ["Calendar", "DEFAULT_CALENDAR"]
