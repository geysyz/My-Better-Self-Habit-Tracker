import json
import os

from .excuse import ExcusedPeriod
from .habit import Habit
from .storage import HabitStorage


class HabitRepository(HabitStorage):
    """Loads and saves habits and excused periods in one JSON file."""

    def __init__(self, path):
        self.path = path

    def _read(self):
        if not os.path.exists(self.path):
            return {"habits": [], "excused_periods": []}
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):          # Sprint 1 file format
            data = {"habits": data}
        data.setdefault("habits", [])
        data.setdefault("excused_periods", [])
        return data

    def _write(self, data):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        return [Habit.from_dict(d) for d in self._read()["habits"]]

    def save(self, habits):
        data = self._read()
        data["habits"] = [h.to_dict() for h in habits]
        self._write(data)

    def load_periods(self):
        return [ExcusedPeriod.from_dict(d) for d in self._read()["excused_periods"]]

    def save_periods(self, periods):
        data = self._read()
        data["excused_periods"] = [p.to_dict() for p in periods]
        self._write(data)