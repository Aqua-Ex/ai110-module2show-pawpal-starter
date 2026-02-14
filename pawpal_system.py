from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecurrencePattern(Enum):
    """How often a task should be done."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


@dataclass
class TimeWindow:
    """Represents a time window within a day."""
    start: time
    end: time

    def __post_init__(self):
        """Validate that start comes before end."""
        if self.start >= self.end:
            raise ValueError(f"Start time {self.start} must be before end time {self.end}")

    def contains(self, t: time) -> bool:
        """Check if a specific time falls within this window."""
        return self.start <= t <= self.end

    def overlaps(self, other: "TimeWindow") -> bool:
        """Check if this window overlaps with another window."""
        return not (self.end <= other.start or other.end <= self.start)

    def duration_minutes(self) -> int:
        """Calculate duration of this window in minutes."""
        start_dt = datetime.combine(datetime.today(), self.start)
        end_dt = datetime.combine(datetime.today(), self.end)
        delta = end_dt - start_dt
        return int(delta.total_seconds() / 60)

    def fits_task(self, duration_minutes: int) -> bool:
        """Check if a task of given duration fits in this window."""
        return self.duration_minutes() >= duration_minutes

    def split_at(self, t: time) -> tuple[Optional["TimeWindow"], Optional["TimeWindow"]]:
        """Split window at a specific time, returning (before, after) windows."""
        if not self.contains(t):
            return (self, None)

        before = TimeWindow(self.start, t) if t > self.start else None
        after = TimeWindow(t, self.end) if t < self.end else None
        return (before, after)


@dataclass
class Owner:
    id: str
    name: str
    timezone: Optional[str] = None
    availability: List[TimeWindow] = field(default_factory=list)
    pets: List["Pet"] = field(default_factory=list)

    def __post_init__(self):
        """Validate owner data."""
        if not self.id or not self.name:
            raise ValueError("Owner must have valid id and name")

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner_id = self.id

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by ID. Returns True if removed, False if not found."""
        original_count = len(self.pets)
        self.pets = [p for p in self.pets if p.id != pet_id]
        return len(self.pets) < original_count

    def get_availability(self, date: datetime) -> List[TimeWindow]:
        """Return availability windows for the given date.

        Current implementation returns daily recurring windows.
        Override this method for date-specific availability logic.
        """
        return self.availability.copy()


