# SME-ERPSim: Copilot Instructions

## Project Overview
SME-ERPSim is a discrete-event simulation engine for SME ERP processes (order-to-cash, procure-to-pay, make-to-stock). Built on **SimPy** for event scheduling and **Pydantic** for configuration validation. The architecture separates concerns: process models define workflow graphs, resources model capacity constraints, demand processes generate arrivals, and monitors collect events/KPIs.

## Architecture & Data Flow

### Core Components (5-layer architecture)
1. **Process Layer** (`process/model.py`): Activities and transitions as a NetworkX directed graph. `Activity` = work unit with duration function; `ProcessModel.choose_next()` handles probabilistic routing.
2. **Resources** (`resources/`): `WorkerPool` and `WorkCenter` wrap SimPy resources. Call `.bind(env)` to instantiate SimPy primitives.
3. **Demand** (`demand/processes.py`): `OrderArrivalProcess` subclasses (Poisson, deterministic, empirical) generate interarrival times via `.next_interarrival(rng)`.
4. **Simulation Engine** (`simulation/engine.py`): Orchestrates SimPy environment. `_arrival_generator` spawns orders; `_run_order` walks process graph and requests resources with `yield req`.
5. **Monitoring/KPI** (`simulation/monitors.py`, `kpi/`): `EventMonitor.record()` collects typed events; KPI functions compute lead times, throughput from pandas DataFrames.

### Key Patterns
- **Duration Functions**: All activity durations are `Callable[[np.random.Generator], float]`. Use closures to capture config values: `lambda rng, m=act.mean_duration: m`.
- **Resource Binding**: Resources decouple from SimPy until runtime. `SimulationEngine._bind_resources()` calls `.bind(self.env)` to create SimPy Resource objects stored in a dict.
- **Event-Driven Monitoring**: Engine calls `_notify(event)` to broadcast typed events (`OrderArrival`, `StartActivity`, `EndActivity`, `OrderCompletion`) to all registered monitors. Events have structured `data` dict and timestamp.
- **Process Graph Traversal**: `_run_order` iterates through activities via `choose_next()` which respects transition probabilities. Loop terminates when `choose_next` returns `None`.

## Configuration System

### YAML/JSON Schema (validated by Pydantic)
- **ProcessConfig**: `activities` (name, mean_duration, resource), `transitions` (list of [source, target] pairs), `start_activity` (must exist).
- **ResourceConfig**: `name`, `capacity` (>0), `kind` ("worker" or "machine").
- **DemandConfig**: `process` ("poisson" or "deterministic"), `rate_per_hour`, optional `deterministic_interarrival`.
- **SimulationConfig**: Top-level wrapper with `duration_hours`, `random_seed`.

### Loading Pattern
```python
cfg = load_simulation_config("path.yaml")  # Pydantic validation happens here
engine = SimulationEngine.from_config(cfg)
```
`from_config` factory method constructs `ProcessModel`, instantiates resources, and creates arrival process via `arrival_from_config()`.

## Development Workflows

### Running Simulations
```bash
# CLI with config file
sme-erpsim run-config examples/make_to_stock.yaml

# Programmatic API
python -c "from sme_erpsim import SimulationEngine; ..."
```

### Testing
```bash
pytest                    # Run all tests
pytest tests/test_simulation_engine.py -v
```
Tests instantiate `ProcessModel`, `WorkerPool`, `SimulationEngine` directly. Use `DeterministicArrival` for reproducible scenarios. Verify `monitor.count_completed()` and `monitor.lead_times()`.

### Package Installation
```bash
pip install .             # Installs as editable if needed: pip install -e .
```
Entry point `sme-erpsim` defined in `pyproject.toml` → `sme_erpsim.cli:main`.

## Common Extension Points

### Adding New Activity Types
Subclass `Activity` or add fields to `ActivityConfig`. Update `from_config` factory to handle new parameters. Duration functions can embed logic: `lambda rng: rng.uniform(1, 3) if condition else 2.0`.

### Custom Arrival Processes
Subclass `OrderArrivalProcess` in `demand/processes.py`, implement `next_interarrival(rng)`. Register in `arrival_from_config()` for YAML support.

### New Resource Types
Follow `WorkerPool` pattern: store config, implement `.bind(env)` returning SimPy resource. `WorkCenter` wraps multiple `Machine` objects (see `resources/machines.py`).

### ERP Data Integration
Use `io/csv_adapter.py` functions to load `SalesOrder`, `PurchaseOrder`, `InventoryTransaction` from CSV. Convert to empirical distributions for calibration (see `calibration/parameter_estimation.py`).

## Key Conventions

- **Random Number Generation**: Always pass `np.random.Generator` (not global `random`). Engine instantiates `self.rng = np.random.default_rng(random_seed)` for reproducibility.
- **Event Typing**: Events are dataclasses with `timestamp`, `event_type` string, and `data` dict. Typed subclasses (`StartActivity`, `EndActivity`) add order_id/activity fields.
- **Resource Requests**: Use `with resource.request() as req: yield req` pattern inside generator functions. This blocks until resource available.
- **Graph Validation**: `add_transition` requires both activities exist. `start_activity` must be set before running simulation.
- **Pandas for Reporting**: `EventMonitor.event_log()` returns DataFrame. KPI functions expect columns: `type`, `time`, `order_id`, `activity`, `duration`.

## JOSS Submission Context
This project targets Journal of Open Source Software submission (see `paper/paper.md`, `JOSS_SUBMISSION_INSTRUCTIONS.md`). When editing paper content:
- Maintain academic tone with citations to simulation texts (Law, Banks, Shannon)
- Emphasize SME focus and ERP-friendly abstractions as differentiators
- Examples must be reproducible from `examples/` directory
- Update `paper.md` with author/affiliation info before submission

## Files Not to Modify Directly
- `src/sme_erpsim.egg-info/`: Auto-generated during install
- `**/__pycache__/`: Python bytecode cache
