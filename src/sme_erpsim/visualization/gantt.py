"""Simple Gantt chart visualization."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_gantt(event_log: pd.DataFrame) -> None:
    df = event_log[event_log["type"].isin(["start_activity", "end_activity"])]
    orders = df["order_id"].unique()
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = plt.cm.tab20.colors
    for idx, oid in enumerate(orders):
        starts = df[(df["order_id"] == oid) & (df["type"] == "start_activity")].set_index("activity")["time"]
        ends = df[(df["order_id"] == oid) & (df["type"] == "end_activity")].set_index("activity")["time"]
        for act in starts.index.intersection(ends.index):
            ax.barh(idx, ends[act] - starts[act], left=starts[act], color=colors[idx % len(colors)], edgecolor="black")
    ax.set_yticks(range(len(orders)))
    ax.set_yticklabels(orders)
    ax.set_xlabel("Time")
    ax.set_title("Activity Gantt Chart")
    plt.tight_layout()
    plt.show()
