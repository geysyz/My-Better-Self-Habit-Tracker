# My Better Self - Habit Tracker

A command-line habit tracker that helps busy adults build routines by
recording daily habits and showing their current streaks.

## Purpose

Users create habits (such as drinking water or reading), mark them done each
day, and see how many consecutive days they have kept each habit going. The
streak gives visible proof of progress to keep users motivated.

## Technologies

- Python 3.10 or newer
- Standard library only (`datetime`, `json`, `os`); no third-party packages
- Data stored in a local JSON file

## Prerequisites

- Python 3.10+ (check with `python3 --version`)
- Git (only needed to clone the repository)

## Installation

```bash
git clone https://github.com/[YOUR-USERNAME]/[YOUR-REPO].git
cd [YOUR-REPO]
```

No dependencies need to be installed. (`requirements.txt` is included and
currently lists none.)

## Configuration

No configuration is required.

Optional: set the `HABIT_TODAY` environment variable to pretend today is a
different date (format `YYYY-MM-DD`). This is used to test streaks without
waiting several days.

## Running the application

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

## Trying the Sprint 1 functionality

**1. Add a habit (US-01)**
1. Run `python3 main.py` and choose **1**.
2. Enter name `Drink water`, category `Health`, frequency `daily`.
3. Choose **3**. The habit appears with a streak of 0.
4. Try adding a habit with an empty name or only spaces. An error message
   appears and nothing is added.
5. Choose **4** to quit, run the program again, and choose **3**. The habit is
   still there.

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
3. Choose **3**. Expected streaks: [fill in from your sample file, e.g.
   "Drink water" = 3, "Read a book" = 0 because of a gap].

## Project structure

```
habit_tracker/
  habit.py         Habit class (completion dates and streak calculation)
  repository.py    Loads and saves habits to data/habits.json
  tracker.py       Validation and application logic
main.py            Console menu
data/
  sample_habits.json   Fictional sample data
```

## Known limitations (Sprint 1)

- Console interface only; no pages or graphical interface yet.
- Habits cannot be edited or deleted yet.
- No filtering, sorting, or progress reports yet.
- Streaks are calculated for daily habits only; weekly habits can be saved but
  do not have a streak yet.
- The "break bonus" (excused days) is not implemented.
- No login; data is stored in a single local file.

## Planned for later sprints

Edit/delete habits, filter by category or frequency, sort by streak,
completion-percentage reports, and the break-bonus rule.