import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
import pawpal_system as ps


def make_task(title="Walk"):
    return ps.Task(title=title, priority=1, duration_in_minutes=20, date=date.today())


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = ps.Pet("Cookie", 6, 15.5, "Doodle")
    assert len(pet.tasks) == 0
    pet.add_task(make_task("Feeding"))
    assert len(pet.tasks) == 1
    pet.add_task(make_task("Walk"))
    assert len(pet.tasks) == 2
