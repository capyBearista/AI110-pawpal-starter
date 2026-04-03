from dataclasses import dataclass, field
from datetime import date


@dataclass
class Owner:
    name: str
    available_minutes: int


@dataclass
class Pet:
    name: str
    age: int
    weight: float
    breed: str


@dataclass
class Task:
    title: str
    priority: int          # lower number = higher priority (e.g. 1 is most urgent)
    duration_in_minutes: int
    date: date


@dataclass
class Scheduler:
    owner: Owner
    pet_involved: Pet
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        self.tasks.append(task)

    def build_schedule(self) -> list[Task]:
        """Return a prioritized list of tasks that fits within the owner's available time."""
        return []
