from math import isfinite
from numbers import Real

DEFAULT_SUBJECTS = ("python", "java", "sql")


def _validate_marks(marks):
    if not isinstance(marks, (list, tuple)):
        raise ValueError("Marks must be provided as a list or tuple")
    if any(
        isinstance(mark, bool)
        or not isinstance(mark, Real)
        or not isfinite(mark)
        or mark < 0
        or mark > 100
        for mark in marks
    ):
        raise ValueError("Marks must be finite numbers between 0 and 100")
    return marks


def calculate_total(marks):
    _validate_marks(marks)
    return sum(marks)


def calculate_average(marks):
    _validate_marks(marks)
    if not marks:
        return 0
    return calculate_total(marks) / len(marks)


def assign_grade(student_average, class_average):
    _validate_marks([student_average, class_average])
    return "P" if student_average >= class_average else "F"


class Student:
    def __init__(self, subjects=None):
        self.student_data = {}
        self.student_names = set()
        self.student_name_lookup = {}
        self.marks_per_student = None
        subjects = DEFAULT_SUBJECTS if subjects is None else subjects
        self.subjects = self._validate_subjects(subjects)

    @staticmethod
    def _validate_subjects(subjects):
        if not isinstance(subjects, (list, tuple)) or not subjects:
            raise ValueError("Enter at least one subject name")
        names = [subject.strip() if isinstance(subject, str) else "" for subject in subjects]
        if any(not name for name in names):
            raise ValueError("Subject names cannot be empty")
        if len({name.casefold() for name in names}) != len(names):
            raise ValueError("Subject names must be unique")
        return names

    def add_student(self, name, marks):
        name = name.strip() if isinstance(name, str) else ""
        if not name:
            raise ValueError("Student name cannot be empty")
        name_key = name.casefold()
        if name_key in self.student_names:
            raise ValueError("Student name has already been entered")
        if not isinstance(marks, (list, tuple)) or not marks:
            raise ValueError("Enter at least one mark")
        _validate_marks(marks)
        if len(marks) != len(self.subjects):
            raise ValueError("Enter one mark for each subject")
        if self.marks_per_student is not None and len(marks) != self.marks_per_student:
            raise ValueError("Every student must have the same number of marks")

        self.marks_per_student = len(marks)
        self.student_data[name] = list(marks)
        self.student_names.add(name_key)
        self.student_name_lookup[name_key] = name

    def _get_student_name(self, name):
        name_key = name.strip().casefold() if isinstance(name, str) else ""
        stored_name = self.student_name_lookup.get(name_key)
        if stored_name is None:
            raise ValueError(f"Student {name!r} was not found")
        return stored_name

    def calculate_student_total(self, name):
        stored_name = self._get_student_name(name)
        return calculate_total(self.student_data[stored_name])

    def calculate_student_average(self, name):
        stored_name = self._get_student_name(name)
        return calculate_average(self.student_data[stored_name])

    def calculate_total_and_average(self):
        all_marks = [mark for marks in self.student_data.values() for mark in marks]
        return calculate_total(all_marks), calculate_average(all_marks)

    def assign_grades(self):
        if not self.student_data:
            return {}
        _, class_average = self.calculate_total_and_average()
        return {
            name: assign_grade(self.calculate_student_average(name), class_average)
            for name in self.student_data
        }

    def get_subject_averages(self):
        if not self.student_data:
            return {subject: 0 for subject in self.subjects or []}
        return {
            subject: calculate_average([marks[index] for marks in self.student_data.values()])
            for index, subject in enumerate(self.subjects)
        }

    def get_subject_summary(self):
        summary = {}
        for index, subject in enumerate(self.subjects):
            subject_marks = [marks[index] for marks in self.student_data.values()]
            summary[subject] = {
                "total": calculate_total(subject_marks),
                "average": calculate_average(subject_marks),
            }
        return summary

    def assign_subject_grades(self):
        subject_averages = self.get_subject_averages()
        return {
            name: {
                subject: assign_grade(marks[index], subject_averages[subject])
                for index, subject in enumerate(self.subjects)
            }
            for name, marks in self.student_data.items()
        }

    def get_highest_performers(self):
        if not self.student_data:
            return [], None

        averages = {
            name: self.calculate_student_average(name)
            for name in self.student_data
        }
        highest_average = max(averages.values())
        names = [
            name
            for name, average in averages.items()
            if average == highest_average
        ]
        return names, highest_average

    def get_performance_report(self):
        grades = self.assign_grades()
        subject_grades = self.assign_subject_grades()
        return {
            name: {
                "marks": list(marks),
                "subject_marks": dict(zip(self.subjects, marks)),
                "total": self.calculate_student_total(name),
                "average": self.calculate_student_average(name),
                "grade": grades[name],
                "subject_grades": subject_grades[name],
            }
            for name, marks in self.student_data.items()
        }

