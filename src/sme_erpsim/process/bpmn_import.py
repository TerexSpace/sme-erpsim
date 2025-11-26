"""Minimal BPMN-like import to create a ProcessModel."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from .model import ProcessModel, Activity


def from_json(path: str) -> ProcessModel:
    """Load a BPMN-like JSON structure.

    Expected structure:
    {
      "name": "...",
      "activities": [{"name": "a", "mean_duration": 1.0}],
      "transitions": [["a", "b"]],
      "start": "a"
    }
    """
    data = json.loads(Path(path).read_text())
    return from_dict(data)


def from_dict(data: Dict[str, Any]) -> ProcessModel:
    process = ProcessModel(data["name"])
    for a in data["activities"]:
        activity = Activity(name=a["name"], duration=lambda rng, m=a["mean_duration"]: m)
        process.add_activity(activity, is_start=(a["name"] == data["start"]))
    for src, dst in data.get("transitions", []):
        process.add_transition(src, dst, probability=1.0)
    return process


__all__ = ["from_json", "from_dict"]
