#!/usr/bin/env python3
"""
PawPal+ Testing Ground
Demonstrates the scheduling system with sample data.
"""

from datetime import datetime, time
from pawpal_system import (
    Owner,
    Pet,
    Task,
    TimeWindow,
    Priority,
    RecurrencePattern,
    Scheduler,
)


def main():
    print("=" * 60)
    print("PawPal+ Schedule Generator - Testing Ground")
    print("=" * 60)
    print()

    # Create an owner with availability windows
    owner = Owner(
        id="owner1",
        name="Alex",
        timezone="America/New_York",
        availability=[
            TimeWindow(start=time(7, 0), end=time(9, 0)),    # Morning: 7-9 AM
            TimeWindow(start=time(12, 0), end=time(13, 0)),  # Lunch: 12-1 PM
            TimeWindow(start=time(17, 0), end=time(20, 0)),  # Evening: 5-8 PM
        ]
    )

    print(f"Owner: {owner.name}")
    print(f"Available time windows:")
    for window in owner.availability:
        print(f"  - {window.start.strftime('%I:%M %p')} to {window.end.strftime('%I:%M %p')}")
    print()

    # Create pets
    dog = Pet(id="pet1", name="Max", species="Dog")
    cat = Pet(id="pet2", name="Whiskers", species="Cat")

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    print(f"Pets: {', '.join([p.name for p in owner.pets])}")
    print()

    # Create tasks for the dog
    walk_task = Task(
        id="task1",
        title="Morning Walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        required=True,
        recurrence=RecurrencePattern.DAILY,
        preferred_windows=[TimeWindow(start=time(7, 0), end=time(9, 0))]
    )

    feeding_task = Task(
        id="task2",
        title="Feed Max",
        duration_minutes=15,
        priority=Priority.CRITICAL,
        required=True,
        recurrence=RecurrencePattern.DAILY,
    )

    playtime_task = Task(
        id="task3",
        title="Play & Training",
        duration_minutes=20,
        priority=Priority.MEDIUM,
        recurrence=RecurrencePattern.DAILY,
        preferred_windows=[TimeWindow(start=time(17, 0), end=time(20, 0))]
    )

    grooming_task = Task(
        id="task4",
        title="Brush Fur",
        duration_minutes=10,
        priority=Priority.LOW,
        recurrence=RecurrencePattern.WEEKLY,
    )

    # Create tasks for the cat
    cat_feed_task = Task(
        id="task5",
        title="Feed Whiskers",
        duration_minutes=10,
        priority=Priority.CRITICAL,
        required=True,
        recurrence=RecurrencePattern.DAILY,
    )

    litter_task = Task(
        id="task6",
        title="Clean Litter Box",
        duration_minutes=15,
        priority=Priority.HIGH,
        required=True,
        recurrence=RecurrencePattern.DAILY,
    )

    cat_play_task = Task(
        id="task7",
        title="Interactive Play",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        recurrence=RecurrencePattern.DAILY,
        preferred_windows=[TimeWindow(start=time(17, 0), end=time(20, 0))]
    )

    # Add tasks to pets
    dog.add_task(walk_task)
    dog.add_task(feeding_task)
    dog.add_task(playtime_task)
    dog.add_task(grooming_task)

    cat.add_task(cat_feed_task)
    cat.add_task(litter_task)
    cat.add_task(cat_play_task)

    print(f"{dog.name}'s tasks: {len(dog.tasks)}")
    for task in dog.tasks:
        print(f"  - {task.title} ({task.duration_minutes} min, {task.priority.value})")
    print()

    print(f"{cat.name}'s tasks: {len(cat.tasks)}")
    for task in cat.tasks:
        print(f"  - {task.title} ({task.duration_minutes} min, {task.priority.value})")
    print()

    # Create scheduler
    scheduler = Scheduler()

    # Generate schedule for the dog
    print("=" * 60)
    print(f"GENERATING SCHEDULE FOR {dog.name.upper()}")
    print("=" * 60)
    today = datetime.now()
    dog_schedule = scheduler.generate_schedule(owner, dog, today)

    print(f"\nSchedule Date: {dog_schedule.date.strftime('%A, %B %d, %Y')}")
    print(f"Total Available Time: {dog_schedule.total_minutes_available} minutes")
    print(f"Total Scheduled Time: {dog_schedule.total_minutes_scheduled} minutes")
    print(f"Utilization Rate: {dog_schedule.get_utilization_rate():.1f}%")
    print()

    print(f"SCHEDULED TASKS ({len(dog_schedule.scheduled_tasks)}):")
    print("-" * 60)
    for st in dog_schedule.scheduled_tasks:
        print(f"{st.start_time.strftime('%I:%M %p')} - {st.end_time.strftime('%I:%M %p')}: {st.task.title}")
        print(f"  Duration: {st.task.duration_minutes} min | {st.reason}")
        print()

    if dog_schedule.unscheduled_tasks:
        print(f"UNSCHEDULED TASKS ({len(dog_schedule.unscheduled_tasks)}):")
        print("-" * 60)
        for task in dog_schedule.unscheduled_tasks:
            print(f"- {task.title} ({task.duration_minutes} min, {task.priority.value})")
        print()

    # Generate schedule for the cat
    print("=" * 60)
    print(f"GENERATING SCHEDULE FOR {cat.name.upper()}")
    print("=" * 60)
    cat_schedule = scheduler.generate_schedule(owner, cat, today)

    print(f"\nSchedule Date: {cat_schedule.date.strftime('%A, %B %d, %Y')}")
    print(f"Total Available Time: {cat_schedule.total_minutes_available} minutes")
    print(f"Total Scheduled Time: {cat_schedule.total_minutes_scheduled} minutes")
    print(f"Utilization Rate: {cat_schedule.get_utilization_rate():.1f}%")
    print()

    print(f"SCHEDULED TASKS ({len(cat_schedule.scheduled_tasks)}):")
    print("-" * 60)
    for st in cat_schedule.scheduled_tasks:
        print(f"{st.start_time.strftime('%I:%M %p')} - {st.end_time.strftime('%I:%M %p')}: {st.task.title}")
        print(f"  Duration: {st.task.duration_minutes} min | {st.reason}")
        print()

    if cat_schedule.unscheduled_tasks:
        print(f"UNSCHEDULED TASKS ({len(cat_schedule.unscheduled_tasks)}):")
        print("-" * 60)
        for task in cat_schedule.unscheduled_tasks:
            print(f"- {task.title} ({task.duration_minutes} min, {task.priority.value})")
        print()

    # Show decision explanation
    print("=" * 60)
    print("SCHEDULING EXPLANATION")
    print("=" * 60)
    print(scheduler.explain_decision())
    print()

    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