@dataclass
class Pet:
    id: str
    name: str
    species: Optional[str] = None
    owner_id: Optional[str] = None
    tasks: List["Task"] = field(default_factory=list)

    def __post_init__(self):
        """Validate pet data."""
        if not self.id or not self.name:
            raise ValueError("Pet must have valid id and name")

    def add_task(self, t: "Task") -> None:
        """Add a task to this pet's task list."""
        if not t.id:
            raise ValueError("Task must have a valid id")

        # Check for duplicate task IDs
        if any(task.id == t.id for task in self.tasks):
            raise ValueError(f"Task with id {t.id} already exists")

        self.tasks.append(t)
        t.pet_id = self.id

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID. Returns True if removed, False if not found."""
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < original_count

    def get_tasks_by_priority(self, priority: Priority) -> List["Task"]:
        """Get all tasks matching a specific priority."""
        return [t for t in self.tasks if t.priority == priority]

    def get_required_tasks(self) -> List["Task"]:
        """Get all required tasks."""
        return [t for t in self.tasks if t.required]


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    preferred_windows: List[TimeWindow] = field(default_factory=list)
    required: bool = False
    last_done: Optional[datetime] = None
    recurrence: RecurrencePattern = RecurrencePattern.AS_NEEDED
    pet_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)  # Task IDs that must be done before this

    def __post_init__(self):
        """Validate task data."""
        if not self.id or not self.title:
            raise ValueError("Task must have valid id and title")
        if self.duration_minutes <= 0:
            raise ValueError(f"Duration must be positive, got {self.duration_minutes}")
        if self.duration_minutes > 1440:  # 24 hours
            raise ValueError(f"Duration cannot exceed 24 hours (1440 minutes), got {self.duration_minutes}")

    def is_overdue(self) -> bool:
        """Check if this task is overdue based on last_done and recurrence."""
        if not self.last_done:
            return self.required  # Never done - overdue if required

        now = datetime.now()
        time_since = now - self.last_done

        if self.recurrence == RecurrencePattern.DAILY:
            return time_since > timedelta(days=1)
        elif self.recurrence == RecurrencePattern.WEEKLY:
            return time_since > timedelta(weeks=1)
        elif self.recurrence == RecurrencePattern.BIWEEKLY:
            return time_since > timedelta(weeks=2)
        elif self.recurrence == RecurrencePattern.MONTHLY:
            return time_since > timedelta(days=30)

        return False


@dataclass
class ScheduledTask:
    """Represents a task that has been assigned to a specific time slot."""
    task: Task
    start_time: datetime
    end_time: datetime
    reason: str = ""  # Why this task was scheduled at this time

    def __post_init__(self):
        """Validate scheduled task."""
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")

        expected_duration = timedelta(minutes=self.task.duration_minutes)
        actual_duration = self.end_time - self.start_time
        if abs((expected_duration - actual_duration).total_seconds()) > 60:  # Allow 1-minute tolerance
            raise ValueError(f"Scheduled duration {actual_duration} doesn't match task duration {expected_duration}")

    def overlaps_with(self, other: "ScheduledTask") -> bool:
        """Check if this scheduled task overlaps with another."""
        return not (self.end_time <= other.start_time or other.end_time <= self.start_time)


@dataclass
class Schedule:
    """Represents a complete schedule for a pet."""
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)
    total_minutes_scheduled: int = 0
    total_minutes_available: int = 0
    explanation: str = ""
    date: Optional[datetime] = None

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> bool:
        """Add a scheduled task if it doesn't conflict. Returns True if added."""
        # Check for conflicts
        for existing in self.scheduled_tasks:
            if scheduled_task.overlaps_with(existing):
                return False

        self.scheduled_tasks.append(scheduled_task)
        self.total_minutes_scheduled += scheduled_task.task.duration_minutes
        return True

    def get_conflicts(self) -> List[tuple[ScheduledTask, ScheduledTask]]:
        """Find all pairs of conflicting scheduled tasks."""
        conflicts = []
        for i, task1 in enumerate(self.scheduled_tasks):
            for task2 in self.scheduled_tasks[i+1:]:
                if task1.overlaps_with(task2):
                    conflicts.append((task1, task2))
        return conflicts

    def sort_by_time(self) -> None:
        """Sort scheduled tasks by start time."""
        self.scheduled_tasks.sort(key=lambda st: st.start_time)

    def get_utilization_rate(self) -> float:
        """Get the percentage of available time that's been scheduled."""
        if self.total_minutes_available == 0:
            return 0.0
        return (self.total_minutes_scheduled / self.total_minutes_available) * 100


