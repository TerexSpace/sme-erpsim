"""Config loaders for YAML/JSON files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import yaml

from .schema import SimulationConfig


def _load_raw(path: str) -> Any:
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(path)
    text = path_obj.read_text()
    if path_obj.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def load_simulation_config(path: str) -> SimulationConfig:
    """Load and validate a SimulationConfig from YAML or JSON."""
    raw = _load_raw(path)
    return SimulationConfig.model_validate(raw)


__all__ = ["load_simulation_config"]
