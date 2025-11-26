"""Process model abstractions backed by a directed graph."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

import networkx as nx
import numpy as np


DurationFunc = Callable[[np.random.Generator], float]


@dataclass
class Activity:
    """A unit of work requiring time and possibly resources."""

    name: str
    duration: DurationFunc
    resource: Optional[str] = None
    priority: int = 0


@dataclass
class Transition:
    """Directed edge between activities."""

    source: str
    target: str
    probability: float = 1.0


class ProcessModel:
    """Represents a graph of activities and transitions."""

    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()
        self.start_activity: Optional[str] = None

    def add_activity(self, activity: Activity, is_start: bool = False) -> None:
        self.graph.add_node(activity.name, activity=activity)
        if is_start:
            self.start_activity = activity.name

    def add_transition(self, source: str, target: str, probability: float = 1.0) -> None:
        if source not in self.graph or target not in self.graph:
            raise ValueError("Activities must be added before creating transitions")
        self.graph.add_edge(source, target, transition=Transition(source, target, probability))

    def next_activities(self, current: str) -> List[Activity]:
        successors = list(self.graph.successors(current))
        return [self.graph.nodes[s]["activity"] for s in successors]

    def choose_next(self, current: str, rng: np.random.Generator) -> Optional[Activity]:
        edges = list(self.graph.successors(current))
        if not edges:
            return None
        probs = [self.graph[current][succ]["transition"].probability for succ in edges]
        probs = np.array(probs, dtype=float)
        probs = probs / probs.sum()
        choice = rng.choice(edges, p=probs)
        return self.graph.nodes[choice]["activity"]

    def activities(self) -> List[Activity]:
        return [data["activity"] for _, data in self.graph.nodes(data=True)]

    def transitions(self) -> List[Transition]:
        return [data["transition"] for _, _, data in self.graph.edges(data=True)]
