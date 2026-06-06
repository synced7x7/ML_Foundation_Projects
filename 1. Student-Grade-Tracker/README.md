# Student Grade Tracker

A command-line application for tracking student grades across multiple subjects.
Built with Python using OOP, file persistence, error handling, and CSV export.

This is a Week 1 portfolio project from my AI Engineering roadmap —
covering Python classes, file I/O, exception handling, and modules.

---

## Features

- Add and remove students with unique IDs
- Record scores per subject (multiple scores per subject supported)
- Undo the last entered grade for any subject
- Compute per-subject average, overall average, and letter grade
- Identify each student's top and weakest subject
- Search students by letter grade
- Sort all students by overall average
- Find the top-performing student in the class
- Auto-save all data to JSON — data persists between sessions
- Export summary and detailed reports to CSV

---

## Project structure

```
grade-tracker/
├── main.py            # CLI entry point — run this
├── student.py         # Student class — core data model
├── tracker.py         # StudentTracker class — manages all students
├── test_tracker.py    # Manual test suite (no external libraries needed)
├── requirements.txt   # No external dependencies
├── .gitignore
└── README.md
```
---
## Sample session

```
  ╔══════════════════════════════════════════╗
  ║       STUDENT GRADE TRACKER  v1.0       ║
  ╚══════════════════════════════════════════╝

    [1]  Add student
    [2]  Add grade
    ...

  Choose an option: 1

  ADD STUDENT

  Full name      : Ayan
  Student ID     : AI-001
  Age            : 21
  [+] Added student: Ayan (ID: AI-001)
```

```
  Choose an option: 4

  ════════════════════════════════════════════════════════════════════
  CLASS REPORT  ·  2 student(s)  ·  2026-04-27 10:32
  Class Average : 84.5
  ────────────────────────────────────────────────────────────────────
  ID         Name               Avg  Grade  Top Subject      Scores
  ────────── ────────────────── ───  ─────  ────────────────  ──────
  AI-001     Ayan               90.0    A   Python               4
  AI-002     Rafi               79.0    C   Statistics           3
  ────────────────────────────────────────────────────────────────────
  Top Student : Ayan (90.0 avg)
  ════════════════════════════════════════════════════════════════════
```

---

## Concepts demonstrated

| Concept | Where |
|---|---|
| Classes, `__init__`, `self` | `student.py` |
| Instance vs class attributes | `Student.school` vs `self.name` |
| `__str__`, `__repr__`, `__len__` | both files |
| `@classmethod` | `Student.from_dict()` |
| Default parameters | `StudentTracker(filepath="students.json")` |
| Custom exceptions | `InvalidScoreError` |
| `try/except/else/finally` | `tracker.py` — `_save()` and `_load()` |
| File I/O — read and write | `tracker.py` |
| JSON serialization | `to_dict()` and `from_dict()` |
| CSV export | `tracker.export_csv()` |
| `__name__ == "__main__"` | `main.py` |
| Pattern matching (`match`) | `main.py` — menu routing |
| Type hints | throughout |
| Docstrings | every class and method |

---

## Author

Built by Ekanto as part of a 12-month AI Engineering learning roadmap.

**Roadmap progress:** Phase 1 — Python & Math Foundations (Week 1 of 8)

---

## License

MIT
