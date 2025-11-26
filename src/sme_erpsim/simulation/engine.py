"""Simulation engine built on SimPy."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import itertools
import simpy
import numpy as np

from ..process.model import ProcessModel, Activity
from ..demand.processes import OrderArrivalProcess
from ..resources.workers import WorkerPool
from ..resources.machines import WorkCenter, Machine
from .events import (
    Event,
    OrderArrival,
    OrderCompletion,
    StartActivity,
    EndActivity,
)
from .monitors import EventMonitor
from ..config.schema import SimulationConfig
from ..config.loaders import load_simulation_config
from ..demand.processes import arrival_from_config
from ..process.model import Activity as ModelActivity


@dataclass
class SimulationResult:
    events: List[Event]
    monitors: List[EventMonitor]


class SimulationEngine:
    """High-level API that wraps SimPy to execute a process model."""

    def __init__(
        self,
        process_model: ProcessModel,
        arrival_process: OrderArrivalProcess,
        resources: Optional[Dict[str, object]] = None,
        monitors: Optional[List[EventMonitor]] = None,
        random_seed: Optional[int] = None,
    ):
        self.process_model = process_model
        self.arrival_process = arrival_process
        self.resources = resources or {}
        self.monitors = monitors or []
        self.random_seed = random_seed
        self.env = simpy.Environment()
        self.rng = np.random.default_rng(random_seed)
        self._order_counter = itertools.count()

    @classmethod
    def from_config(cls, config: SimulationConfig) -> "SimulationEngine":
        pm = ProcessModel(config.process.name)
        res_map: Dict[str, object] = {}
        for act in config.process.activities:
            activity = ModelActivity(act.name, duration=lambda rng, m=act.mean_duration: m, resource=act.resource)
            pm.add_activity(activity, is_start=(act.name == config.process.start_activity))
        for src, dst in config.process.transitions:
            pm.add_transition(src, dst)
        for r in config.resources:
            if r.kind == "worker":
                res_map[r.name] = WorkerPool(r.name, r.capacity)
            else:
                res_map[r.name] = WorkCenter(r.name, machines=[Machine(r.name, capacity=r.capacity)])
        arrival = arrival_from_config(
            process=config.demand.process,
            rate_per_hour=config.demand.rate_per_hour,
            deterministic_interarrival=config.demand.deterministic_interarrival,
        )
        return cls(pm, arrival_process=arrival, resources=res_map, random_seed=config.random_seed)

    def _bind_resources(self) -> Dict[str, simpy.Resource]:
        bound = {}
        for name, resource in self.resources.items():
            if hasattr(resource, "bind"):
                bound[name] = resource.bind(self.env)
        return bound

    def run(self, until: float) -> SimulationResult:
        bound_resources = self._bind_resources()
        self.env.process(self._arrival_generator(bound_resources))
        self.env.run(until=until)
        return SimulationResult(events=list(itertools.chain.from_iterable(m.events for m in self.monitors)), monitors=self.monitors)

    def _arrival_generator(self, bound_resources: Dict[str, simpy.Resource]):
        while True:
            inter = self.arrival_process.next_interarrival(self.rng)
            yield self.env.timeout(inter)
            order_id = f"O{next(self._order_counter)}"
            arrival_event = OrderArrival(timestamp=self.env.now, event_type="order_arrival", data={"order_id": order_id}, order_id=order_id)
            self._notify(arrival_event)
            self.env.process(self._run_order(order_id, bound_resources))

    def _run_order(self, order_id: str, bound_resources: Dict[str, simpy.Resource]):
        current = self.process_model.start_activity
        if current is None:
            raise RuntimeError("Process model has no start activity")
        while current is not None:
            activity: Activity = self.process_model.graph.nodes[current]["activity"]
            if activity.resource:
                resource = bound_resources.get(activity.resource)
                with resource.request() as req:
                    yield req
                    yield from self._execute_activity(order_id, activity)
            else:
                yield from self._execute_activity(order_id, activity)
            next_act = self.process_model.choose_next(current, self.rng)
            current = next_act.name if next_act else None
        completion = OrderCompletion(timestamp=self.env.now, event_type="order_complete", data={"order_id": order_id}, order_id=order_id)
        self._notify(completion)

    def _execute_activity(self, order_id: str, activity: Activity):
        start_event = StartActivity(
            timestamp=self.env.now,
            event_type="start_activity",
            data={"order_id": order_id, "activity": activity.name},
            order_id=order_id,
            activity=activity.name,
        )
        self._notify(start_event)
        duration = activity.duration(self.rng)
        yield self.env.timeout(duration)
        end_event = EndActivity(
            timestamp=self.env.now,
            event_type="end_activity",
            data={"order_id": order_id, "activity": activity.name, "duration": duration},
            order_id=order_id,
            activity=activity.name,
        )
        self._notify(end_event)

    def _notify(self, event: Event) -> None:
        for m in self.monitors:
            m.record(event)
