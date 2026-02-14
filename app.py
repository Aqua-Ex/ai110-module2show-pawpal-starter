import streamlit as st
from datetime import datetime, time
from pawpal_system import (
    Owner,
    Pet,
    Task,
    TimeWindow,
    Priority,
    RecurrencePattern,
    Scheduler,
    Schedule,
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("📝 Owner & Pet Setup")

# Owner section
col1, col2 = st.columns([2, 1])
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    if st.button("Create/Update Owner"):
        if owner_name:
            st.session_state.owner = Owner(
                id="owner1",
                name=owner_name,
                availability=[]  # Will be set later
            )
            st.success(f"✅ Owner '{owner_name}' created!")
        else:
            st.error("Please enter an owner name")

# Pet section
st.markdown("### Your Pet")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    st.write("")  # Spacer
    st.write("")  # Spacer
    if st.button("Add Pet"):
        if pet_name and st.session_state.owner:
            # Create or update pet
            st.session_state.pet = Pet(
                id="pet1",
                name=pet_name,
                species=species
            )
            # Use the add_pet method from Owner class
            st.session_state.owner.add_pet(st.session_state.pet)
            st.success(f"✅ Pet '{pet_name}' added to {st.session_state.owner.name}'s care!")
        elif not st.session_state.owner:
            st.error("Please create an owner first")
        else:
            st.error("Please enter a pet name")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# Initialize session state for persistent data
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = None

if "pet" not in st.session_state:
    st.session_state.pet = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add Task"):
    if not st.session_state.pet:
        st.error("⚠️ Please add a pet first before adding tasks!")
    elif not task_title:
        st.error("⚠️ Please enter a task title")
    else:
        try:
            # Map string priority to Priority enum
            priority_map = {
                "low": Priority.LOW,
                "medium": Priority.MEDIUM,
                "high": Priority.HIGH,
            }

            # Create Task object
            task = Task(
                id=f"task{len(st.session_state.pet.tasks) + 1}",
                title=task_title,
                duration_minutes=int(duration),
                priority=priority_map.get(priority, Priority.MEDIUM)
            )

            # Use the add_task method from Pet class
            st.session_state.pet.add_task(task)

            # Also keep in session tasks for display
            st.session_state.tasks.append(
                {"title": task_title, "duration_minutes": int(duration), "priority": priority}
            )

            st.success(f"✅ Added '{task_title}' to {st.session_state.pet.name}'s tasks!")
        except ValueError as e:
            st.error(f"Error adding task: {str(e)}")

# Display tasks from Pet object if it exists
if st.session_state.pet and st.session_state.pet.tasks:
    st.write(f"**{st.session_state.pet.name}'s Tasks:**")

    for task in st.session_state.pet.tasks:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**{task.title}**")
        with col2:
            st.caption(f"{task.duration_minutes} min")
        with col3:
            st.caption(f"{task.priority.value}")
        with col4:
            # Use pet.remove_task() method
            if st.button("🗑️", key=f"del_{task.id}"):
                if st.session_state.pet.remove_task(task.id):
                    # Also remove from session tasks list
                    st.session_state.tasks = [
                        t for t in st.session_state.tasks
                        if t["title"] != task.title
                    ]
                    st.rerun()

    st.divider()

    # Show task counts by priority
    col1, col2, col3 = st.columns(3)
    with col1:
        high_tasks = st.session_state.pet.get_tasks_by_priority(Priority.HIGH)
        st.metric("High Priority", len(high_tasks))
    with col2:
        medium_tasks = st.session_state.pet.get_tasks_by_priority(Priority.MEDIUM)
        st.metric("Medium Priority", len(medium_tasks))
    with col3:
        low_tasks = st.session_state.pet.get_tasks_by_priority(Priority.LOW)
        st.metric("Low Priority", len(low_tasks))

    # Task filtering view
    with st.expander("🔍 Filter & Sort Tasks", expanded=False):
        filter_option = st.selectbox(
            "Show tasks:",
            ["All Tasks", "Completed Tasks", "Incomplete Tasks", "High Priority", "Medium Priority", "Low Priority"]
        )

        if filter_option == "Completed Tasks":
            filtered = st.session_state.pet.get_completed_tasks()
        elif filter_option == "Incomplete Tasks":
            filtered = st.session_state.pet.get_incomplete_tasks()
        elif filter_option == "High Priority":
            filtered = st.session_state.pet.get_tasks_by_priority(Priority.HIGH)
        elif filter_option == "Medium Priority":
            filtered = st.session_state.pet.get_tasks_by_priority(Priority.MEDIUM)
        elif filter_option == "Low Priority":
            filtered = st.session_state.pet.get_tasks_by_priority(Priority.LOW)
        else:
            filtered = st.session_state.pet.tasks

        if filtered:
            task_table = []
            for task in filtered:
                task_table.append({
                    "Task": task.title,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority.value.title(),
                    "Status": "✅ Done" if task.last_done else "⏳ Pending",
                    "Recurrence": task.recurrence.value.replace("_", " ").title()
                })
            st.table(task_table)
        else:
            st.info(f"No tasks found for filter: {filter_option}")

elif st.session_state.tasks:
    st.write("Current tasks (not yet assigned to a pet):")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# Show persisted data info
with st.expander("🔍 Session State & Methods Used (Debug)", expanded=False):
    st.markdown("**Current Session Data:**")

    if st.session_state.owner:
        st.success(f"✅ Owner: {st.session_state.owner.name} (ID: {st.session_state.owner.id})")
        st.caption(f"Available windows: {len(st.session_state.owner.availability)}")
        st.caption(f"Pets: {len(st.session_state.owner.pets)} (using owner.pets list)")
    else:
        st.info("No owner created yet")

    if st.session_state.pet:
        st.success(f"✅ Pet: {st.session_state.pet.name} ({st.session_state.pet.species})")
        st.caption(f"Owner ID: {st.session_state.pet.owner_id}")
        st.caption(f"Tasks: {len(st.session_state.pet.tasks)} (using pet.tasks list)")

        # Show required tasks count
        required_tasks = st.session_state.pet.get_required_tasks()
        st.caption(f"Required tasks: {len(required_tasks)} (using pet.get_required_tasks())")
    else:
        st.info("No pet created yet")

    st.markdown("---")
    st.markdown("**Class Methods Being Used:**")
    st.code("""
# Owner methods:
owner.add_pet(pet)          # Adds pet to owner's pets list
owner.get_availability()     # Returns availability windows

# Pet methods:
pet.add_task(task)          # Adds task to pet's tasks list
pet.remove_task(task_id)    # Removes task by ID
pet.get_tasks_by_priority() # Gets tasks by priority level
pet.get_required_tasks()    # Gets all required tasks

# Scheduler methods:
scheduler.generate_schedule() # Creates optimized schedule
scheduler.score_task()        # Scores tasks for priority
    """, language="python")

    st.markdown("---")
    st.markdown("**Session State Pattern:**")
    st.markdown("""
    - `st.session_state` persists data across page refreshes
    - Objects are stored in the "vault" until browser tab closes
    - Methods are called on persisted objects, not recreated
    - Changes persist because we modify the same object instance
    """)

st.divider()

st.subheader("Owner Availability")
st.caption("Define when you're available to care for your pet")

# Add time window inputs
col1, col2 = st.columns(2)
with col1:
    start_hour = st.number_input("Start hour (0-23)", min_value=0, max_value=23, value=7)
    start_minute = st.number_input("Start minute", min_value=0, max_value=59, value=0, key="start_min")
with col2:
    end_hour = st.number_input("End hour (0-23)", min_value=0, max_value=23, value=20)
    end_minute = st.number_input("End minute", min_value=0, max_value=59, value=0, key="end_min")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your tasks and availability")

if st.button("Generate schedule"):
    if not st.session_state.owner:
        st.warning("⚠️ Please create an owner first!")
    elif not st.session_state.pet:
        st.warning("⚠️ Please add a pet first!")
    elif not st.session_state.pet.tasks:
        st.warning("⚠️ Please add at least one task to your pet before generating a schedule.")
    else:
        try:
            # Update owner's availability with current input values
            st.session_state.owner.availability = [
                TimeWindow(
                    start=time(start_hour, start_minute),
                    end=time(end_hour, end_minute)
                )
            ]

            # Generate schedule using session state objects
            scheduler = Scheduler()
            schedule = scheduler.generate_schedule(
                st.session_state.owner,
                st.session_state.pet,
                datetime.now()
            )

            # Display results
            st.success("✅ Schedule generated successfully!")

            # Check for scheduling conflicts/warnings
            if scheduler.has_warnings():
                st.warning("⚠️ **Scheduling Conflicts Detected**")
                st.markdown("Some tasks overlap in time. Consider adjusting task durations or extending your availability window.")

                with st.expander("📋 View Conflict Details", expanded=True):
                    for warning in scheduler.get_warnings():
                        st.warning(warning)

                    st.markdown("**💡 Suggestions:**")
                    st.markdown("""
                    - Reduce the duration of lower-priority tasks
                    - Add more availability windows throughout the day
                    - Mark some tasks as optional (lower priority)
                    - Reschedule conflicting tasks to different days
                    """)

            # Show schedule summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Time Available", f"{schedule.total_minutes_available} min")
            with col2:
                st.metric("Time Scheduled", f"{schedule.total_minutes_scheduled} min")
            with col3:
                st.metric("Utilization", f"{schedule.get_utilization_rate():.1f}%")

            # Display scheduled tasks
            if schedule.scheduled_tasks:
                st.subheader("📅 Your Daily Schedule")

                # Create a table view option
                view_mode = st.radio(
                    "View mode:",
                    ["Detailed Cards", "Compact Table"],
                    horizontal=True,
                    label_visibility="collapsed"
                )

                if view_mode == "Detailed Cards":
                    for st_task in schedule.scheduled_tasks:
                        # Add recurring indicator
                        recurring_badge = ""
                        if st_task.task.recurrence != RecurrencePattern.AS_NEEDED:
                            recurring_badge = f" 🔄 {st_task.task.recurrence.value.replace('_', ' ').title()}"

                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{st_task.task.title}**{recurring_badge}")
                                st.caption(f"{st_task.start_time.strftime('%I:%M %p')} - {st_task.end_time.strftime('%I:%M %p')} • {st_task.reason}")
                            with col2:
                                st.info(f"{st_task.task.duration_minutes} min")
                else:
                    # Compact table view
                    table_data = []
                    for st_task in schedule.scheduled_tasks:
                        recurring_indicator = ""
                        if st_task.task.recurrence != RecurrencePattern.AS_NEEDED:
                            recurring_indicator = " 🔄"

                        table_data.append({
                            "Time": f"{st_task.start_time.strftime('%I:%M %p')} - {st_task.end_time.strftime('%I:%M %p')}",
                            "Task": st_task.task.title + recurring_indicator,
                            "Duration": f"{st_task.task.duration_minutes} min",
                            "Priority": st_task.task.priority.value.title(),
                            "Recurrence": st_task.task.recurrence.value.replace("_", " ").title(),
                            "Reason": st_task.reason
                        })
                    st.table(table_data)

            # Display unscheduled tasks
            if schedule.unscheduled_tasks:
                st.subheader("⚠️ Could Not Schedule")
                st.caption(f"{len(schedule.unscheduled_tasks)} task(s) didn't fit in your availability window")

                # Group by priority for better visibility
                high_unscheduled = [t for t in schedule.unscheduled_tasks if t.priority == Priority.HIGH]
                medium_unscheduled = [t for t in schedule.unscheduled_tasks if t.priority == Priority.MEDIUM]
                low_unscheduled = [t for t in schedule.unscheduled_tasks if t.priority == Priority.LOW]

                if high_unscheduled:
                    st.warning("**🔴 High Priority Tasks Not Scheduled:**")
                    for task in high_unscheduled:
                        st.markdown(f"- **{task.title}** ({task.duration_minutes} min)")

                if medium_unscheduled:
                    st.info("**🟡 Medium Priority Tasks Not Scheduled:**")
                    for task in medium_unscheduled:
                        st.markdown(f"- {task.title} ({task.duration_minutes} min)")

                if low_unscheduled:
                    st.info("**🟢 Low Priority Tasks Not Scheduled:**")
                    for task in low_unscheduled:
                        st.markdown(f"- {task.title} ({task.duration_minutes} min)")

                st.markdown("**💡 To fit more tasks:**")
                st.markdown("""
                - Extend your availability window (add more hours)
                - Reduce task durations where possible
                - Lower the priority of less important tasks
                - Split tasks across multiple days
                """)

            # Show explanation
            with st.expander("🤔 How was this schedule created?"):
                st.text(schedule.explanation)

        except Exception as e:
            st.error(f"Error generating schedule: {str(e)}")
            st.exception(e)
