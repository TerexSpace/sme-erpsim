import pytest
import numpy as np
from sme_erpsim.process.model import Activity, ProcessModel
from sme_erpsim.demand.processes import DeterministicArrival, PoissonOrderArrival
from sme_erpsim.resources.workers import WorkerPool
from sme_erpsim.simulation.engine import SimulationEngine
from sme_erpsim.simulation.monitors import EventMonitor

def test_resource_contention():
    """
    Test that limited resources cause queuing (longer lead times).
    Scenario:
    - Activity takes 1.0 hour.
    - Arrivals every 0.5 hours (Demand > Capacity).
    - 1 Worker.
    - Run for 10 hours.
    - Expected: ~20 arrivals, but only ~10 completions (since capacity is 1/hr).
    """
    pm = ProcessModel("bottleneck")
    # Activity takes exactly 1.0 hour
    act = Activity("work", duration=lambda rng: 1.0, resource="worker")
    pm.add_activity(act, is_start=True)
    
    # Arrivals every 0.5 hours
    arrival = DeterministicArrival(interarrival_time=0.5)
    
    # 1 Worker
    workers = WorkerPool("worker", capacity=1)
    
    monitor = EventMonitor()
    engine = SimulationEngine(
        pm, 
        arrival_process=arrival, 
        resources={"worker": workers}, 
        monitors=[monitor], 
        random_seed=42
    )
    
    # Run for 10 hours
    engine.run(until=10.0)
    
    # Check results
    completed = monitor.count_completed()
    # Max theoretical capacity = 10 hours / 1.0 hr/job = 10 jobs
    # Plus maybe one in progress or just finished.
    assert completed <= 11 
    assert completed >= 9
    
    # Arrivals should be around 20 (10 / 0.5)
    # We can check arrivals from the event log
    df = monitor.event_log()
    arrivals = len(df[df["type"] == "order_arrival"])
    assert arrivals >= 19

def test_probabilistic_routing():
    """
    Test that routing follows defined probabilities.
    Scenario:
    - Start -> (30%) PathA
    - Start -> (70%) PathB
    - Run many orders, check ratio.
    """
    pm = ProcessModel("split")
    start = Activity("start", duration=lambda rng: 0.0)
    path_a = Activity("path_a", duration=lambda rng: 0.0)
    path_b = Activity("path_b", duration=lambda rng: 0.0)
    
    pm.add_activity(start, is_start=True)
    pm.add_activity(path_a)
    pm.add_activity(path_b)
    
    pm.add_transition("start", "path_a", probability=0.3)
    pm.add_transition("start", "path_b", probability=0.7)
    
    # Fast arrivals to get sample size
    arrival = DeterministicArrival(interarrival_time=0.01)
    monitor = EventMonitor()
    
    engine = SimulationEngine(
        pm, 
        arrival_process=arrival, 
        monitors=[monitor], 
        random_seed=12345
    )
    
    engine.run(until=10.0) # ~1000 orders
    
    df = monitor.event_log()
    # Count how many times 'path_a' and 'path_b' were started
    starts_a = len(df[(df["type"] == "start_activity") & (df["activity"] == "path_a")])
    starts_b = len(df[(df["type"] == "start_activity") & (df["activity"] == "path_b")])
    total = starts_a + starts_b
    
    assert total > 0
    ratio_a = starts_a / total
    
    # Check if ratio is close to 0.3 (allow some variance)
    assert 0.25 < ratio_a < 0.35

def test_deterministic_timing():
    """
    Test exact timing of events.
    Scenario:
    - Arrival at t=1.0
    - Activity duration = 2.0
    - Completion should be at t=3.0
    """
    pm = ProcessModel("fixed")
    act = Activity("process", duration=lambda rng: 2.0)
    pm.add_activity(act, is_start=True)
    
    # First arrival at 1.0 (since next_interarrival is called at t=0)
    arrival = DeterministicArrival(interarrival_time=1.0)
    
    monitor = EventMonitor()
    engine = SimulationEngine(
        pm, 
        arrival_process=arrival, 
        monitors=[monitor], 
        random_seed=42
    )
    
    engine.run(until=3.5)
    
    df = monitor.event_log()
    
    # First order
    o0_arrival = df[(df["type"] == "order_arrival") & (df["order_id"] == "O0")].iloc[0]["time"]
    o0_complete = df[(df["type"] == "order_complete") & (df["order_id"] == "O0")].iloc[0]["time"]
    
    assert o0_arrival == 1.0
    assert o0_complete == 3.0
