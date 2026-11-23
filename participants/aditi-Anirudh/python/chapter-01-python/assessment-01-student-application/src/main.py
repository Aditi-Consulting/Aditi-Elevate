from Student_marks import Student


def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value <= 0:
            print("Please enter a number greater than zero.")
            continue
        return value


def read_student_name(existing_names):
    while True:
        name = input("Enter student name: ").strip()
        if not name:
            print("Student name cannot be empty.")
        elif name.casefold() in existing_names:
            print("That student name has already been entered.")
        else:
            return name


def read_marks(subjects):
    marks = []
    while len(marks) < len(subjects):
        subject = subjects[len(marks)]
        try:
            mark = float(input(f"Enter mark for {subject}: "))
        except ValueError:
            print("Please enter a numeric mark.")
            continue
        if not 0 <= mark <= 100:
            print("Marks must be between 0 and 100.")
            continue
        marks.append(int(mark) if mark.is_integer() else mark)
    return marks


def main():
    student_count = read_positive_integer("How many students? ")
    analyzer = Student()
    subjects = analyzer.subjects

    for _ in range(student_count):
        name = read_student_name(analyzer.student_names)
        marks = read_marks(subjects)
        analyzer.add_student(name, marks)

    print("\nStudent Performance Report")
    for name, result in analyzer.get_performance_report().items():
        print(
            f"{name}: marks={result['marks']}, total={result['total']}, "
            f"average={result['average']:.2f}, grade={result['grade']}"
        )
        for subject in subjects:
            print(
                f"  {subject}: mark={result['subject_marks'][subject]}, "
                f"grade={result['subject_grades'][subject]}"
            )

    print("\nSubject Summary")
    for subject, result in analyzer.get_subject_summary().items():
        print(f"{subject}: total={result['total']}, average={result['average']:.2f}")

    names, average = analyzer.get_highest_performers()
    print(f"Highest average: {', '.join(names)} ({average:.2f})")


if __name__ == "__main__":
    main()
