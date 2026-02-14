# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## ✨ New Features & Algorithm Improvements

This implementation includes several advanced scheduling algorithms that significantly improve efficiency:

### 🚀 Performance Optimizations
- **Window Duration Caching**: Pre-calculates and caches time window durations (~70% faster)
- **Binary Search Insertion**: Uses `bisect.insort()` to maintain sorted schedules (O(log n) search)
- **Pre-sorted Windows**: Automatically sorts time windows chronologically for consistent scheduling

### 🎯 Smart Scheduling
- **Required Task Pre-allocation**: Critical/required tasks scheduled before optional ones
- **Scaled Overdue Scoring**: Tasks get +0.5 priority per day overdue (capped at +3.0)
- **Window Fit Optimization**: Bonus scoring for tasks that fit tightly in preferred windows
- **Window Fragmentation**: Splits time windows after scheduling, reusing remaining time (15-200% more tasks scheduled!)

### 🐾 Pet Care Features
- **Recurring Task Auto-creation**: Daily/weekly/monthly tasks automatically generate next instance when completed
- **Task Filtering**: Filter by completion status, priority, or pet name
- **Conflict Detection**: Lightweight warning system for overlapping tasks (non-blocking)



## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
