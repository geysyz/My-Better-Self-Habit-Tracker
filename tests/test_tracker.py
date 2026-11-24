from datetime import date

from habit_tracker.tracker import HabitTracker
from tests.fakes import FakeStorage

TODAY = date(2026, 11, 10)


def test_add_habit_saves_to_storage():
    storage = FakeStorage()
    habit, error = HabitTracker(storage).add_habit("Drink water", "Health", "daily")
    assert error is None
    assert len(storage.habits) == 1 and habit.name == "Drink water"


def test_empty_name_rejected():
    storage = FakeStorage()
    habit, error = HabitTracker(storage).add_habit("   ", "Health", "daily")
    assert habit is None and "empty" in error
    assert storage.habits == []


def test_mark_done_twice_is_rejected():
    tracker = HabitTracker(FakeStorage())
    habit, _ = tracker.add_habit("Read", "Learning", "daily")
    assert tracker.mark_done(habit.id, TODAY)[0] is True
    ok, message = tracker.mark_done(habit.id, TODAY)
    assert ok is False and "already done" in message

def test_add_excused_period_is_saved():
    storage = FakeStorage()
    tracker = HabitTracker(storage)
    period, error = tracker.add_excused_period(
        date(2026, 11, 11), date(2026, 11, 13), "Vacation", TODAY)
    assert error is None and len(storage.periods) == 1


def test_invalid_period_is_not_saved():
    storage = FakeStorage()
    period, error = HabitTracker(storage).add_excused_period(
        date(2026, 11, 13), date(2026, 11, 11), "Vacation", TODAY)
    assert period is None and storage.periods == []