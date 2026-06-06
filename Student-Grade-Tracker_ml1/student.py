class InvalidScoreError(Exception):
    pass

class Student:
    school = "AI Engineering Institute"

    def __init__(self, name, sudent_id, age):
        self.name = name
        self.student_id = sudent_id
        self.age = age
        self.grades: dict[str, list[float]] = {}  #{key, value} <- dictionary

    def add_grade(self, subject: str, score: float):
        if not isinstance(score, (float, int)):
            raise TypeError(f"Score must be a number, got {type(score).__name__!r}")
        
        if not (0<=score<=100):
            raise InvalidScoreError(f"Score {score} is invalid. Must be in between 0 to 100")
        
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(float(score))

    def remove_last_grade(self, subject: str) -> float | None:
        subject = subject.strip().title()
        if subject in self.grades and self.grades[subject]:
            return self.grades[subject].pop()
        return None


    def subject_average(self, subject: str) -> float:
        subject = subject.strip().title()
        if subject not in self.grades or not self.grades[subject]:
            return 0.0
        scores = self.grades[subject]
        return round(sum(scores)/len(scores), 2)
    
    def overall_average(self) -> float:
        all_scores = [s for scores in self.grades.values() for s in scores]
#         [ new_item 
#           for outer_loop 
#           for inner_loop]

        if not all_scores:
            return 0.0
        return round(sum(all_scores) / len(all_scores) , 2)
    
    def letter_grade(self) -> str:
        avgNo = self.overall_average()

        if(avgNo >= 90): return "A"
        elif(avgNo >= 80): return "B"
        elif(avgNo >= 70): return "C"
        elif(avgNo >= 60): return "D"
        return "F"
    
    def top_subject(self) -> str:
        if not self.grades:
            return "N/A"
        return max(self.grades, key=self.subject_average) #max(iterable, key=function)

    def weakest_subject(self) -> str:
        if not self.grades:
            return "N/A"
        return min(self.grades, key=self.subject_average)

    def total_scores_entered(self) -> int:
        return sum(len(v) for v in self.grades.values())

    def to_dict(self) ->dict:
        return {
            "name": self.name,
            "student_id": self.student_id,
            "age": self.age,
            "grades": self.grades
        }
# ------------// Class Method VS Instance Method //--------------------
# Instance method (self)
# “I am a student, I can update my grades”
# Class method (cls)
# “I am the Student class, I can create new students”

    @classmethod
    def from_dict(cls, data: dict) -> "Student": #can create object from json directly
        student = cls(data["name"], data["student_id"], data["age"])
        student.grades = data.get("grades", {}) #if grades missing then it return empty
        return student

    # modifiying how print(student) will look like
    def __str__(self) ->str:
        return (f"Student(name={self.name!r}, id={self.student_id!r}, "
                f"avg={self.overall_average()}, grade={self.letter_grade()!r})")

    #dev
    def __repr__(self):
        return f"Student(name={self.name!r}, student_id={self.student_id!r}, age={self.age})"

    #Terminal Display
    def report(self) -> None:
        width = 42
        print(f"\n{'═' * width}")
        print(f"  {self.school}")
        print(f"{'─' * width}")
        print(f"  Name       : {self.name}")
        print(f"  Student ID : {self.student_id}")
        print(f"  Age        : {self.age}")
        print(f"{'─' * width}")

        if not self.grades:
            print("  No grades recorded yet.")
        else:
            #:<16 align to the left and take 16 spaces total, :>5 align to the right and take total 5 spaces 
            print(f"  {'Subject':<16} {'Scores':<16} {'Avg':>5}")
            print(f"  {'─'*16} {'─'*16} {'─'*5}")
            for subject, scores in self.grades.items():
                avg = self.subject_average(subject)
                scores_str = str(scores)
              
                if len(scores_str) > 15:
                    scores_str = scores_str[:12] + "..." #:12 -> take only first 12 characters
                print(f"  {subject:<16} {scores_str:<16} {avg:>5}")

        print(f"{'─' * width}")
        print(f"  Overall Average : {self.overall_average()}")
        print(f"  Letter Grade    : {self.letter_grade()}")
        print(f"  Top Subject     : {self.top_subject()}")
        print(f"  Needs Work      : {self.weakest_subject()}")
        print(f"  Total Scores    : {self.total_scores_entered()}")
        print(f"{'═' * width}\n")
