from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


def _validate_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("Student name cannot be empty.")
    return cleaned


def _validate_mark(mark: float) -> float:
    try:
        value = float(mark)
    except (TypeError, ValueError) as exc:
        raise ValueError("Marks must be numbers.") from exc

    if value < 0 or value > 100:
        raise ValueError("Each mark must be between 0 and 100.")

    return value


def calculate_average(marks: Iterable[float]) -> float:
    values = list(marks)
    if not values:
        raise ValueError("At least one mark is required to calculate an average.")
    return round(sum(values) / len(values), 2)


def determine_grade(average_mark: float) -> str:
    if average_mark >= 90:
        return "A"
    if average_mark >= 75:
        return "B"
    if average_mark >= 60:
        return "C"
    if average_mark >= 50:
        return "D"
    return "F"


@dataclass
class Student:
    name: str
    marks: List[float] = field(default_factory=list)

    def __post_init__(self):
        self.name = _validate_name(self.name)
        cleaned_marks = []
        for mark in self.marks:
            cleaned_marks.append(_validate_mark(mark))
        self.marks = cleaned_marks

    @property
    def average(self) -> float:
        return calculate_average(self.marks)

    @property
    def grade(self) -> str:
        return determine_grade(self.average)


def format_results(students: Iterable[Student]) -> str:
    rows = ["Student Name | Marks | Average | Grade"]
    for student in students:
        marks_text = ", ".join(str(mark) for mark in student.marks)
        rows.append(f"{student.name} | {marks_text} | {student.average:.2f} | {student.grade}")
    return "\n".join(rows)


def collect_students() -> list[Student]:
    students: list[Student] = []
    print("Type 'done' when you have finished adding students.")

    while True:
        student_name = input("Student name: ").strip()
        if student_name.lower() in {"", "done", "exit", "quit"}:
            if students:
                break
            print("You need to add at least one student before finishing.")
            continue

        marks: list[float] = []
        while True:
            raw_mark = input(
                f"Enter a mark for {student_name} (or type 'done' to finish this student): "
            ).strip()

            if raw_mark.lower() in {"done", "exit", "quit"}:
                if marks:
                    break
                print("Please enter at least one valid mark before finishing this student.")
                continue

            try:
                marks.append(_validate_mark(raw_mark))
            except ValueError as exc:
                print(f"Invalid input: {exc} Please enter a value between 0 and 100.")
                continue

        try:
            students.append(Student(student_name, marks))
        except ValueError as exc:
            print(f"Invalid student record: {exc}")

    return students


def main() -> None:
    print("Student Grade Manager")
    print("=" * 22)

    try:
        students = collect_students()
    except KeyboardInterrupt:
        print("\nProgram cancelled by user.")
        return

    if not students:
        print("No student records were entered.")
        return

    print("\nGrade Summary")
    print("-" * 22)
    print(format_results(students))


if __name__ == "__main__":
    main()
