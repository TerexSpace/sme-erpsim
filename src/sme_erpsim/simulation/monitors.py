"""Monitors for collecting events and KPIs."""
from __future__ import annotations

from typing import List, Dict
import pandas as pd

from .events import Event, OrderArrival, OrderCompletion


class EventMonitor:
    """Collects events into a list for downstream analysis."""

    def __init__(self) -> None:
        self.events: List[Event] = []
        self.arrival_times: Dict[str, float] = {}
        self.completion_times: Dict[str, float] = {}

    def record(self, event: Event) -> None:
        self.events.append(event)
        if isinstance(event, OrderArrival):
            self.arrival_times[event.order_id] = event.timestamp
        if isinstance(event, OrderCompletion):
            self.completion_times[event.order_id] = event.timestamp

    def event_log(self) -> pd.DataFrame:
        return pd.DataFrame([{ "time": e.timestamp, "type": e.event_type, **e.data} for e in self.events])

    def count_completed(self) -> int:
        return len(self.completion_times)

    def lead_times(self) -> List[float]:
        times = []
        for oid, start in self.arrival_times.items():
            if oid in self.completion_times:
                times.append(self.completion_times[oid] - start)
        return times
