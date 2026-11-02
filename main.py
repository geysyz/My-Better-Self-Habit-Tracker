import os

from habit_tracker.repository import HabitRepository
from habit_tracker.tracker import HabitTracker, get_today

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "habits.json")

MENU = """
=== My Better Self ===
1. Add a habit
2. Mark a habit done today
3. View habits and streaks
4. Quit
"""


def add_habit_flow(tracker):
    name = input("Habit name: ")
    category = input("Category (e.g., Health): ")
    frequency = input("Frequency (daily/weekly) [daily]: ")
    habit, error = tracker.add_habit(name, category, frequency)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Added '{habit.name}'.")


def show_habits(tracker, today):
    habits = tracker.list_habits()
    if not habits:
        print("No habits yet. Choose 1 to add one.")
        return
    print(f"\nToday: {today.isoformat()}")
    for h in habits:
        status = "done today" if h.is_done_on(today) else "not done today"
        if h.frequency == "daily":
            streak = f"{h.current_streak(today)} day(s)"
        else:
            streak = "not available yet (weekly)"
        print(f"{h.id}. {h.name} [{h.category}, {h.frequency}] "
              f"- streak: {streak} - {status}")


def mark_done_flow(tracker, today):
    if not tracker.list_habits():
        print("No habits yet. Choose 1 to add one.")
        return
    show_habits(tracker, today)
    choice = input("Number of the habit to mark done: ")
    try:
        habit_id = int(choice)
    except ValueError:
        print("Error: please enter a number.")
        return
    _, message = tracker.mark_done(habit_id, today)
    print(message)


def main():
    tracker = HabitTracker(HabitRepository(DATA_FILE))
    while True:
        today = get_today()
        print(MENU)
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            add_habit_flow(tracker)
        elif choice == "2":
            mark_done_flow(tracker, today)
        elif choice == "3":
            show_habits(tracker, today)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()