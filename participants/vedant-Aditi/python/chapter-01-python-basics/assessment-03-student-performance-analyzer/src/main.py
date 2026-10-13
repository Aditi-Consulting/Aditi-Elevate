NUMBER_OF_SUBJECTS = 3


def calculate_total(marks):
    """Return the sum of the supplied marks."""
    return sum(marks)


def calculate_average(marks):
    """Return the arithmetic mean, or 0 for an empty marks list."""
    if not marks:
        return 0

    return calculate_total(marks) / len(marks)


def assign_grade(average):
    """Return a grade for the supplied average."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"

    return "F"


def validate_mark(mark):
    """Convert a mark to a number and validate that it is between 0 and 100."""
    try:
        numeric_mark = float(mark)
    except ValueError as error:
        raise ValueError("Mark must be a number.") from error

    if numeric_mark < 0 or numeric_mark > 100:
        raise ValueError("Mark must be between 0 and 100.")

    return numeric_mark


def find_top_student(students):
    """Return the student with the highest average, or None for empty input.

    If students tie for the highest average, the first student in the list wins.
    """
    if not students:
        return None

    top_student = students[0]
    top_average = calculate_average(top_student["marks"])

    for student in students[1:]:
        student_average = calculate_average(student["marks"])
        if student_average > top_average:
            top_student = student
            top_average = student_average

    return top_student


def generate_report(students):
    """Return a readable performance report for the supplied students."""
    if not students:
        return "No student records available."

    report_lines = ["Student Performance Report"]

    for student in students:
        total = calculate_total(student["marks"])
        average = calculate_average(student["marks"])
        grade = assign_grade(average)
        report_lines.append(
            f"{student['name']}: Total = {total:.2f}, "
            f"Average = {average:.2f}, Grade = {grade}"
        )

    top_student = find_top_student(students)
    top_average = calculate_average(top_student["marks"])
    top_grade = assign_grade(top_average)
    report_lines.append(
        f"Top Student: {top_student['name']} "
        f"(Average = {top_average:.2f}, Grade = {top_grade})"
    )

    return "\n".join(report_lines)


def get_positive_integer(prompt):
    """Prompt until the user enters a positive integer."""
    while True:
        user_input = input(prompt)

        try:
            value = int(user_input)
        except ValueError:
            print("Please enter a positive integer.")
            continue

        if value <= 0:
            print("Please enter a positive integer.")
            continue

        return value


def get_mark(prompt):
    """Prompt until the user enters a valid mark."""
    while True:
        user_input = input(prompt)

        try:
            return validate_mark(user_input)
        except ValueError as error:
            print(error)


def main():
    students = []
    student_count = get_positive_integer("Enter the number of students: ")

    for student_number in range(1, student_count + 1):
        name = input(f"Enter name for student {student_number}: ").strip()

        while not name:
            print("Student name cannot be empty.")
            name = input(f"Enter name for student {student_number}: ").strip()

        marks = []
        for subject_number in range(1, NUMBER_OF_SUBJECTS + 1):
            mark = get_mark(f"Enter mark {subject_number} for {name}: ")
            marks.append(mark)

        students.append({"name": name, "marks": marks})

    print(generate_report(students))


if __name__ == "__main__":
    main()
