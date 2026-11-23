from habit_tracker.storage import HabitStorage


class FakeStorage(HabitStorage):
    """In-memory storage so tests never touch the disk."""

    def __init__(self, habits=None):
        self.habits = list(habits or [])
        self.periods = []

    def load(self):
        return list(self.habits)

    def save(self, habits):
        self.habits = list(habits)

    def load_periods(self):
            return list(self.periods)
    
    def save_periods(self, periods):
        self.periods = list(periods)