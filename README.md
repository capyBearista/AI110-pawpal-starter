# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## Smarter Scheduling

The `Scheduler` class includes logic to make daily pet care planning more reliable:

- **Conflict detection** (`detect_conflicts`): Flags any two tasks that are scheduled at overlapping times on the same day, so you can catch accidental double-bookings before they happen.
- **Chronological sorting** (`sort_by_time`): Reorders all tasks by date and start time, giving you a clean, time-ordered view of the day.
- **Filtered views** (`filter_tasks`): Lets you slice the task list by completion status or pet name.
- **Prioritized schedule building** (`build_schedule`): Selects and orders tasks to fit within the owner's available time budget.

## Testing PawPal+

Run the full test suite from the `pawpal-starter` directory:

```bash
python -m pytest
```

The test suite covers the following behaviors:

| Group | What is tested |
|---|---|
| **Sorting** | Tasks in mixed order come out chronologically; date takes priority over time of day |
| **Recurrence** | Completing a daily task creates a new task dated `+1 day`; weekly creates `+7 days`; one-time tasks return `None` |
| **Conflict detection** | Double-booked and overlapping slots are flagged; back-to-back tasks and same-time tasks on different dates are not flagged |

> **Confidence Level: 3/5 ⭐**
> *The core behaviors — sorting, recurrence, and conflict detection — are well-tested and reliable, but I am capping confidence at 3 stars because `build_schedule` (the prioritized daily plan builder) isn't yet implemented. We can't be totally sure that the system functions perfectly, without it.*