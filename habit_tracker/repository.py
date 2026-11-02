import json
import os

from .habit import Habit


class HabitRepository:
    """Loads and saves habits to a JSON file."""

    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Habit.from_dict(item) for item in data]

    def save(self, habits):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([h.to_dict() for h in habits], f, indent=2)