def calculate_summary(marks: list[float]) -> tuple[float, float]:
    if not marks:
        return 0.0, 0.0
    total = sum(marks)
    average = total / len(marks)
    return total, average


def assign_grades(average: float) -> str:
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_top_scorer(students: list[dict]) -> dict | None:
    if not students:
        return None
    return max(students, key=lambda s: s["average"])


def validate_marks(marks: str) -> float:
    mark = float(marks)
    if mark < 0 or mark > 100:
        raise ValueError("Marks must be between 0 and 100.")
    return mark


def get_valid_mark(subject_num: int) -> float:
    while True:
        raw = input(f"Enter marks for subject {subject_num} (0-100): ").strip()
        try:
            return validate_marks(raw)
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number between 0 and 100.")


def display_report(students: list[dict]) -> None:
    if not students:
        print("No students found.")
        return

    print("\n--- Performance Report ---")
    for s in students:
        print(
            f"Student: {s['name']}, Total Marks: {s['total']}, "
            f"Average Marks: {s['average']:.2f}, Grade: {s['grade']}"
        )

    top = get_top_scorer(students)
    if top:
        print(f"\nTop Performer: {top['name']} (Average: {top['average']:.2f}, Grade: {top['grade']})")


def main() -> None:
    students: list[dict] = []
    print("Student Management System")

    while True:
        name = input("\nEnter student name (or type 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("Name cannot be empty.")
            continue

        marks = [get_valid_mark(i) for i in range(1, 4)]  # 3 subjects
        total, average = calculate_summary(marks)
        grade = assign_grades(average)

        students.append({
            "name": name,
            "marks": marks,
            "total": total,
            "average": average,
            "grade": grade,
        })

    display_report(students)


if __name__ == "__main__":
    main()