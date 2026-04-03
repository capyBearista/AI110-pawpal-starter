import pawpal_system as ps
from datetime import date, time

alice = ps.Owner("Alice", 120)
cookie = ps.Pet("Cookie", 6, 15.5, "Doodle")
mocha = ps.Pet("Mocha", 3, 7.2, "Poodle")

scheduler = ps.Scheduler(owner=alice, pets_involved=[cookie, mocha])

scheduler.add_task(ps.Task("Feeding Time", priority=2,
                   duration_in_minutes=15, date=date.today(), time=time(12, 30), pet_name="Cookie"))
scheduler.add_task(ps.Task("Morning Walk", priority=1,
                   duration_in_minutes=30, date=date.today(), time=time(8, 0), pet_name="Mocha"))
scheduler.add_task(ps.Task("Vet Check-up", priority=3,
                   duration_in_minutes=60, date=date.today(), time=time(16, 0), pet_name="Mocha"))
scheduler.add_task(ps.Task("Grooming Session", priority=2,
                   duration_in_minutes=45, date=date.today(), time=time(8, 15), pet_name="Cookie"))

print("=== Today's Schedule ===")
for task in scheduler.tasks:
    print(
        f"[Priority {task.priority}] {task.title} — {task.duration_in_minutes} min  ({task.date})"
    )

print("\n=== Today's Schedule (Chronological)===")
scheduler.sort_by_time()
for task in scheduler.tasks:
    print(
        f"[Priority {task.priority}] {task.title} — {task.duration_in_minutes} min  ({task.date})"
    )

print("\n=== Incomplete Tasks for Cookie ===")
print(scheduler.filter_tasks(completed=False, pet_name="Cookie"))

print("\n=== Conflict Detection ===")
warnings = scheduler.detect_conflicts()
if warnings:
    for warning in warnings:
        print(warning)
else:
    print("No conflicts detected.")