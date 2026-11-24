# My Better Self - Habit Tracker

A habit tracker that runs in a web browser. Users record daily habits,
mark them done, see their current streaks, and log excused periods such as
vacations.

Author: Geysa Tumea
**Current version:** Sprint 2

## Purpose

Users create habits (such as drinking water or reading), mark them done each
day, and see how many consecutive days they have kept each habit going. The
streak gives visible proof of progress to keep users motivated.

## Technologies

- Python 3.10 or newer
- Flask (web framework)
- pytest (automated tests)
- Data stored in a local JSON file
- Developed in Visual Studio Code on macOS

## Prerequisites

- Python 3.10 or newer (check with `python3 --version`)
- pip, which is included with Python (check with `python3 -m pip --version`)
- Git, to clone the repository
- A web browser (Chrome, Firefox, Safari, or Edge)

## Installation

Run these commands in a terminal.

1. Clone the repository and enter the project folder:
   ```bash
   git clone https://github.com/geysyz/My-Better-Self-Habit-Tracker.git
   cd My-Better-Self-Habit-Tracker
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   (On Windows: `.venv\Scripts\activate`.) Your prompt should now start with `(.venv)`.
3. Install the dependencies (Flask and pytest):
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

No configuration is required.

Optional: set the `HABIT_TODAY` environment variable to pretend today is a
different date (format `YYYY-MM-DD`). This is used to test streaks without
waiting several days.
- `HABIT_TODAY=YYYY-MM-DD` pretends today is a different date. Used to test
  streaks and excused-period rules without waiting for real days to pass.
- `SECRET_KEY` sets the key Flask uses for status messages. A development
  default is used if it is not set.

## Running the application

Make sure the virtual environment is active, then, from the project root
(the folder containing `app.py`):

```bash
python3 app.py
```

Open **http://127.0.0.1:5000** in your browser. You should see the
"My Better Self" page with an "Add a habit" form, an "Excused periods"
form, and your habit list. Press Ctrl+C in the terminal to stop the server.

To run with a fixed date (used in the examples below):

```bash
HABIT_TODAY=2026-11-10 python3 app.py
```

Habits and excused periods are saved to `data/habits.json`, which is
created automatically.

The Sprint 1 console interface is still available with `python3 main.py`
(see "Console interface (Sprint 1)" below). It does not support excused periods.

From the project root folder (the one containing `main.py`):

```bash
python3 main.py
```

You should see the main menu:

```
=== My Better Self ===
1. Add a habit
2. Mark a habit done today
3. View habits and streaks
4. Quit
```

Habits are saved to `data/habits.json`, which is created automatically on the
first run.

'''Still works; run with python3 main.py from the project root'''
## Console interface (Sprint 1)

**1. Add a habit (US-01)**
1. Run `python3 main.py` and choose **1**.
2. Enter name `Drink water`, category `Health`, frequency `daily`.
3. Choose **3**. The habit appears with a streak of 0.
4. Try adding a habit with an empty name or only spaces. An error message appears and nothing is added.
5. Choose **4** to quit, run the program again, and choose **3**. The habit is still there.

**2. Mark a habit done (US-02)**
1. Choose **2** and select "Drink water". It is marked done for today.
2. Choose **2** and select it again. The program reports it is already done today.
3. Choose **3**. The habit shows as done today with a streak of 1.

**3. Check streaks with sample data (US-03)**
1. Copy the sample data:
   ```bash
   cp data/sample_habits.json data/habits.json
   ```
2. Run with a fixed date so the sample streaks line up:
   ```bash
   HABIT_TODAY=2026-11-05 python3 main.py
   ```
3. Choose **3**. Expected streaks: "Drink water" = 3, "Read a book" = 0 because of a gap

## Project structure

```
app.py               Flask web app (routes)
templates/
  index.html         Page template
habit_tracker/
  habit.py           Habit class (completion dates, streak)
  excuse.py          ExcusedPeriod and ExcusePolicy (rules for excused periods)
  storage.py         HabitStorage interface (abstraction)
  repository.py      JSON file storage
  tracker.py         Application logic
main.py              Console menu (Sprint 1)
tests/               Automated tests (pytest)
data/
  sample_habits.json Fictional sample data
```

## Trying the Sprint 2 functionality

Start from a clean state (this only deletes your local, git-ignored data file):

```bash
rm -f data/habits.json
HABIT_TODAY=2026-11-10 python3 app.py
```

Then open http://127.0.0.1:5000. The page should show "Today: 2026-11-10".

### US-04: Use the app in a browser

1. In "Add a habit", enter name `Drink water`, category `Health`,
   frequency `daily`, and click **Add**. Message "Added 'Drink water'." appears
   and the habit shows with "Streak: 0 day(s)".
2. Click **Add** with the name left empty (or only spaces). The message
   "Habit name cannot be empty." appears and no habit is added.
3. Click **Done** on Drink water. The habit shows "Done today" with a
   streak of 1.
4. Stop the server (Ctrl+C), start it again with the same command, and reload
   the page. The habit is still there and still done today.

### US-06: Log an excused period

1. In "Excused periods", enter reason `Vacation`, start `2026-11-11`,
   end `2026-11-13`, and click **Add**. The message "Excused period added."
   appears and the period is listed.
2. Try end `2026-11-10` with start `2026-11-12`.
   Expected: "End date cannot be before start date."
3. Try start `2026-12-20`. Expected: a "too far in the future" message
   (limit: 30 days ahead).
4. Try start `2026-11-06`. Expected: a "too far in the past" message
   (limit: 3 days back).
5. Try start `2026-11-10`, end `2026-11-25`. Expected: "An excused period can
   be at most 14 days."
6. Try start `2026-11-13`, end `2026-11-15`. Expected: an overlap message,
   because Vacation already covers Nov 13.
7. Try an empty reason. Expected: "Reason cannot be empty."
8. Restart the server and reload. The Vacation period is still listed.

Rejected entries are never added to the list.

## Running the automated tests

From the project root, with the virtual environment active:

```bash
python3 -m pytest
```

Expected result: all tests pass (for example, `15 passed`). Use
`python3 -m pytest`, not bare `pytest`, so the imports resolve.

## Known limitations (Sprint 2)

- Habits cannot be deleted or edited yet (planned: US-05).
- Excused periods can be logged, but they do **not** yet change streak
  calculations. The streak-freeze rule (US-07) is not implemented.
- Excused periods apply to all habits; they cannot be set per habit.
- Streaks are calculated for daily habits only.
- No filtering, sorting, or progress reports yet.
- The console interface (`main.py`) does not support excused periods.
- No login; data is stored in a single local file.


## Planned for later sprints

Delete a habit, freeze streaks across excused days, filter by category or
frequency, sort by streak, and completion-percentage reports.