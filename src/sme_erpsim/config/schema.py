"""Configuration schemas using Pydantic for validation."""
from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class ResourceConfig(BaseModel):
    name: str
    capacity: int = Field(..., gt=0)
    kind: str = Field("worker", description="worker or machine")


class ActivityConfig(BaseModel):
    name: str
    mean_duration: float = Field(..., gt=0)
    resource: Optional[str] = None

    @field_validator("mean_duration")
    @classmethod
    def check_duration(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("mean_duration must be positive")
        return v


class ProcessConfig(BaseModel):
    name: str
    activities: List[ActivityConfig]
    transitions: List[List[str]] = Field(..., description="Pairs of source,destination names")
    start_activity: str

    @model_validator(mode="after")
    def ensure_start_exists(self) -> "ProcessConfig":
        names = {a.name for a in self.activities}
        if self.start_activity not in names:
            raise ValueError("start_activity must reference an activity")
        return self


class DemandConfig(BaseModel):
    process: str = Field("poisson", description="poisson or deterministic")
    rate_per_hour: float = Field(1.0, gt=0)
    deterministic_interarrival: Optional[float] = None


class SimulationConfig(BaseModel):
    process: ProcessConfig
    resources: List[ResourceConfig]
    demand: DemandConfig
    duration_hours: float = Field(8.0, gt=0)
    random_seed: Optional[int] = None


__all__ = [
    "ResourceConfig",
    "ActivityConfig",
    "ProcessConfig",
    "DemandConfig",
    "SimulationConfig",
]
