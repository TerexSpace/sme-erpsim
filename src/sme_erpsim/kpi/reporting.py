"""Reporting helpers for KPIs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import pandas as pd

from .metrics import compute_lead_times, compute_activity_durations, compute_throughput


@dataclass
class KPIReport:
    lead_times: list[float]
    activity_durations: Dict[str, float]
    throughput_per_hour: float

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "lead_time_mean": [pd.Series(self.lead_times).mean()],
                "throughput_per_hour": [self.throughput_per_hour],
            }
        )

    def to_markdown(self) -> str:
        return self.to_dataframe().to_markdown(index=False)


def build_report(event_log: pd.DataFrame, horizon: float) -> KPIReport:
    return KPIReport(
        lead_times=compute_lead_times(event_log),
        activity_durations=compute_activity_durations(event_log),
        throughput_per_hour=compute_throughput(event_log, horizon),
    )


__all__ = ["KPIReport", "build_report"]
