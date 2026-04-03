from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta

@dataclass
class Owner:
    """Represents a pet owner with a name and daily time budget in minutes."""
    name: str
    available_minutes: int

@dataclass
class Pet:
    """Represents a pet with basic info and a list of associated care tasks."""
    name: str
    age: int
    weight: float
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

@dataclass
class Task:
    """Represents a single pet care task with timing, priority, and optional recurrence."""
    title: str
    priority: int  # lower number = higher priority (e.g. 1 is most urgent)
    duration_in_minutes: int
    date: date
    time: time
    recurrence: str | None = None  # e.g. "daily", "weekly" or None for one-time
    pet_name: str = ""
    completed: bool = False

    def mark_task_complete(self) -> "Task | None":
        """Mark this task as completed."""
        self.completed = True

        if self.recurrence == "daily":
            next_date = self.date + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_date = self.date + timedelta(days=7)
        else:
            return None  # no recurrence, so task won't reappear later
        
        # create identical new task but with updated date and reset completion state
        return replace(self, date=next_date, completed=False)

def _tasks_overlap(task1: "Task", task2: "Task") -> bool:
    """Return True if two tasks overlap in time on the same date."""
    start1 = task1.time.hour * 60 + task1.time.minute
    end1   = start1 + task1.duration_in_minutes
    start2 = task2.time.hour * 60 + task2.time.minute
    end2   = start2 + task2.duration_in_minutes
    return start1 < end2 and start2 < end1

@dataclass
class Scheduler:
    """Manages tasks for an owner's pets and provides scheduling, filtering, and conflict detection."""
    owner: Owner
    pets_involved: list[Pet]
    tasks: list[Task] = field(default_factory=list)
    target_date: date = field(default_factory=date.today)

    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        self.tasks.append(task)

    def build_schedule(self) -> list[Task]:
        """Return a prioritized list of tasks that fits within the owner's available time."""
        return []
    
    def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> list[Task]:
        """Return tasks matching the given completion status and/or pet name. None means no filter."""
        return [
            t for t in self.tasks
            if (completed is None or t.completed == completed)
            and (pet_name is None or t.pet_name == pet_name)
        ]

    def detect_conflicts(self) -> list[str]:
        """Return a warning message for every pair of tasks that overlap in time."""
        warnings = []
        for i in range(len(self.tasks)):
            for task2 in self.tasks[i + 1:]:
                task1 = self.tasks[i]
                if task1.date == task2.date and _tasks_overlap(task1, task2):
                    warnings.append(
                        f"Warning: '{task1.title}' ({task1.pet_name}) and "
                        f"'{task2.title}' ({task2.pet_name}) overlap on {task1.date}."
                    )
        return warnings

    def sort_by_time(self) -> None:
        """Sort the tasks by their time."""
        self.tasks.sort(key=lambda task: (task.date, task.time))