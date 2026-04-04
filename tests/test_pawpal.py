import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, time, timedelta
import pawpal_system as ps


# ── Helpers ────────────────────────────────────────────────────────────────

def make_task(title="Walk", task_date=None, task_time=None, duration=20,
              priority=1, recurrence=None, pet_name=""):
    return ps.Task(
        title=title,
        priority=priority,
        duration_in_minutes=duration,
        date=task_date or date(2025, 3, 1),
        time=task_time or time(8, 0),
        recurrence=recurrence,
        pet_name=pet_name,
    )


def make_scheduler(*tasks):
    owner = ps.Owner("Test Owner", 120)
    scheduler = ps.Scheduler(owner=owner, pets_involved=[])
    for task in tasks:
        scheduler.add_task(task)
    return scheduler


# ── Existing tests (bugs fixed) ────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_task_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = ps.Pet("Cookie", 6, 15.5, "Doodle")
    assert len(pet.tasks) == 0
    pet.add_task(make_task("Feeding"))
    assert len(pet.tasks) == 1
    pet.add_task(make_task("Walk"))
    assert len(pet.tasks) == 2


# ── Sorting ────────────────────────────────────────────────────────────────

def test_sort_by_time_orders_by_date_then_time():
    # Added out of order: March 2 @ 7am, March 1 @ 10am, March 1 @ 8am
    t1 = make_task("Walk",     task_date=date(2025, 3, 1), task_time=time(8, 0))
    t2 = make_task("Feeding",  task_date=date(2025, 3, 2), task_time=time(7, 0))
    t3 = make_task("Grooming", task_date=date(2025, 3, 1), task_time=time(10, 0))

    scheduler = make_scheduler(t2, t3, t1)
    scheduler.sort_by_time()

    titles = [t.title for t in scheduler.tasks]
    assert titles == ["Walk", "Grooming", "Feeding"]


def test_sort_by_time_date_beats_time():
    # 11:59 PM on March 1 should come before 7:00 AM on March 2
    late  = make_task("Late Walk",   task_date=date(2025, 3, 1), task_time=time(23, 59))
    early = make_task("Early Feed",  task_date=date(2025, 3, 2), task_time=time(7, 0))

    scheduler = make_scheduler(early, late)
    scheduler.sort_by_time()

    assert scheduler.tasks[0].title == "Late Walk"
    assert scheduler.tasks[1].title == "Early Feed"


# ── Recurrence ─────────────────────────────────────────────────────────────

def test_daily_recurrence_creates_next_day_task():
    task = make_task(task_date=date(2025, 3, 1), recurrence="daily")
    next_task = task.mark_task_complete()

    assert next_task is not None
    assert next_task.date == date(2025, 3, 2)
    assert next_task.completed is False


def test_weekly_recurrence_creates_task_seven_days_later():
    task = make_task(task_date=date(2025, 3, 1), recurrence="weekly")
    next_task = task.mark_task_complete()

    assert next_task is not None
    assert next_task.date == date(2025, 3, 8)
    assert next_task.completed is False


def test_no_recurrence_returns_none():
    task = make_task(recurrence=None)
    result = task.mark_task_complete()
    assert result is None


# ── Conflict detection ─────────────────────────────────────────────────────

def test_detect_conflicts_flags_same_time_tasks():
    t1 = make_task("Walk",    task_date=date(2025, 3, 1), task_time=time(8, 0), pet_name="Mocha")
    t2 = make_task("Feeding", task_date=date(2025, 3, 1), task_time=time(8, 0), pet_name="Cookie")

    scheduler = make_scheduler(t1, t2)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feeding" in conflicts[0]


def test_detect_conflicts_flags_overlapping_tasks():
    # Walk: 8:00–9:00, Feeding: 8:30–9:00 → overlap
    t1 = make_task("Walk",    task_date=date(2025, 3, 1), task_time=time(8, 0),  duration=60)
    t2 = make_task("Feeding", task_date=date(2025, 3, 1), task_time=time(8, 30), duration=30)

    scheduler = make_scheduler(t1, t2)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_detect_conflicts_ignores_back_to_back_tasks():
    # Walk: 8:00–9:00, Feeding: 9:00–9:30 → back-to-back, no conflict
    t1 = make_task("Walk",    task_date=date(2025, 3, 1), task_time=time(8, 0), duration=60)
    t2 = make_task("Feeding", task_date=date(2025, 3, 1), task_time=time(9, 0), duration=30)

    scheduler = make_scheduler(t1, t2)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0


def test_detect_conflicts_ignores_different_dates():
    # Same time but different dates → no conflict
    t1 = make_task("Walk",    task_date=date(2025, 3, 1), task_time=time(8, 0))
    t2 = make_task("Feeding", task_date=date(2025, 3, 2), task_time=time(8, 0))

    scheduler = make_scheduler(t1, t2)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0
