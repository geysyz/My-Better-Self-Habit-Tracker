from datetime import date

from app import create_app
from habit_tracker.tracker import HabitTracker
from tests.fakes import FakeStorage


def make_client():
    app = create_app(HabitTracker(FakeStorage()), today_fn=lambda: date(2026, 11, 10))
    app.config["TESTING"] = True
    return app.test_client()


def test_add_habit_appears_on_page():
    client = make_client()
    response = client.post("/habits", data={"name": "Drink water", "category": "Health",
                                            "frequency": "daily"}, follow_redirects=True)
    assert b"Drink water" in response.data


def test_empty_name_shows_error():
    response = make_client().post("/habits", data={"name": "  "}, follow_redirects=True)
    assert b"cannot be empty" in response.data


def test_done_button_marks_habit_and_blocks_duplicate():
    client = make_client()
    client.post("/habits", data={"name": "Read", "category": "L", "frequency": "daily"})
    first = client.post("/habits/1/done", follow_redirects=True)
    assert b"marked done" in first.data
    second = client.post("/habits/1/done", follow_redirects=True)
    assert b"already done" in second.data