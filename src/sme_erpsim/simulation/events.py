"""Domain-specific events."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Event:
    timestamp: float
    event_type: str
    data: Dict[str, Any]


@dataclass
class OrderArrival(Event):
    order_id: str


@dataclass
class StartActivity(Event):
    order_id: str
    activity: str


@dataclass
class EndActivity(Event):
    order_id: str
    activity: str


@dataclass
class OrderCompletion(Event):
    order_id: str
