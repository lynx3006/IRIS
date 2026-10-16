from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Signal(BaseModel):
    """A single observation that may indicate abnormal system behavior."""

    source: str = Field(min_length=1)
    service: str = Field(min_length=1)
    signal_type: str = Field(min_length=1)
    observed_value: float
    detected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    description: str = ""

class Incident(BaseModel):
    """A group of related signals representing a possible incident."""

    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1)
    severity: Literal["low", "medium", "high"]
    status: Literal["open", "investigating", "recovering", "closed"] = "open"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )