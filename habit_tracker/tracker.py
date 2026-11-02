import os
from datetime import date

from .habit import Habit

VALID_FREQUENCIES = ("daily", "weekly")


def get_today():
    """Today's date. HABIT_TODAY=YYYY-MM-DD overrides it for testing."""
    override = os.environ.get("HABIT_TODAY")
    if override:
        try:
            return date.fromisoformat(override)
        except ValueError:
            pass  # invalid override: fall back to the real date
    return date.today()


class HabitTracker:
    """Application logic. Never prints; returns values and messages."""

    def __init__(self, repository):
        self.repository = repository
        self.habits = repository.load()

    def list_habits(self):
        return list(self.habits)

    def get_habit(self, habit_id):
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None

    def add_habit(self, name, category, frequency):
        """Returns (habit, None) on success or (None, error_message)."""
        name = name.strip()
        category = category.strip() or "General"
        frequency = frequency.strip().lower() or "daily"

        if not name:
            return None, "Habit name cannot be empty."
        if frequency not in VALID_FREQUENCIES:
            return None, "Frequency must be 'daily' or 'weekly'."

        next_id = max((h.id for h in self.habits), default=0) + 1
        habit = Habit(next_id, name, category, frequency)
        self.habits.append(habit)
        self.repository.save(self.habits)
        return habit, None

    def mark_done(self, habit_id, today):
        """Returns (success, message)."""
        habit = self.get_habit(habit_id)
        if habit is None:
            return False, "No habit with that number."
        if not habit.mark_done(today):
            return False, f"'{habit.name}' is already done today."
        self.repository.save(self.habits)
        return True, f"'{habit.name}' marked done for {today.isoformat()}."