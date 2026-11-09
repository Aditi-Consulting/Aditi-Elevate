"""Collect student marks, calculate grades, and report the top performer."""

from typing import Dict, Mapping, Optional, Tuple, TypedDict


SUBJECTS = ("English", "Maths", "Environment", "Gujarati")


class StudentRecord(TypedDict):
    marks: Dict[str, int]
    total: int
    average: float
    grade: str


def calculate_total(marks: Mapping[str, int]) -> int:
    """Return the sum of the subject marks."""
    return sum(marks.values())


def calculate_average(marks: Mapping[str, int]) -> float:
    """Return the average subject mark, or raise if no marks were provided."""
    if not marks:
        raise ValueError("Cannot calculate an average without any marks.")
    return calculate_total(marks) / len(marks)


def assign_grade(average: float) -> str:
    """Assign a letter grade using the original program's grade thresholds."""
    if average >= 100:
        return "A"
    if average >= 80:
        return "B"
    if average >= 60:
        return "C"
    if average >= 40:
        return "D"
    return "F"


def get_valid_mark(subject: str) -> int:
    """Prompt until the user enters an integer mark from 0 through 100."""
    while True:
        try:
            mark = int(input("Enter marks for {}: ".format(subject)))
        except ValueError:
            print("Please enter a whole number between 0 and 100.")
            continue

        if 0 <= mark <= 100:
            return mark
        print("Please enter marks between 0 and 100.")


def create_student_record(marks: Mapping[str, int]) -> StudentRecord:
    """Build a student's marks, total, average, and grade."""
    marks_by_subject = dict(marks)
    average = calculate_average(marks_by_subject)
    return {
        "marks": marks_by_subject,
        "total": calculate_total(marks_by_subject),
        "average": average,
        "grade": assign_grade(average),
    }


def find_top_student(
    students: Mapping[str, StudentRecord],
) -> Optional[Tuple[str, StudentRecord]]:
    """Return the student with the highest total, or None for no students."""
    if not students:
        return None
    return max(students.items(), key=lambda item: item[1]["total"])


def main() -> None:
    """Collect and display student results until a blank name is entered."""
    students: Dict[str, StudentRecord] = {}
    print("Enter each student's marks. Leave the name blank when finished.")

    while True:
        name = input("Enter student name (or press Enter to finish): ").strip()
        if not name:
            break
        if name in students:
            print("That student name has already been entered.")
            continue

        marks = {subject: get_valid_mark(subject) for subject in SUBJECTS}
        record = create_student_record(marks)
        students[name] = record
        print(
            "{}: total {}, average {:.2f}, grade {}".format(
                name, record["total"], record["average"], record["grade"]
            )
        )

    top_student = find_top_student(students)
    if top_student is None:
        print("No student data was entered.")
        return

    name, record = top_student
    print(
        "Highest-performing student: {} with {} total marks "
        "(average {:.2f}, grade {}).".format(
            name, record["total"], record["average"], record["grade"]
        )
    )


if __name__ == "__main__":
    main()
