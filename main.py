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

    # ========== NEW: TESTING SORTING AND FILTERING ==========
    print("=" * 60)
    print("TESTING SORTING AND FILTERING METHODS")
    print("=" * 60)
    print()

    # Test 1: Add tasks out of order to demonstrate sorting
    print("TEST 1: Adding tasks out of order")
    print("-" * 60)
    test_pet = Pet(id="pet_test", name="Buddy", species="Dog")

    # Add tasks with different times (out of order)
    task_evening = Task(
        id="evening_task",
        title="Evening Walk",
        duration_minutes=25,
        priority=Priority.HIGH,
        last_done=datetime.now()  # Mark as completed
    )

    task_morning = Task(
        id="morning_task",
        title="Morning Breakfast",
        duration_minutes=10,
        priority=Priority.CRITICAL
        # Note: last_done is None (incomplete)
    )

    task_afternoon = Task(
        id="afternoon_task",
        title="Afternoon Play",
        duration_minutes=30,
        priority=Priority.MEDIUM,
        last_done=datetime.now()  # Mark as completed
    )

    # Add tasks out of chronological order
    test_pet.add_task(task_evening)
    test_pet.add_task(task_morning)
    test_pet.add_task(task_afternoon)

    print(f"Added {len(test_pet.tasks)} tasks to {test_pet.name}")
    for i, task in enumerate(test_pet.tasks, 1):
        completion_status = "[X] Done" if task.last_done else "[ ] Not done"
        print(f"  {i}. {task.title} - {completion_status}")
    print()

    # Test 2: Filter by completion status
    print("TEST 2: Filtering by completion status")
    print("-" * 60)
    completed = test_pet.get_completed_tasks()
    incomplete = test_pet.get_incomplete_tasks()

    print(f"Completed tasks ({len(completed)}):")
    for task in completed:
        print(f"  [X] {task.title}")

    print(f"\nIncomplete tasks ({len(incomplete)}):")
    for task in incomplete:
        print(f"  [ ] {task.title}")
    print()

    # Test 3: Filter tasks by pet name
    print("TEST 3: Filtering tasks by pet name")
    print("-" * 60)
    owner.add_pet(test_pet)  # Add test pet to owner

    print(f"Owner {owner.name} has {len(owner.pets)} pets:")
    for pet in owner.pets:
        print(f"  - {pet.name}")

    print(f"\nFiltering tasks for '{dog.name}':")
    max_tasks = owner.get_tasks_by_pet_name(dog.name)
    for task in max_tasks:
        print(f"  - {task.title}")

    print(f"\nFiltering tasks for '{test_pet.name}':")
    buddy_tasks = owner.get_tasks_by_pet_name(test_pet.name)
    for task in buddy_tasks:
        print(f"  - {task.title}")
    print()

    # Test 4: Demonstrate sorting with schedule
    print("TEST 4: Testing sort_by_time() on schedule")
    print("-" * 60)
    print("Before sorting, scheduled tasks are in order of scheduling priority.")
    print("After sort_by_time(), they're sorted chronologically.")
    print()

    if dog_schedule.scheduled_tasks:
        # Create a copy and shuffle to demonstrate sorting
        print("Scheduled tasks (already sorted by sort_by_time()):")
        for st in dog_schedule.scheduled_tasks:
            print(f"  {st.start_time.strftime('%I:%M %p')}: {st.task.title}")
    print()

    # ========== NEW: TESTING RECURRING TASK COMPLETION ==========
    print("=" * 60)
    print("TEST 5: Testing mark_task_complete() with recurring tasks")
    print("=" * 60)
    print()

    # Create a test pet with a daily recurring task
    print("Setting up test scenario:")
    print("-" * 60)
    test_dog = Pet(id="test_dog", name="Luna", species="Dog")

    daily_walk = Task(
        id="daily_walk",
        title="Daily Walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        required=True,
        recurrence=RecurrencePattern.DAILY,
        preferred_windows=[TimeWindow(start=time(7, 0), end=time(9, 0))]
    )

    weekly_grooming = Task(
        id="weekly_grooming",
        title="Weekly Grooming",
        duration_minutes=45,
        priority=Priority.MEDIUM,
        recurrence=RecurrencePattern.WEEKLY
    )

    monthly_vet = Task(
        id="monthly_vet",
        title="Monthly Vet Check",
        duration_minutes=60,
        priority=Priority.HIGH,
        required=True,
        recurrence=RecurrencePattern.MONTHLY
    )

    as_needed_bath = Task(
        id="as_needed_bath",
        title="Bath (as needed)",
        duration_minutes=30,
        priority=Priority.LOW,
        recurrence=RecurrencePattern.AS_NEEDED
    )

    test_dog.add_task(daily_walk)
    test_dog.add_task(weekly_grooming)
    test_dog.add_task(monthly_vet)
    test_dog.add_task(as_needed_bath)

    print(f"Created pet '{test_dog.name}' with {len(test_dog.tasks)} tasks:")
    for task in test_dog.tasks:
        print(f"  - {task.id}: {task.title} ({task.recurrence.value})")
    print()

    # Test marking a daily task complete
    print("TEST 5.1: Marking daily task complete")
    print("-" * 60)
    print(f"Before: {test_dog.name} has {len(test_dog.tasks)} tasks")
    print(f"Daily Walk status: last_done = {daily_walk.last_done}")
    print()

    print("Calling mark_task_complete('daily_walk')...")
    new_daily_task = test_dog.mark_task_complete("daily_walk")

    print(f"After: {test_dog.name} has {len(test_dog.tasks)} tasks")
    print(f"Original Daily Walk: last_done = {daily_walk.last_done.strftime('%Y-%m-%d %H:%M:%S')}")
    if new_daily_task:
        print(f"New task created: {new_daily_task.id}")
        print(f"  - Title: {new_daily_task.title}")
        print(f"  - Recurrence: {new_daily_task.recurrence.value}")
        print(f"  - Priority: {new_daily_task.priority.value}")
        print(f"  - Required: {new_daily_task.required}")
        print(f"  - Last Done: {new_daily_task.last_done}")
        print(f"  - Preferred Windows: {len(new_daily_task.preferred_windows)}")
    print()

    # Test marking a weekly task complete
    print("TEST 5.2: Marking weekly task complete")
    print("-" * 60)
    print(f"Before: {len(test_dog.tasks)} tasks")
    print(f"Weekly Grooming status: last_done = {weekly_grooming.last_done}")
    print()

    print("Calling mark_task_complete('weekly_grooming')...")
    new_weekly_task = test_dog.mark_task_complete("weekly_grooming")

    print(f"After: {len(test_dog.tasks)} tasks")
    if new_weekly_task:
        print(f"New task created: {new_weekly_task.id}")
        print(f"  - Title: {new_weekly_task.title}")
    print()

    # Test marking a monthly task complete
    print("TEST 5.3: Marking monthly task complete")
    print("-" * 60)
    print(f"Before: {len(test_dog.tasks)} tasks")

    print("Calling mark_task_complete('monthly_vet')...")
    new_monthly_task = test_dog.mark_task_complete("monthly_vet")

    print(f"After: {len(test_dog.tasks)} tasks")
    if new_monthly_task:
        print(f"New task created: {new_monthly_task.id}")
        print(f"  - Title: {new_monthly_task.title}")
    print()

    # Test marking an AS_NEEDED task complete (should NOT create new instance)
    print("TEST 5.4: Marking AS_NEEDED task complete (should NOT create new instance)")
    print("-" * 60)
    print(f"Before: {len(test_dog.tasks)} tasks")

    print("Calling mark_task_complete('as_needed_bath')...")
    new_as_needed_task = test_dog.mark_task_complete("as_needed_bath")

    print(f"After: {len(test_dog.tasks)} tasks")
    if new_as_needed_task:
        print(f"New task created: {new_as_needed_task.id}")
    else:
        print("No new task created (expected behavior for AS_NEEDED tasks)")
    print()

    # Test marking the same daily task complete multiple times
    print("TEST 5.5: Marking daily task complete multiple times")
    print("-" * 60)
    print(f"Current task count: {len(test_dog.tasks)}")
    print()

    # Mark the new daily task complete
    print("Marking daily_walk_next_1 complete...")
    new_task_2 = test_dog.mark_task_complete("daily_walk_next_1")
    if new_task_2:
        print(f"New task created: {new_task_2.id}")

    # Mark it complete again
    print(f"Marking {new_task_2.id} complete...")
    new_task_3 = test_dog.mark_task_complete(new_task_2.id)
    if new_task_3:
        print(f"New task created: {new_task_3.id}")

    print(f"\nFinal task count: {len(test_dog.tasks)}")
    print(f"\nAll tasks for {test_dog.name}:")
    for task in test_dog.tasks:
        status = "COMPLETED" if task.last_done else "PENDING"
        print(f"  - {task.id}: {task.title} [{status}]")
    print()

    # Test error handling
    print("TEST 5.6: Error handling for non-existent task")
    print("-" * 60)
    try:
        test_dog.mark_task_complete("non_existent_task")
        print("ERROR: Should have raised ValueError!")
    except ValueError as e:
        print(f"Correctly raised ValueError: {e}")
    print()

    # ========== NEW: TESTING CONFLICT DETECTION ==========
    print("=" * 60)
    print("TEST 6: Testing conflict detection for overlapping tasks")
    print("=" * 60)
    print()

    # Create a test pet with overlapping tasks
    print("Setting up conflict scenario:")
    print("-" * 60)
    conflict_pet = Pet(id="conflict_pet", name="Charlie", species="Cat")

    # Create two tasks with preferred windows that overlap
    morning_feed = Task(
        id="morning_feed",
        title="Morning Feeding",
        duration_minutes=30,
        priority=Priority.CRITICAL,
        required=True,
        preferred_windows=[TimeWindow(start=time(7, 0), end=time(8, 0))]
    )

    morning_play = Task(
        id="morning_play",
        title="Morning Playtime",
        duration_minutes=30,
        priority=Priority.HIGH,
        required=True,
        preferred_windows=[TimeWindow(start=time(7, 0), end=time(8, 0))]  # Same window!
    )

    morning_walk = Task(
        id="morning_walk_cat",
        title="Morning Walk",
        duration_minutes=20,
        priority=Priority.MEDIUM,
        preferred_windows=[TimeWindow(start=time(7, 15), end=time(8, 0))]  # Overlaps with feeding
    )

    conflict_pet.add_task(morning_feed)
    conflict_pet.add_task(morning_play)
    conflict_pet.add_task(morning_walk)

    print(f"Created pet '{conflict_pet.name}' with {len(conflict_pet.tasks)} tasks")
    print("Tasks with overlapping preferred windows:")
    for task in conflict_pet.tasks:
        if task.preferred_windows:
            window = task.preferred_windows[0]
            print(f"  - {task.title}: {window.start.strftime('%I:%M %p')} - {window.end.strftime('%I:%M %p')}")
    print()

    # Create owner with availability matching the preferred windows
    conflict_owner = Owner(
        id="owner_conflict",
        name="Sam",
        availability=[TimeWindow(start=time(7, 0), end=time(8, 30))]
    )
    conflict_owner.add_pet(conflict_pet)

    print("TEST 6.1: Generating schedule with potential conflicts")
    print("-" * 60)
    conflict_scheduler = Scheduler()
    conflict_schedule = conflict_scheduler.generate_schedule(
        conflict_owner,
        conflict_pet,
        datetime.now()
    )

    print(f"Schedule generated:")
    print(f"  - Scheduled tasks: {len(conflict_schedule.scheduled_tasks)}")
    print(f"  - Unscheduled tasks: {len(conflict_schedule.unscheduled_tasks)}")
    print()

    # Display scheduled tasks
    if conflict_schedule.scheduled_tasks:
        print("Successfully scheduled:")
        for st in conflict_schedule.scheduled_tasks:
            print(f"  {st.start_time.strftime('%I:%M %p')} - {st.end_time.strftime('%I:%M %p')}: {st.task.title}")
        print()

    # Display unscheduled tasks
    if conflict_schedule.unscheduled_tasks:
        print("Could not schedule (due to conflicts):")
        for task in conflict_schedule.unscheduled_tasks:
            print(f"  - {task.title}")
        print()

    # Display warnings
    print("TEST 6.2: Checking for conflict warnings")
    print("-" * 60)
    if conflict_scheduler.has_warnings():
        print(f"WARNING: {len(conflict_scheduler.get_warnings())} conflict(s) detected!")
        print()
        for warning in conflict_scheduler.get_warnings():
            print(f"  [!] {warning}")
    else:
        print("No conflicts detected - all tasks scheduled successfully!")
    print()

    # Test with multiple pets scheduling at the same time
    print("TEST 6.3: Multiple pets with overlapping schedules")
    print("-" * 60)

    # Create second pet with task at same time as first pet
    pet2 = Pet(id="pet2_conflict", name="Bella", species="Dog")
    pet2_task = Task(
        id="pet2_morning_feed",
        title="Bella's Morning Feeding",
        duration_minutes=20,
        priority=Priority.CRITICAL,
        preferred_windows=[TimeWindow(start=time(7, 0), end=time(8, 0))]
    )
    pet2.add_task(pet2_task)
    conflict_owner.add_pet(pet2)

    print(f"Added second pet '{pet2.name}' with overlapping schedule")
    print(f"Both pets need feeding at 7:00 AM")
    print()

    # Generate schedules for both pets
    schedule1 = conflict_scheduler.generate_schedule(conflict_owner, conflict_pet, datetime.now())
    schedule2 = conflict_scheduler.generate_schedule(conflict_owner, pet2, datetime.now())

    print(f"{conflict_pet.name}'s schedule: {len(schedule1.scheduled_tasks)} tasks scheduled")
    print(f"{pet2.name}'s schedule: {len(schedule2.scheduled_tasks)} tasks scheduled")
    print()

    print("Note: In a real-world scenario, you'd want to combine these schedules")
    print("and ensure the owner has enough time for both pets!")
    print()

    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
