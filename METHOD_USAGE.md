# PawPal+ Method Usage Guide

This document shows where and how class methods from `pawpal_system.py` are used in the Streamlit app.

## 🏗️ Owner Class Methods

### `Owner.__init__(id, name, availability)`
**Where:** app.py, line ~48
**Usage:** Creating owner object when "Create/Update Owner" button is clicked
```python
st.session_state.owner = Owner(
    id="owner1",
    name=owner_name,
    availability=[]
)
```

### `owner.add_pet(pet)`
**Where:** app.py, line ~63
**Usage:** Adding pet to owner's pets list using the class method
```python
st.session_state.owner.add_pet(st.session_state.pet)
```

### `owner.get_availability(date)`
**Where:** Called internally by Scheduler.generate_schedule()
**Usage:** Retrieves owner's availability windows for scheduling
```python
available_windows = owner.get_availability(date)
```

---

## 🐾 Pet Class Methods

### `Pet.__init__(id, name, species, owner_id)`
**Where:** app.py, line ~58
**Usage:** Creating pet object when "Add Pet" button is clicked
```python
st.session_state.pet = Pet(
    id="pet1",
    name=pet_name,
    species=species
)
```

### `pet.add_task(task)`
**Where:** app.py, line ~96
**Usage:** Adding task to pet's task list when "Add Task" button is clicked
```python
task = Task(...)
st.session_state.pet.add_task(task)
```

### `pet.remove_task(task_id)`
**Where:** app.py, line ~116
**Usage:** Removing task when delete button (🗑️) is clicked
```python
if st.session_state.pet.remove_task(task.id):
    st.rerun()
```

### `pet.get_tasks_by_priority(priority)`
**Where:** app.py, line ~125-131
**Usage:** Displaying task count metrics by priority level
```python
high_tasks = st.session_state.pet.get_tasks_by_priority(Priority.HIGH)
st.metric("High Priority", len(high_tasks))
```

### `pet.get_required_tasks()`
**Where:** Debug panel, app.py
**Usage:** Showing count of required tasks in debug info
```python
required_tasks = st.session_state.pet.get_required_tasks()
```

---

## ✅ Task Class Methods

### `Task.__init__(...)`
**Where:** app.py, line ~86
**Usage:** Creating task object when "Add Task" button is clicked
```python
task = Task(
    id=f"task{len(st.session_state.pet.tasks) + 1}",
    title=task_title,
    duration_minutes=int(duration),
    priority=priority_map.get(priority, Priority.MEDIUM)
)
```

### `task.is_overdue()`
**Where:** Called internally by Scheduler.score_task()
**Usage:** Determining if task is overdue for priority scoring
```python
if t.is_overdue():
    score += 1.0
```

---

## 📅 Scheduler Class Methods

### `Scheduler.__init__()`
**Where:** app.py, line ~179
**Usage:** Creating scheduler instance when "Generate schedule" button is clicked
```python
scheduler = Scheduler()
```

### `scheduler.generate_schedule(owner, pet, date)`
**Where:** app.py, line ~180
**Usage:** Generating optimized schedule for the pet
```python
schedule = scheduler.generate_schedule(
    st.session_state.owner,
    st.session_state.pet,
    datetime.now()
)
```

### `scheduler.score_task(task)`
**Where:** Called internally by generate_schedule()
**Usage:** Scoring tasks to determine scheduling priority
```python
scored_tasks = [(self.score_task(t), t) for t in pet.tasks]
```

### `scheduler.explain_decision()`
**Where:** app.py, expander section
**Usage:** Displaying explanation of scheduling decisions
```python
st.text(schedule.explanation)
```

---

## 📊 Schedule Class Methods

### `schedule.add_scheduled_task(scheduled_task)`
**Where:** Called internally by Scheduler._schedule_in_window()
**Usage:** Adding task to schedule if no conflicts
```python
return schedule.add_scheduled_task(scheduled_task)
```

### `schedule.sort_by_time()`
**Where:** Called internally by generate_schedule()
**Usage:** Sorting scheduled tasks chronologically
```python
schedule.sort_by_time()
```

### `schedule.get_utilization_rate()`
**Where:** app.py, line ~196
**Usage:** Displaying utilization percentage metric
```python
st.metric("Utilization", f"{schedule.get_utilization_rate():.1f}%")
```

### `schedule.get_conflicts()`
**Where:** Available but not currently used in UI
**Usage:** Could be used to detect and display scheduling conflicts
```python
conflicts = schedule.get_conflicts()
```

---

## 🔧 TimeWindow Class Methods

### `TimeWindow.__init__(start, end)`
**Where:** app.py, line ~170-174
**Usage:** Creating time window for owner availability
```python
TimeWindow(
    start=time(start_hour, start_minute),
    end=time(end_hour, end_minute)
)
```

### `window.duration_minutes()`
**Where:** Called internally by Scheduler
**Usage:** Calculating total available minutes
```python
total_available = sum(w.duration_minutes() for w in available_windows)
```

### `window.fits_task(duration_minutes)`
**Where:** Called internally by Scheduler._schedule_in_window()
**Usage:** Checking if task can fit in time window
```python
if not window.fits_task(task.duration_minutes):
    return False
```

### `window.overlaps(other)`
**Where:** Available for conflict detection
**Usage:** Could be used to prevent overlapping time windows

---

## 🎯 Method Call Flow

```
User clicks "Generate schedule"
    ↓
Scheduler.generate_schedule() called
    ↓
owner.get_availability(date) → gets TimeWindow objects
    ↓
For each pet.tasks:
    ↓
    scheduler.score_task(task) → uses task.is_overdue()
    ↓
    scheduler._try_schedule_task()
        ↓
        scheduler._schedule_in_window()
            ↓
            window.fits_task() → checks duration
            ↓
            schedule.add_scheduled_task() → adds if no conflicts
    ↓
schedule.sort_by_time() → chronological order
    ↓
Display results using:
    - schedule.total_minutes_available
    - schedule.total_minutes_scheduled
    - schedule.get_utilization_rate()
    - schedule.scheduled_tasks
    - schedule.unscheduled_tasks
    - schedule.explanation
```

---

## 📝 Summary

**Total Methods Used:** 20+

**Direct UI Calls:** 12
- Owner.__init__
- owner.add_pet()
- Pet.__init__
- pet.add_task()
- pet.remove_task()
- pet.get_tasks_by_priority()
- pet.get_required_tasks()
- Task.__init__
- Scheduler.__init__
- scheduler.generate_schedule()
- schedule.get_utilization_rate()
- TimeWindow.__init__

**Internal Calls:** 8+
- owner.get_availability()
- task.is_overdue()
- scheduler.score_task()
- scheduler._try_schedule_task()
- scheduler._schedule_in_window()
- window.duration_minutes()
- window.fits_task()
- schedule.add_scheduled_task()
- schedule.sort_by_time()

All major class methods are being utilized either directly in the UI or internally by the scheduling engine!
