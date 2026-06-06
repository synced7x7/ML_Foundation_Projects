import json
import csv
import os
from datetime import datetime
from student import Student, InvalidScoreError

class StudentTracker:
    def __init__(self, filepath: str = "students.json"):
        self.filepath = filepath
        self.students: dict[str, Student] = {}
        self._load()

    def add_student(self, name: str, student_id: str, age: int) -> bool:
        student_id = student_id.strip().upper()

        if student_id in self.students:
            print(f"Student Id: {student_id} already exists")
            return False
        if not name.strip():
            print(" [!] Name cannot be empty")
            return False
        if not isinstance(age, int) or age<1 or age>120:
            print(" [!] Age must be a whole number between 1 to 120.")
            return False
        
        self.students[student_id] = Student(name.strip().title(), student_id, age)
        self._save()
        print(f"  [+] Added student: {name.strip().title()} (ID: {student_id})")
        return True
    
    def remove_student(self, student_id: str) -> bool:
        student_id = student_id.strip().upper()
        if student_id not in self.students:
            print(f"  [!] Student ID '{student_id}' not found.")
            return False

        name = self.students[student_id].name
        del self.students[student_id]
        self._save()
        print(f"  [-] Removed student: {name} (ID: {student_id})")
        return True
    
    def get_student(self, student_id: str) -> Student | None:
        return self.students.get(student_id.strip().upper())
    
    def add_grade(self, student_id: str, subject: str, score: float) -> bool:
        student = self.get_student(student_id)
        if student is None:
            print(" [!] Student not found")
            return False
        student.add_grade(subject, score)
        self._save()
        print(f"  [+] Added {score} → {subject} for {student.name}")
        return True
    
    def undo_last_grade(self, student_id: str, subject: str) ->bool:
        student = self.get_student(student_id)
        if student is None: 
            print(f" Student ID: {student_id} not found")
            return False
        
        removed = student.remove_last_grade(subject)
        if removed is None: 
            print(f"  [!] No grades to remove for {subject}.")
            return False

        self._save()
        print(f"  [-] Removed last grade ({removed}) from {subject} for {student.name}")
        return True

    def top_student(self) ->Student | None:
        if not self.students:
            return None
        return max(self.students.values(), key = lambda s:s.overall_average())
    
    def students_by_average(self, descending: bool = True) -> list[Student]:
        return sorted(
            self.students.values(),
            key = lambda s:s.overall_average(),
            reverse=descending
        )
    
    def students_by_grade(self, letter:str) -> list[Student]:
        return [s for s in self.students.values() if s.letter_grade() == letter.upper()]
    
    def class_average(self) ->float:
        if not self.students:
            return 0.0
        
        avgs = [s.overall_average() for s in self.students.values()]
        return round(sum(avgs)/len(avgs) , 2)
    
    def _save(self) -> None:
        try:
            data = {sid: student.to_dict() for sid, student in self.students.items()}
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f" [!] Cound not save data: {e}")

    def _load(self) -> None:
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r") as f:
                raw = json.load(f)
            self.students = {
                sid: Student.from_dict(data) for sid, data in raw.items()
            }
            print(f"  [*] Loaded {len(self.students)} student(s) from '{self.filepath}'")
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"  [!] Failed to load data: {e}. Starting fresh.")
            self.students = {}

    def export_csv(self, out_file: str = "report.csv") -> None:
        if not self.students:
            print("  [!] No students to export.")
            return

        try:
            with open(out_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID", "Name", "Age",
                    "Overall Average", "Grade",
                    "Top Subject", "Weakest Subject", "Total Scores"
                ])
                for s in self.students_by_average():
                    writer.writerow([
                        s.student_id, s.name, s.age,
                        s.overall_average(), s.letter_grade(),
                        s.top_subject(), s.weakest_subject(),
                        s.total_scores_entered()
                    ])
            print(f"  [+] Exported CSV → '{out_file}'")
        except IOError as e:
            print(f"  [!] Could not export CSV: {e}")

    def export_detailed_csv(self, out_file: str = "detailed_report.csv") -> None:
        if not self.students:
            print("  [!] No students to export.")
            return

        try:
            with open(out_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Subject", "Scores", "Subject Average"])
                for s in self.students.values():
                    for subject, scores in s.grades.items():
                        writer.writerow([
                            s.student_id, s.name, subject,
                            str(scores), s.subject_average(subject)
                        ])
            print(f"  [+] Exported detailed CSV → '{out_file}'")
        except IOError as e:
            print(f"  [!] Could not export detailed CSV: {e}")


    def report(self) -> None:
        width = 68
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        print(f"\n{'═' * width}")
        print(f"  CLASS REPORT  ·  {len(self.students)} student(s)  ·  {timestamp}")
        print(f"  Class Average : {self.class_average()}")
        print(f"{'─' * width}")

        if not self.students:
            print("  No students registered yet.")
        else:
            print(f"  {'ID':<10} {'Name':<18} {'Avg':>6} {'Grade':>6} "
                  f"{'Top Subject':<16} {'Scores':>6}")
            print(f"  {'─'*10} {'─'*18} {'─'*6} {'─'*6} {'─'*16} {'─'*6}")

            for s in self.students_by_average():
                print(f"  {s.student_id:<10} {s.name:<18} "
                      f"{s.overall_average():>6} {s.letter_grade():>6} "
                      f"{s.top_subject():<16} {s.total_scores_entered():>6}")

        top = self.top_student()
        if top:
            print(f"{'─' * width}")
            print(f"  Top Student : {top.name} ({top.overall_average()} avg)")

        print(f"{'═' * width}\n")

    def __len__(self) -> int:
        return len(self.students)

    def __repr__(self) -> str:
        return f"StudentTracker(students={len(self.students)}, file={self.filepath!r})"





        
    
