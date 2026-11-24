import os
from datetime import date

from .habit import Habit
from .storage import HabitStorage
from .excuse import ExcusePolicy, ExcusedPeriod

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

    def __init__(self, repository, policy=None):
        self.repository = repository
        self.policy = policy or ExcusePolicy()
        self.habits = repository.load()
        self.periods = repository.load_periods()

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

    def list_periods(self):
        return sorted(self.periods, key=lambda p: p.start_date)

    def add_excused_period(self, start, end, reason, today):
        """Returns (period, None) or (None, error_message)."""
        if start is None or end is None:
            return None, "Please enter valid start and end dates."
        error = self.policy.validate(start, end, reason, today, self.periods)
        if error:
            return None, error
        next_id = max((p.id for p in self.periods), default=0) + 1
        period = ExcusedPeriod(next_id, start, end, reason.strip())
        self.periods.append(period)
        self.repository.save_periods(self.periods)
        return period, None

    def delete_excused_period(self, period_id):
        for p in self.periods:
            if p.id == period_id:
                self.periods.remove(p)
                self.repository.save_periods(self.periods)
                return True, "Excused period deleted."
        return False, "No excused period with that number."

    def excuse_warning(self, today):
        if self.policy.should_warn(self.periods, today):
            return "Heads up: you've logged more than 14 excused days recently."
        return None