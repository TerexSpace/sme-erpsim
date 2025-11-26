"""Command-line interface for SME-ERPSim."""
from __future__ import annotations

import argparse

from .config.loaders import load_simulation_config
from .simulation.engine import SimulationEngine
from .simulation.monitors import EventMonitor
from .kpi.reporting import build_report


def main() -> None:
    parser = argparse.ArgumentParser(description="SME-ERPSim CLI")
    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run-config", help="Run a simulation from config file")
    run_cmd.add_argument("path", help="Path to YAML/JSON config")

    args = parser.parse_args()
    if args.command == "run-config":
        cfg = load_simulation_config(args.path)
        engine = SimulationEngine.from_config(cfg)
        monitor = EventMonitor()
        engine.monitors.append(monitor)
        engine.run(until=cfg.duration_hours)
        report = build_report(monitor.event_log(), cfg.duration_hours)
        print(report.to_markdown())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
