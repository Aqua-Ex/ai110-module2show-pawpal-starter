from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Owner:
    id: str
    name: str
    timezone: Optional[str] = None
    availability: List["TimeWindow"] = field(default_factory=list)

    def get_availability(self, date: datetime) -> List["TimeWindow"]:
        """Return availability windows for the given date."""
        raise NotImplementedError()


@dataclass
class Pet:
    id: str
    name: str
    species: Optional[str] = None
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, t: "Task") -> None:
        raise NotImplementedError()

    def remove_task(self, task_id: str) -> None:
        raise NotImplementedError()


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    preferred_windows: List["TimeWindow"] = field(default_factory=list)
    required: bool = False
    last_done: Optional[datetime] = None


class Scheduler:
    """Core scheduling engine: produces a schedule and explains decisions."""

    def generate_schedule(self, owner: Owner, pet: Pet, available_minutes: int):
        """Return a Schedule (not implemented in skeleton)."""
        raise NotImplementedError()

    def explain_decision(self) -> str:
        """Explain why the scheduler chose the produced plan."""
        raise NotImplementedError()

    def score_task(self, t: Task) -> float:
        """Return a numeric score for task ordering/selection."""
        raise NotImplementedError()


# Minimal helper type used in annotations. Implementations omitted in this skeleton.
@dataclass
class TimeWindow:
    start: time
    end: time

    def contains(self, t: time) -> bool:
        raise NotImplementedError()
