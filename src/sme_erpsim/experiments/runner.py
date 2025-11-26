"""Experiment runner utilities."""
from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd

from ..simulation.engine import SimulationEngine
from ..kpi.reporting import build_report
from ..simulation.monitors import EventMonitor


def run_experiments(configs: List[Dict[str, Any]], builder) -> pd.DataFrame:
    """Run a set of experiments given a builder that produces SimulationEngine."""
    rows = []
    for cfg in configs:
        engine: SimulationEngine = builder(cfg)
        monitor = EventMonitor()
        engine.monitors.append(monitor)
        engine.run(until=cfg.get("duration", 8.0))
        report = build_report(monitor.event_log(), cfg.get("duration", 8.0))
        lead_mean = sum(report.lead_times) / max(len(report.lead_times), 1)
        rows.append({"config": cfg, "throughput": report.throughput_per_hour, "lead_time_mean": lead_mean})
    return pd.DataFrame(rows)
