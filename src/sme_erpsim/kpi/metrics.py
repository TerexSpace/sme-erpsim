"""KPI computation utilities."""
from __future__ import annotations

from typing import List, Dict
import pandas as pd


def compute_lead_times(event_log: pd.DataFrame) -> List[float]:
    arrivals = event_log[event_log["type"] == "order_arrival"].set_index("order_id")["time"]
    completions = event_log[event_log["type"] == "order_complete"].set_index("order_id")["time"]
    intersect = arrivals.index.intersection(completions.index)
    return list((completions.loc[intersect] - arrivals.loc[intersect]).astype(float))


def compute_activity_durations(event_log: pd.DataFrame) -> Dict[str, float]:
    durations = event_log[event_log["type"] == "end_activity"].groupby("activity")["duration"].mean()
    return durations.to_dict()


def compute_throughput(event_log: pd.DataFrame, horizon: float) -> float:
    completed = event_log[event_log["type"] == "order_complete"]
    return len(completed) / horizon if horizon > 0 else 0.0


__all__ = ["compute_lead_times", "compute_activity_durations", "compute_throughput"]
