"""
main.py
-------
Command-line interface for the Student Grade Tracker.
Run this file to start the program:

    python main.py

All data is automatically saved to students.json and reloaded
on the next run — your data is never lost.
"""

from tracker import StudentTracker
from student import InvalidScoreError


# ------------------------------------------------------------------ #
#  Helper utilities                                                    #
# ------------------------------------------------------------------ #

def divider(char: str = "─", width: int = 44) -> None:
    print(f"\n  {char * width}\n")


def prompt(text: str) -> str:
    """Display a prompt and return stripped user input."""
    return input(f"  {text}").strip()


def prompt_int(text: str) -> int | None:
    """Prompt for an integer. Returns None if input is invalid."""
    raw = prompt(text)
    try:
        return int(raw)
    except ValueError:
        print(f"  [!] '{raw}' is not a valid whole number.")
        return None


def prompt_float(text: str) -> float | None:
    """Prompt for a float. Returns None if input is invalid."""
    raw = prompt(text)
    try:
        return float(raw)
    except ValueError:
        print(f"  [!] '{raw}' is not a valid number.")
        return None


def confirm(text: str) -> bool:
    """Ask a yes/no question. Returns True for 'y'."""
    ans = prompt(f"{text} (y/n): ").lower()
    return ans == "y"


# ------------------------------------------------------------------ #
#  Menu action handlers                                                #
# ------------------------------------------------------------------ #

def handle_add_student(tracker: StudentTracker) -> None:
    divider()
    print("  ADD STUDENT\n")
    name = prompt("Full name      : ")
    sid  = prompt("Student ID     : ")
    age  = prompt_int("Age            : ")

    if not name or not sid or age is None:
        print("  [!] Cancelled — one or more fields were empty or invalid.")
        return

    tracker.add_student(name, sid, age)


def handle_add_grade(tracker: StudentTracker) -> None:
    divider()
    print("  ADD GRADE\n")

    if len(tracker) == 0:
        print("  [!] No students yet. Add a student first.")
        return

    sid     = prompt("Student ID : ")
    subject = prompt("Subject    : ")
    score   = prompt_float("Score      : ")

    if not sid or not subject or score is None:
        print("  [!] Cancelled — one or more fields were empty or invalid.")
        return

    try:
        tracker.add_grade(sid, subject, score)
    except InvalidScoreError as e:
        print(f"  [!] {e}")


def handle_undo_grade(tracker: StudentTracker) -> None:
    divider()
    print("  UNDO LAST GRADE\n")
    sid     = prompt("Student ID : ")
    subject = prompt("Subject    : ")

    if not sid or not subject:
        print("  [!] Cancelled.")
        return

    tracker.undo_last_grade(sid, subject)


def handle_view_student(tracker: StudentTracker) -> None:
    divider()
    print("  VIEW STUDENT REPORT\n")
    sid = prompt("Student ID (or ENTER to list all): ")

    if not sid:
        for s in tracker.students_by_average():
            s.report()
        return

    student = tracker.get_student(sid)
    if student is None:
        print(f"  [!] Student ID '{sid.upper()}' not found.")
        return
    student.report()


def handle_class_report(tracker: StudentTracker) -> None:
    tracker.report()


def handle_search(tracker: StudentTracker) -> None:
    divider()
    print("  SEARCH BY LETTER GRADE\n")
    letter = prompt("Letter grade to find (A/B/C/D/F): ").upper()

    if letter not in ("A", "B", "C", "D", "F"):
        print("  [!] Invalid grade letter.")
        return

    results = tracker.students_by_grade(letter)
    if not results:
        print(f"  No students with grade {letter}.")
        return

    print(f"\n  Students with grade {letter}:\n")
    for s in results:
        print(f"    {s.student_id:<10} {s.name:<20} avg={s.overall_average()}")
    print()


def handle_remove_student(tracker: StudentTracker) -> None:
    divider()
    print("  REMOVE STUDENT\n")
    sid = prompt("Student ID to remove: ")

    if not sid:
        print("  [!] Cancelled.")
        return

    student = tracker.get_student(sid)
    if student is None:
        print(f"  [!] Student ID '{sid.upper()}' not found.")
        return

    if confirm(f"  Are you sure you want to permanently remove {student.name}?"):
        tracker.remove_student(sid)
    else:
        print("  [*] Cancelled.")


def handle_export(tracker: StudentTracker) -> None:
    divider()
    print("  EXPORT\n")
    print("  [1] Summary CSV  (one row per student)")
    print("  [2] Detailed CSV (one row per student-subject)")
    print("  [0] Back\n")

    choice = prompt("Choice: ")
    if choice == "1":
        filename = prompt("Filename (ENTER for 'report.csv'): ") or "report.csv"
        tracker.export_csv(filename)
    elif choice == "2":
        filename = prompt("Filename (ENTER for 'detailed_report.csv'): ") or "detailed_report.csv"
        tracker.export_detailed_csv(filename)
    elif choice == "0":
        return
    else:
        print("  [!] Invalid choice.")


def handle_top_student(tracker: StudentTracker) -> None:
    top = tracker.top_student()
    if top is None:
        print("\n  [!] No students yet.\n")
    else:
        print(f"\n  Top Student : {top.name} — {top.overall_average()} avg ({top.letter_grade()})\n")


# ------------------------------------------------------------------ #
#  Main menu                                                           #
# ------------------------------------------------------------------ #

MENU = """
  ╔══════════════════════════════════════════╗
  ║       STUDENT GRADE TRACKER  v1.0       ║
  ╚══════════════════════════════════════════╝

    [1]  Add student
    [2]  Add grade
    [3]  View student report
    [4]  Class report (all students)
    [5]  Search by letter grade
    [6]  Top student
    [7]  Undo last grade
    [8]  Remove student
    [9]  Export to CSV
    [0]  Quit

"""


def main() -> None:
    tracker = StudentTracker()

    while True:
        print(MENU)
        choice = prompt("Choose an option: ")

        match choice:
            case "1": handle_add_student(tracker)
            case "2": handle_add_grade(tracker)
            case "3": handle_view_student(tracker)
            case "4": handle_class_report(tracker)
            case "5": handle_search(tracker)
            case "6": handle_top_student(tracker)
            case "7": handle_undo_grade(tracker)
            case "8": handle_remove_student(tracker)
            case "9": handle_export(tracker)
            case "0":
                print("\n  Goodbye. Your data is saved.\n")
                break
            case _:
                print("  [!] Invalid option. Enter a number from the menu.")


if __name__ == "__main__":
    main()
