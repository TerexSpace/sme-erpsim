# SME-ERPSim: A discrete-event simulation engine for SME ERP processes

SME-ERPSim is a research-grade Python package for simulating order-to-cash, procure-to-pay, and light make-to-stock / assemble-to-order flows. It targets small and medium enterprises (SMEs) that need fast what-if analysis without heavyweight ERP modules.

## Statement of need
SMEs often lack the resources to run commercial simulation suites or complex ERP planning modules. SME-ERPSim offers a lightweight, configurable, and validated simulator that ingests ERP exports, produces event traces, and yields actionable KPIs such as lead time, fill rate, and resource utilization.

## Features
- Domain abstractions: sales orders, purchase orders, inventory transactions, workers, machines, work centers.
- Configurable via Python API or validated YAML/JSON.
- Discrete-event core powered by SimPy with domain-specific events.
- KPI and reporting helpers; simple parameter estimation from ERP logs.
- CSV adapters to integrate with ERP exports.
- Visualization utilities for Gantt charts and process graphs.

## Installation
```bash
pip install .
```

## Quick start
```python
from sme_erpsim.process.model import Activity, ProcessModel
from sme_erpsim.resources.workers import WorkerPool
from sme_erpsim.demand.processes import PoissonOrderArrival
from sme_erpsim.simulation.engine import SimulationEngine
from sme_erpsim.simulation.monitors import EventMonitor

process = ProcessModel("order_to_cash")
procurement = Activity("receive_order", duration=lambda rng: 1.0)
fulfillment = Activity("fulfill", duration=lambda rng: 2.0)
process.add_activity(procurement, is_start=True)
process.add_activity(fulfillment)
process.add_transition("receive_order", "fulfill")

workers = WorkerPool("ops", capacity=2)
arrival = PoissonOrderArrival(rate_per_hour=4)
monitor = EventMonitor()

engine = SimulationEngine(
    process_model=process,
    arrival_process=arrival,
    resources={"ops": workers},
    monitors=[monitor],
    random_seed=42,
)
engine.run(until=8.0)

print("Orders processed:", monitor.count_completed())
print("Lead times:", monitor.lead_times())
```

## Examples
- `examples/make_to_stock.yaml`: YAML configuration for a make-to-stock flow.
- `examples/make_to_order.yaml`: YAML configuration for a make-to-order flow.
- `examples/small_trading_company.ipynb`: Notebook outline showing data ingestion, scenario definition, simulation, and reporting.

Run the CLI:
```bash
sme-erpsim run-config examples/make_to_stock.yaml
```

## Testing
```bash
pytest
```

## License
MIT License (see `LICENSE`).
