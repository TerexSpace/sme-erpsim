from sme_erpsim.process.model import Activity, ProcessModel
from sme_erpsim.demand.processes import DeterministicArrival
from sme_erpsim.resources.workers import WorkerPool
from sme_erpsim.simulation.engine import SimulationEngine
from sme_erpsim.simulation.monitors import EventMonitor


def test_engine_runs_and_completes_orders():
    pm = ProcessModel("flow")
    a = Activity("a", duration=lambda rng: 0.5, resource="workers")
    b = Activity("b", duration=lambda rng: 0.5)
    pm.add_activity(a, is_start=True)
    pm.add_activity(b)
    pm.add_transition("a", "b")
    workers = WorkerPool("workers", capacity=1)
    monitor = EventMonitor()
    engine = SimulationEngine(pm, arrival_process=DeterministicArrival(1.0), resources={"workers": workers}, monitors=[monitor], random_seed=123)
    engine.run(until=3.5)
    assert monitor.count_completed() >= 2
    assert all(lt > 0 for lt in monitor.lead_times())
