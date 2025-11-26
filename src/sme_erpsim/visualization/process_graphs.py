"""Process graph visualization."""
from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from ..process.model import ProcessModel


def plot_process_model(model: ProcessModel) -> None:
    pos = nx.spring_layout(model.graph)
    labels = {n: n for n in model.graph.nodes}
    nx.draw(model.graph, pos, with_labels=True, labels=labels, node_color="#4C72B0", node_size=1500, font_color="white")
    plt.title(model.name)
    plt.show()
