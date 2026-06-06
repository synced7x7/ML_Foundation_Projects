"""
test_tracker.py
---------------
Tests for the Student Grade Tracker.
Run with:  python test_tracker.py

Tests are written manually (no external library needed)
so you can run them immediately without installing anything.
This is great practice before you learn pytest in a later phase.
"""

import os
import json
from student import Student, InvalidScoreError
from tracker import StudentTracker

# ------------------------------------------------------------------ #
#  Tiny test framework                                                 #
# ------------------------------------------------------------------ #

passed = 0
failed = 0


def test(name: str, condition: bool) -> None:
    global passed, failed
    if condition:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  FAILED: {name}")
        failed += 1


def raises(exception, fn, *args, **kwargs) -> bool:
    """Return True if fn(*args) raises the expected exception."""
    try:
        fn(*args, **kwargs)
        return False
    except exception:
        return True


# ------------------------------------------------------------------ #
#  Student tests                                                       #
# ------------------------------------------------------------------ #

print("\n── Student class ─────────────────────────────────────\n")

s = Student("Ayan", "AI-001", 21)

test("student name set correctly",      s.name == "Ayan")
test("student ID set correctly",        s.student_id == "AI-001")
test("student age set correctly",       s.age == 21)
test("grades start empty",             s.grades == {})
test("overall average is 0 with no grades", s.overall_average() == 0.0)
test("letter grade is F with no grades",    s.letter_grade() == "F")

s.add_grade("Python", 90)
s.add_grade("Python", 80)
s.add_grade("Math", 70)

test("grade added to correct subject",  "Python" in s.grades)
test("subject stores correct scores",   s.grades["Python"] == [90.0, 80.0])
test("subject average correct",        s.subject_average("Python") == 85.0)
test("overall average correct",        s.overall_average() == 80.0)
test("letter grade B for avg 80",      s.letter_grade() == "B")
test("top subject is Python",          s.top_subject() == "Python")
test("weakest subject is Math",        s.weakest_subject() == "Math")
test("total scores counted correctly", s.total_scores_entered() == 3)

test("invalid score raises error",
     raises(InvalidScoreError, s.add_grade, "Python", 150))
test("negative score raises error",
     raises(InvalidScoreError, s.add_grade, "Python", -1))
test("non-number score raises TypeError",
     raises(TypeError, s.add_grade, "Python", "ninety"))

removed = s.remove_last_grade("Python")
test("remove_last_grade returns correct value", removed == 80.0)
test("grade list shortened after removal",      len(s.grades["Python"]) == 1)

# serialization round-trip
d = s.to_dict()
s2 = Student.from_dict(d)
test("from_dict name matches",   s2.name == s.name)
test("from_dict grades match",   s2.grades == s.grades)
test("from_dict avg matches",    s2.overall_average() == s.overall_average())

# grade boundaries
s3 = Student("Boundary", "TEST-1", 20)
s3.add_grade("X", 0)
test("score of 0 is valid",   0.0 in s3.grades["X"])
s3.add_grade("X", 100)
test("score of 100 is valid", 100.0 in s3.grades["X"])

# letter grade boundaries
def avg_to_grade(avg):
    s = Student("T", "T", 20)
    s.add_grade("X", avg)
    return s.letter_grade()

test("avg 90 → A", avg_to_grade(90) == "A")
test("avg 89 → B", avg_to_grade(89) == "B")
test("avg 80 → B", avg_to_grade(80) == "B")
test("avg 79 → C", avg_to_grade(79) == "C")
test("avg 70 → C", avg_to_grade(70) == "C")
test("avg 69 → D", avg_to_grade(69) == "D")
test("avg 59 → F", avg_to_grade(59) == "F")


# ------------------------------------------------------------------ #
#  StudentTracker tests                                                #
# ------------------------------------------------------------------ #

print("\n── StudentTracker class ──────────────────────────────\n")

TEST_FILE = "test_students.json"

# clean up from previous runs
if os.path.exists(TEST_FILE):
    os.remove(TEST_FILE)

tracker = StudentTracker(filepath=TEST_FILE)

test("starts with zero students",       len(tracker) == 0)
test("class average is 0 with no data", tracker.class_average() == 0.0)
test("top student is None when empty",  tracker.top_student() is None)

r1 = tracker.add_student("Ayan", "AI-001", 21)
r2 = tracker.add_student("Rafi", "AI-002", 22)
test("add_student returns True on success",        r1 is True)
test("tracker has 2 students after adding",        len(tracker) == 2)
test("duplicate ID rejected",
     tracker.add_student("Other", "AI-001", 20) is False)

test("get_student finds by ID",    tracker.get_student("AI-001").name == "Ayan")
test("get_student returns None for missing ID", tracker.get_student("NONE") is None)
test("IDs normalized to uppercase",
     tracker.get_student("ai-001").name == "Ayan")

tracker.add_grade("AI-001", "Python", 95)
tracker.add_grade("AI-001", "Python", 85)
tracker.add_grade("AI-001", "Math",   75)
tracker.add_grade("AI-002", "Python", 60)

test("grade added correctly",  tracker.get_student("AI-001").subject_average("Python") == 90.0)
test("top student is Ayan",    tracker.top_student().name == "Ayan")
test("class average computed", tracker.class_average() == round(
    (tracker.get_student("AI-001").overall_average() +
     tracker.get_student("AI-002").overall_average()) / 2, 2))

sorted_students = tracker.students_by_average()
test("students sorted by avg descending", sorted_students[0].name == "Ayan")

test("search by grade B returns Ayan",
     any(s.name == "Ayan" for s in tracker.students_by_grade("B")))

r3 = tracker.remove_student("AI-002")
test("remove_student returns True",  r3 is True)
test("tracker has 1 student after removal", len(tracker) == 1)
test("remove non-existent returns False",
     tracker.remove_student("GHOST") is False)

# persistence — save and reload
tracker2 = StudentTracker(filepath=TEST_FILE)
test("data persists across reload",      len(tracker2) == 1)
test("student data correct after reload",
     tracker2.get_student("AI-001").name == "Ayan")
test("grades survive reload",
     tracker2.get_student("AI-001").subject_average("Python") == 90.0)

# CSV export
tracker3 = StudentTracker(filepath=TEST_FILE)
tracker3.export_csv("test_export.csv")
test("CSV file created", os.path.exists("test_export.csv"))

tracker3.export_detailed_csv("test_detailed.csv")
test("Detailed CSV file created", os.path.exists("test_detailed.csv"))

# undo grade
tracker3.add_grade("AI-001", "Python", 70)
avg_before = tracker3.get_student("AI-001").subject_average("Python")
tracker3.undo_last_grade("AI-001", "Python")
avg_after = tracker3.get_student("AI-001").subject_average("Python")
test("undo_last_grade restores previous average", avg_before != avg_after)


# ------------------------------------------------------------------ #
#  Cleanup test files                                                  #
# ------------------------------------------------------------------ #

for f in [TEST_FILE, "test_export.csv", "test_detailed.csv"]:
    if os.path.exists(f):
        os.remove(f)


# ------------------------------------------------------------------ #
#  Summary                                                             #
# ------------------------------------------------------------------ #

total = passed + failed
print(f"\n── Results ───────────────────────────────────────────\n")
print(f"  {passed}/{total} tests passed", end="")
if failed == 0:
    print("  ✓  All tests passed!\n")
else:
    print(f"  —  {failed} test(s) failed\n")
