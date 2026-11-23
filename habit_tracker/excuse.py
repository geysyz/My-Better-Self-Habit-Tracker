from dataclasses import dataclass
from datetime import date, timedelta

MAX_FUTURE_DAYS = 30
MAX_PAST_DAYS = 3
MAX_PERIOD_DAYS = 14
WARN_AFTER_DAYS = 14


@dataclass
class ExcusedPeriod:
    id: int
    start_date: date
    end_date: date
    reason: str

    def covers(self, day):
        return self.start_date <= day <= self.end_date

    def length_days(self):
        return (self.end_date - self.start_date).days + 1

    def to_dict(self):
        return {"id": self.id, "start_date": self.start_date.isoformat(),
                "end_date": self.end_date.isoformat(), "reason": self.reason}

    @staticmethod
    def from_dict(d):
        return ExcusedPeriod(d["id"], date.fromisoformat(d["start_date"]),
                             date.fromisoformat(d["end_date"]), d["reason"])


class ExcusePolicy:
    """Rules for excused periods. No file access, no printing."""

    def validate(self, start, end, reason, today, existing):
        """Return an error message, or None if the period is allowed."""
        if not reason.strip():
            return "Reason cannot be empty."
        if end < start:
            return "End date cannot be before start date."
        if start > today + timedelta(days=MAX_FUTURE_DAYS):
            return f"Start date can be at most {MAX_FUTURE_DAYS} days in the future."
        if start < today - timedelta(days=MAX_PAST_DAYS):
            return f"Start date can be at most {MAX_PAST_DAYS} days in the past."
        if (end - start).days + 1 > MAX_PERIOD_DAYS:
            return f"An excused period can be at most {MAX_PERIOD_DAYS} days."
        for p in existing:
            if start <= p.end_date and end >= p.start_date:
                return "This overlaps an existing excused period."
        return None

    def is_excused(self, day, periods):
        return any(p.covers(day) for p in periods)

    def should_warn(self, periods, today):
        """R8: soft warning if many excused days were logged recently."""
        cutoff = today - timedelta(days=29)
        total = sum(p.length_days() for p in periods if p.start_date >= cutoff)
        return total > WARN_AFTER_DAYS