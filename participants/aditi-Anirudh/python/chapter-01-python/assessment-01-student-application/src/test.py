import unittest
from Student_marks import Student, assign_grade, calculate_average, calculate_total

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(["Subject A", "Subject B"])

    def test_calculate_total(self):
        self.assertEqual(calculate_total([80, 90, 70]), 240)
        self.assertEqual(calculate_total([]), 0)

    def test_default_subjects_are_predefined(self):
        student = Student()
        self.assertEqual(student.subjects, ["python", "java", "sql"])
        student.add_student("Alice", [80, 90, 70])

    def test_calculate_average(self):
        self.assertEqual(calculate_average([80, 90, 70]), 80)

    def test_calculate_average_for_empty_marks(self):
        self.assertEqual(calculate_average([]), 0)

    def test_calculation_helpers_reject_invalid_marks(self):
        for marks in ([-1], [101], [float("nan")], [float("inf")], ["invalid"]):
            with self.subTest(marks=marks), self.assertRaises(ValueError):
                calculate_total(marks)
            with self.subTest(marks=marks), self.assertRaises(ValueError):
                calculate_average(marks)

    def test_invalid_marks_are_rejected(self):
        for marks in ([-1, 80], [101, 80], ["not a number", 80], [True, 80]):
            with self.subTest(marks=marks), self.assertRaises(ValueError):
                self.student.add_student("Alice", marks)

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.student.add_student("  ", [80])

    def test_different_mark_counts_are_rejected(self):
        self.student.add_student("Alice", [80, 90])
        with self.assertRaises(ValueError):
            self.student.add_student("Bob", [75])

    def test_grade_assignment_uses_class_average_without_changing_marks(self):
        self.student.add_student("Alice", [90, 80])
        self.student.add_student("Bob", [70, 80])

        grades = self.student.assign_grades()

        self.assertEqual(grades, {"Alice": "P", "Bob": "F"})
        self.assertEqual(self.student.assign_grades(), grades)
        self.assertEqual(self.student.student_data["Alice"], [90, 80])
        self.assertEqual(self.student.student_data["Bob"], [70, 80])
        self.assertEqual(assign_grade(80, 80), "P")

    def test_grade_equal_to_class_average_passes(self):
        self.assertEqual(assign_grade(80, 80), "P")

    def test_grade_rejects_invalid_averages(self):
        for average in (-1, 101, float("nan"), float("inf"), True, "80"):
            with self.subTest(average=average), self.assertRaises(ValueError):
                assign_grade(average, 80)
            with self.subTest(average=average), self.assertRaises(ValueError):
                assign_grade(80, average)

    def test_subject_grades_compare_marks_to_each_subject_average(self):
        self.student.add_student("Alice", [90, 70])
        self.student.add_student("Bob", [70, 90])

        grades = self.student.assign_subject_grades()

        self.assertEqual(grades["Alice"], {"Subject A": "P", "Subject B": "F"})
        self.assertEqual(grades["Bob"], {"Subject A": "F", "Subject B": "P"})
        self.assertEqual(self.student.student_data["Alice"], [90, 70])

    def test_subject_mark_equal_to_average_passes(self):
        self.student.add_student("Alice", [80, 80])
        self.assertEqual(
            self.student.assign_subject_grades()["Alice"],
            {"Subject A": "P", "Subject B": "P"},
        )

    def test_subject_summary_calculates_totals_and_averages(self):
        self.student.add_student("Alice", [90, 70])
        self.student.add_student("Bob", [70, 90])

        self.assertEqual(self.student.get_subject_summary(), {
            "Subject A": {"total": 160, "average": 80},
            "Subject B": {"total": 160, "average": 80},
        })

    def test_subject_names_must_be_nonempty_and_unique(self):
        with self.assertRaises(ValueError):
            Student(["Subject A", " "])
        with self.assertRaises(ValueError):
            Student(["Subject A", "subject a"])
        for subjects in ([], "Subject A", [1]):
            with self.subTest(subjects=subjects), self.assertRaises(ValueError):
                Student(subjects)

    def test_duplicate_student_names_ignore_case_and_surrounding_spaces(self):
        self.student.add_student("Alice", [80, 90])
        with self.assertRaises(ValueError):
            self.student.add_student(" alice ", [70, 80])

    def test_highest_average_includes_ties(self):
        self.student.add_student("Alice", [90, 80])
        self.student.add_student("Bob", [80, 90])
        self.student.add_student("Charlie", [70, 70])

        names, average = self.student.get_highest_performers()

        self.assertEqual(names, ["Alice", "Bob"])
        self.assertEqual(average, 85)

    def test_highest_average_includes_equal_decimal_averages(self):
        self.student.add_student("Alice", [0.1, 0.2])
        self.student.add_student("Bob", [0.1, 0.2])

        names, average = self.student.get_highest_performers()

        self.assertEqual(names, ["Alice", "Bob"])
        self.assertAlmostEqual(average, 0.15)

    def test_highest_average_for_no_students(self):
        self.assertEqual(self.student.get_highest_performers(), ([], None))
        self.assertEqual(self.student.assign_grades(), {})
        self.assertEqual(self.student.assign_subject_grades(), {})

    def test_unknown_student_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Student 'Unknown' was not found"):
            self.student.calculate_student_average("Unknown")
        with self.assertRaisesRegex(ValueError, "Student 'Unknown' was not found"):
            self.student.calculate_student_total("Unknown")

    def test_student_lookup_ignores_case_and_surrounding_spaces(self):
        self.student.add_student("Alice", [80, 90])
        self.assertEqual(self.student.calculate_student_average(" alice "), 85)
        self.assertEqual(self.student.calculate_student_total("ALICE"), 170)

    def test_student_report_has_individual_calculations(self):
        self.student.add_student("Alice", [80, 100])

        report = self.student.get_performance_report()

        self.assertEqual(report["Alice"], {
            "marks": [80, 100],
            "subject_marks": {"Subject A": 80, "Subject B": 100},
            "total": 180,
            "average": 90,
            "grade": "P",
            "subject_grades": {"Subject A": "P", "Subject B": "P"},
        })
if __name__ == '__main__':
    unittest.main()