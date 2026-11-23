import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from habit_tracker.repository import HabitRepository
from habit_tracker.tracker import HabitTracker, get_today

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "habits.json")


def create_app(tracker=None, today_fn=get_today):
    """The tracker and the clock are injected so tests can fake both."""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
    tracker = tracker or HabitTracker(HabitRepository(DATA_FILE))

    @app.get("/")
    def index():
        today = today_fn()
        rows = []
        for h in tracker.list_habits():
            streak = h.current_streak(today) if h.frequency == "daily" else None
            rows.append({"habit": h, "streak": streak, "done": h.is_done_on(today)})
        return render_template("index.html", rows=rows, today=today)

    @app.post("/habits")
    def add_habit():
        habit, error = tracker.add_habit(
            request.form.get("name", ""),
            request.form.get("category", ""),
            request.form.get("frequency", "daily"),
        )
        flash(error or f"Added '{habit.name}'.", "error" if error else "ok")
        return redirect(url_for("index"))

    @app.post("/habits/<int:habit_id>/done")
    def mark_done(habit_id):
        ok, message = tracker.mark_done(habit_id, today_fn())
        flash(message, "ok" if ok else "error")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)