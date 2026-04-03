import pawpal_system as ps
from datetime import date

alice = ps.Owner("Alice", 120)
cookie = ps.Pet("Cookie", 6, 15.5, "Doodle")
mocha = ps.Pet("Mocha", 3, 7.2, "Poodle")

scheduler = ps.Scheduler(owner=alice, pets_involved=[cookie, mocha])

scheduler.add_task(ps.Task("Morning Walk", priority=1,
                   duration_in_minutes=30, date=date.today()))
scheduler.add_task(ps.Task("Feeding Time", priority=2,
                   duration_in_minutes=15, date=date.today()))
scheduler.add_task(ps.Task("Vet Check-up", priority=3,
                   duration_in_minutes=60, date=date.today()))

print("=== Today's Schedule ===")
for task in scheduler.tasks:
    print(
        f"[Priority {task.priority}] {task.title} — {task.duration_in_minutes} min  ({task.date})"
    )
