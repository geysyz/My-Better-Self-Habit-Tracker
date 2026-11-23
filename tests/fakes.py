from habit_tracker.storage import HabitStorage


class FakeStorage(HabitStorage):
    """In-memory storage so tests never touch the disk."""

    def __init__(self, habits=None):
        self.habits = list(habits or [])

    def load(self):
        return list(self.habits)

    def save(self, habits):
        self.habits = list(habits)