class Scheduler:
    """Core scheduling engine: produces a schedule and explains decisions."""

    def __init__(self):
        """Initialize scheduler with state tracking."""
        self.last_schedule: Optional[Schedule] = None
        self.decision_log: List[str] = []

    def generate_schedule(
        self,
        owner: Owner,
        pet: Pet,
        date: datetime,
        available_windows: Optional[List[TimeWindow]] = None
    ) -> Schedule:
        """Generate a schedule for a pet on a given date.

        Args:
            owner: The pet owner
            pet: The pet to schedule tasks for
            date: The date to schedule for
            available_windows: Specific time windows available (uses owner.get_availability if None)

        Returns:
            A Schedule object with scheduled and unscheduled tasks
        """
        self.decision_log = []

        # Get available time windows
        if available_windows is None:
            available_windows = owner.get_availability(date)

        total_available = sum(w.duration_minutes() for w in available_windows)

        # Create schedule
        schedule = Schedule(
            date=date,
            total_minutes_available=total_available
        )

        # Score and sort tasks
        scored_tasks = [(self.score_task(t), t) for t in pet.tasks]
        scored_tasks.sort(reverse=True, key=lambda x: x[0])

        self._log(f"Scheduling {len(pet.tasks)} tasks for {pet.name} on {date.date()}")
        self._log(f"Available windows: {len(available_windows)}, Total minutes: {total_available}")

        # Try to schedule each task
        for score, task in scored_tasks:
            scheduled = self._try_schedule_task(task, schedule, available_windows, date)
            if scheduled:
                self._log(f"[SCHEDULED] {task.title} (score: {score:.2f}, priority: {task.priority.value})")
            else:
                schedule.unscheduled_tasks.append(task)
                self._log(f"[SKIPPED] {task.title} (score: {score:.2f})")

        schedule.sort_by_time()
        schedule.explanation = "\n".join(self.decision_log)
        self.last_schedule = schedule

        return schedule

    def _try_schedule_task(
        self,
        task: Task,
        schedule: Schedule,
        available_windows: List[TimeWindow],
        date: datetime
    ) -> bool:
        """Try to schedule a single task. Returns True if successful."""
        # Check dependencies
        if task.dependencies:
            for dep_id in task.dependencies:
                if not any(st.task.id == dep_id for st in schedule.scheduled_tasks):
                    self._log(f"  → Skipping {task.title}: dependency {dep_id} not scheduled yet")
                    return False

        # Try preferred windows first
        for window in task.preferred_windows:
            if self._schedule_in_window(task, window, schedule, date):
                return True

        # Try any available window
        for window in available_windows:
            if self._schedule_in_window(task, window, schedule, date):
                return True

        return False

    def _schedule_in_window(
        self,
        task: Task,
        window: TimeWindow,
        schedule: Schedule,
        date: datetime
    ) -> bool:
        """Try to schedule a task in a specific window."""
        if not window.fits_task(task.duration_minutes):
            return False

        start_dt = datetime.combine(date.date(), window.start)
        end_dt = start_dt + timedelta(minutes=task.duration_minutes)

        # Make sure we don't exceed the window
        window_end = datetime.combine(date.date(), window.end)
        if end_dt > window_end:
            return False

        reason = f"Priority: {task.priority.value}"
        if task.required:
            reason += ", Required"
        if task.is_overdue():
            reason += ", Overdue"

        scheduled_task = ScheduledTask(
            task=task,
            start_time=start_dt,
            end_time=end_dt,
            reason=reason
        )

        return schedule.add_scheduled_task(scheduled_task)

    def score_task(self, t: Task) -> float:
        """Return a numeric score for task ordering/selection.

        Higher scores = higher priority for scheduling.
        Scoring factors:
        - Priority level (critical=4, high=3, medium=2, low=1)
        - Required tasks get +2 bonus
        - Overdue tasks get +1 bonus
        - Recently done tasks get penalty
        """
        score = 0.0

        # Priority scoring
        priority_scores = {
            Priority.CRITICAL: 4.0,
            Priority.HIGH: 3.0,
            Priority.MEDIUM: 2.0,
            Priority.LOW: 1.0
        }
        score += priority_scores.get(t.priority, 2.0)

        # Required bonus
        if t.required:
            score += 2.0

        # Overdue bonus
        if t.is_overdue():
            score += 1.0

        # Recency penalty (if done recently, lower priority)
        if t.last_done:
            hours_since = (datetime.now() - t.last_done).total_seconds() / 3600
            if hours_since < 6:
                score -= 1.0  # Done very recently
            elif hours_since < 12:
                score -= 0.5  # Done somewhat recently

        return score

    def explain_decision(self) -> str:
        """Explain why the scheduler chose the produced plan."""
        if not self.last_schedule:
            return "No schedule has been generated yet."

        return self.last_schedule.explanation

    def _log(self, message: str) -> None:
        """Add a message to the decision log."""
        self.decision_log.append(message)
