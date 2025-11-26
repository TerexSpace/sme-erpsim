"""Routing policies as callables."""
from __future__ import annotations

from typing import List, Any, Callable


def fifo(queue: List[Any]) -> Any:
    return queue[0] if queue else None


def lifo(queue: List[Any]) -> Any:
    return queue[-1] if queue else None


def priority(queue: List[Any], key: Callable[[Any], int]) -> Any:
    if not queue:
        return None
    return sorted(queue, key=key)[0]


__all__ = ["fifo", "lifo", "priority"]
