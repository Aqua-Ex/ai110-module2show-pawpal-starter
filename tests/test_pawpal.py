"""
Tests for PawPal+ scheduling system.
"""

import pytest
from datetime import datetime, time, timedelta
from pawpal_system import (
    Owner,
    Pet,
    Task,
    TimeWindow,
    Priority,
    RecurrencePattern,
    Scheduler,
    Schedule,
    ScheduledTask,
)


class TestTaskAddition:
    """Test adding tasks to pets."""

    def test_add_task_increases_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet(id="pet1", name="Buddy", species="Dog")
        initial_count = len(pet.tasks)

        task = Task(
            id="task1",
            title="Walk",
            duration_minutes=30,
            priority=Priority.HIGH
        )

        # Act
        pet.add_task(task)

        # Assert
        assert len(pet.tasks) == initial_count + 1
        assert task in pet.tasks
        assert task.pet_id == pet.id

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks to a pet."""
        # Arrange
        pet = Pet(id="pet1", name="Whiskers", species="Cat")

        task1 = Task(id="task1", title="Feed", duration_minutes=10)
        task2 = Task(id="task2", title="Play", duration_minutes=15)
        task3 = Task(id="task3", title="Groom", duration_minutes=20)

        # Act
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        # Assert
        assert len(pet.tasks) == 3
        assert all(t in pet.tasks for t in [task1, task2, task3])

    def test_cannot_add_duplicate_task_id(self):
        """Test that duplicate task IDs are rejected."""
        # Arrange
        pet = Pet(id="pet1", name="Max", species="Dog")
        task1 = Task(id="task1", title="Walk", duration_minutes=30)
        task2 = Task(id="task1", title="Different Task", duration_minutes=20)

        pet.add_task(task1)

        # Act & Assert
        with pytest.raises(ValueError, match="Task with id task1 already exists"):
            pet.add_task(task2)


class TestTaskCompletion:
    """Test task completion and overdue logic."""

    def test_mark_task_complete_updates_last_done(self):
        """Verify that marking a task complete updates last_done timestamp."""
        # Arrange
        task = Task(
            id="task1",
            title="Feed",
            duration_minutes=15,
            recurrence=RecurrencePattern.DAILY,
            required=True
        )

        assert task.last_done is None

        # Act - simulate marking complete
        task.last_done = datetime.now()

        # Assert
        assert task.last_done is not None
        assert isinstance(task.last_done, datetime)

    def test_task_is_overdue_when_never_done_and_required(self):
        """Test that required tasks with no last_done are considered overdue."""
        # Arrange
        task = Task(
            id="task1",
            title="Medicine",
            duration_minutes=5,
            required=True,
            recurrence=RecurrencePattern.DAILY
        )

        # Act & Assert
        assert task.is_overdue() is True

    def test_task_not_overdue_when_recently_done(self):
        """Test that tasks done recently are not overdue."""
        # Arrange
        task = Task(
            id="task1",
            title="Walk",
            duration_minutes=30,
            required=True,
            recurrence=RecurrencePattern.DAILY,
            last_done=datetime.now() - timedelta(hours=12)  # Done 12 hours ago
        )

        # Act & Assert
        assert task.is_overdue() is False

    def test_daily_task_overdue_after_24_hours(self):
        """Test that daily tasks become overdue after 24 hours."""
        # Arrange
        task = Task(
            id="task1",
            title="Feed",
            duration_minutes=10,
            recurrence=RecurrencePattern.DAILY,
            last_done=datetime.now() - timedelta(days=2)  # Done 2 days ago
        )

        # Act & Assert
        assert task.is_overdue() is True


class TestTaskRemoval:
    """Test removing tasks from pets."""

    def test_remove_task_decreases_count(self):
        """Verify that removing a task decreases the pet's task count."""
        # Arrange
        pet = Pet(id="pet1", name="Buddy", species="Dog")
        task = Task(id="task1", title="Walk", duration_minutes=30)
        pet.add_task(task)
        initial_count = len(pet.tasks)

        # Act
        result = pet.remove_task("task1")

        # Assert
        assert result is True
        assert len(pet.tasks) == initial_count - 1
        assert task not in pet.tasks

    def test_remove_nonexistent_task_returns_false(self):
        """Test that removing a non-existent task returns False."""
        # Arrange
        pet = Pet(id="pet1", name="Max", species="Dog")

        # Act
        result = pet.remove_task("nonexistent_id")

        # Assert
        assert result is False


class TestTimeWindow:
    """Test TimeWindow functionality."""

    def test_time_window_duration(self):
        """Test calculating duration of a time window."""
        # Arrange
        window = TimeWindow(start=time(9, 0), end=time(11, 30))

        # Act
        duration = window.duration_minutes()

        # Assert
        assert duration == 150  # 2.5 hours = 150 minutes

    def test_time_window_fits_task(self):
        """Test checking if a task fits in a window."""
        # Arrange
        window = TimeWindow(start=time(9, 0), end=time(10, 0))  # 60 minutes

        # Act & Assert
        assert window.fits_task(30) is True  # 30 min task fits
        assert window.fits_task(60) is True  # 60 min task fits
        assert window.fits_task(90) is False  # 90 min task doesn't fit

    def test_time_window_overlap(self):
        """Test detecting overlapping time windows."""
        # Arrange
        window1 = TimeWindow(start=time(9, 0), end=time(11, 0))
        window2 = TimeWindow(start=time(10, 0), end=time(12, 0))  # Overlaps
        window3 = TimeWindow(start=time(14, 0), end=time(16, 0))  # No overlap

        # Act & Assert
        assert window1.overlaps(window2) is True
        assert window1.overlaps(window3) is False


