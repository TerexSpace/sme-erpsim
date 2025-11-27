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
    """
    Represents a business process as a directed graph of activities and transitions.

    The model uses a NetworkX DiGraph where:
    - Nodes represent Activities (work units).
    - Edges represent Transitions (flow of control).

    Attributes:
        name (str): Name of the process.
        graph (nx.DiGraph): The underlying graph structure.
        start_activity (Optional[str]): The name of the entry point activity.
    """

    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()
        self.start_activity: Optional[str] = None

    def add_activity(self, activity: Activity, is_start: bool = False) -> None:
        """
        Add an activity node to the process graph.

        Args:
            activity (Activity): The activity object to add.
            is_start (bool): If True, marks this activity as the process entry point.
        """
        self.graph.add_node(activity.name, activity=activity)
        if is_start:
            self.start_activity = activity.name

    def add_transition(self, source: str, target: str, probability: float = 1.0) -> None:
        """
        Add a directed transition between two existing activities.

        Args:
            source (str): Name of the source activity.
            target (str): Name of the target activity.
            probability (float): Probability of taking this path (default 1.0).
                Probabilities for outgoing edges should sum to 1.0.

        Raises:
            ValueError: If source or target activities are not in the graph.
        """
        if source not in self.graph or target not in self.graph:
            raise ValueError("Activities must be added before creating transitions")
        self.graph.add_edge(source, target, transition=Transition(source, target, probability))

    def next_activities(self, current: str) -> List[Activity]:
        successors = list(self.graph.successors(current))
        return [self.graph.nodes[s]["activity"] for s in successors]

    def choose_next(self, current: str, rng: np.random.Generator) -> Optional[Activity]:
        """
        Select the next activity based on transition probabilities.

        Args:
            current (str): The name of the current activity.
            rng (np.random.Generator): Random number generator for probabilistic routing.

        Returns:
            Optional[Activity]: The next activity object, or None if no transitions exist (end of process).
        """
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
