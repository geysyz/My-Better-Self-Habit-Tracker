from datetime import date, timedelta


class Habit:
    """A habit and the dates on which it was completed."""

    def __init__(self, id, name, category, frequency, completed_dates=None):
        self.id = id
        self.name = name
        self.category = category
        self.frequency = frequency
        self.completed_dates = set(completed_dates or [])

    def is_done_on(self, day):
        return day in self.completed_dates

    def mark_done(self, day):
        """Mark done for the given day. Returns False if already done."""
        if day in self.completed_dates:
            return False
        self.completed_dates.add(day)
        return True
    
    def current_streak(self, today):
        """Consecutive days completed, ending today (or yesterday if
        today is not done yet, since the day isn't over)."""
        day = today if today in self.completed_dates else today - timedelta(days=1)
        streak = 0
        while day in self.completed_dates:
            streak += 1
            day -= timedelta(days=1)
        return streak

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "frequency": self.frequency,
            "completed_dates": sorted(d.isoformat() for d in self.completed_dates),
        }

    @staticmethod
    def from_dict(data):
        dates = [date.fromisoformat(d) for d in data.get("completed_dates", [])]
        return Habit(
            data["id"],
            data["name"],
            data["category"],
            data["frequency"],
            dates,
        )