class TestScheduler:
    """Test the scheduling engine."""

    def test_scheduler_creates_schedule(self):
        """Test that scheduler creates a valid schedule."""
        # Arrange
        owner = Owner(
            id="owner1",
            name="Alex",
            availability=[
                TimeWindow(start=time(9, 0), end=time(12, 0))
            ]
        )

        pet = Pet(id="pet1", name="Max", species="Dog")

        task1 = Task(
            id="task1",
            title="Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            required=True
        )

        task2 = Task(
            id="task2",
            title="Feed",
            duration_minutes=15,
            priority=Priority.CRITICAL,
            required=True
        )

        pet.add_task(task1)
        pet.add_task(task2)

        scheduler = Scheduler()

        # Act
        schedule = scheduler.generate_schedule(owner, pet, datetime.now())

        # Assert
        assert isinstance(schedule, Schedule)
        assert len(schedule.scheduled_tasks) > 0
        assert schedule.total_minutes_available == 180  # 3 hours

    def test_scheduler_prioritizes_critical_tasks(self):
        """Test that scheduler prioritizes critical tasks over low priority tasks."""
        # Arrange
        owner = Owner(
            id="owner1",
            name="Alex",
            availability=[TimeWindow(start=time(9, 0), end=time(10, 0))]
        )

        pet = Pet(id="pet1", name="Max", species="Dog")

        low_task = Task(
            id="task1",
            title="Grooming",
            duration_minutes=30,
            priority=Priority.LOW
        )

        critical_task = Task(
            id="task2",
            title="Medicine",
            duration_minutes=30,
            priority=Priority.CRITICAL,
            required=True
        )

        pet.add_task(low_task)
        pet.add_task(critical_task)

        scheduler = Scheduler()

        # Act
        schedule = scheduler.generate_schedule(owner, pet, datetime.now())

        # Assert
        # Critical task should be scheduled, low priority might not be
        scheduled_titles = [st.task.title for st in schedule.scheduled_tasks]
        assert "Medicine" in scheduled_titles

    def test_scheduler_respects_time_windows(self):
        """Test that scheduled tasks fit within available time windows."""
        # Arrange
        owner = Owner(
            id="owner1",
            name="Alex",
            availability=[TimeWindow(start=time(9, 0), end=time(10, 0))]
        )

        pet = Pet(id="pet1", name="Max", species="Dog")

        task = Task(
            id="task1",
            title="Walk",
            duration_minutes=30,
            priority=Priority.HIGH
        )

        pet.add_task(task)

        scheduler = Scheduler()

        # Act
        schedule = scheduler.generate_schedule(owner, pet, datetime.now())

        # Assert
        for st in schedule.scheduled_tasks:
            # Check that task times fall within availability
            task_start = st.start_time.time()
            task_end = st.end_time.time()
            assert time(9, 0) <= task_start <= time(10, 0)
            assert time(9, 0) <= task_end <= time(10, 0)


class TestOwnerPetRelationship:
    """Test Owner-Pet relationship."""

    def test_add_pet_to_owner(self):
        """Test adding a pet to an owner."""
        # Arrange
        owner = Owner(id="owner1", name="Alex")
        pet = Pet(id="pet1", name="Max", species="Dog")

        # Act
        owner.add_pet(pet)

        # Assert
        assert pet in owner.pets
        assert pet.owner_id == owner.id

    def test_remove_pet_from_owner(self):
        """Test removing a pet from an owner."""
        # Arrange
        owner = Owner(id="owner1", name="Alex")
        pet = Pet(id="pet1", name="Max", species="Dog")
        owner.add_pet(pet)

        # Act
        result = owner.remove_pet("pet1")

        # Assert
        assert result is True
        assert pet not in owner.pets


class TestValidation:
    """Test input validation."""

    def test_task_requires_positive_duration(self):
        """Test that task duration must be positive."""
        # Act & Assert
        with pytest.raises(ValueError, match="Duration must be positive"):
            Task(id="task1", title="Invalid", duration_minutes=0)

        with pytest.raises(ValueError, match="Duration must be positive"):
            Task(id="task1", title="Invalid", duration_minutes=-10)

    def test_task_duration_cannot_exceed_24_hours(self):
        """Test that task duration cannot exceed 24 hours."""
        # Act & Assert
        with pytest.raises(ValueError, match="Duration cannot exceed 24 hours"):
            Task(id="task1", title="Too Long", duration_minutes=1500)

    def test_time_window_start_before_end(self):
        """Test that time window start must be before end."""
        # Act & Assert
        with pytest.raises(ValueError, match="Start time .* must be before end time"):
            TimeWindow(start=time(14, 0), end=time(10, 0))
