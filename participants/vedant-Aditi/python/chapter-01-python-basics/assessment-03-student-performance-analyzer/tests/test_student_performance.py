import os
import sys
import unittest


CURRENT_DIR = os.path.dirname(__file__)
ASSESSMENT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(ASSESSMENT_DIR, "src")
sys.path.insert(0, SRC_DIR)

from main import (
    assign_grade,
    calculate_average,
    calculate_total,
    find_top_student,
    generate_report,
    validate_mark,
)


class TestStudentPerformanceAnalyzer(unittest.TestCase):
    def test_calculate_total(self):
        self.assertEqual(calculate_total([80, 90, 100]), 270)

    def test_calculate_average_with_decimal_result(self):
        self.assertEqual(calculate_average([89, 90]), 89.5)

    def test_assign_grade_boundaries(self):
        self.assertEqual(assign_grade(100), "A")
        self.assertEqual(assign_grade(90), "A")
        self.assertEqual(assign_grade(89.5), "B")
        self.assertEqual(assign_grade(80), "B")
        self.assertEqual(assign_grade(79.9), "C")
        self.assertEqual(assign_grade(70), "C")
        self.assertEqual(assign_grade(69.9), "D")
        self.assertEqual(assign_grade(60), "D")
        self.assertEqual(assign_grade(59.9), "F")

    def test_validate_mark_accepts_valid_numeric_values(self):
        self.assertEqual(validate_mark("95"), 95)
        self.assertEqual(validate_mark("82.5"), 82.5)

    def test_validate_mark_rejects_invalid_values(self):
        invalid_marks = ["-1", "101", "abc"]

        for mark in invalid_marks:
            with self.subTest(mark=mark):
                with self.assertRaises(ValueError):
                    validate_mark(mark)

    def test_find_top_student(self):
        students = [
            {"name": "Anya", "marks": [80, 85, 90]},
            {"name": "Ravi", "marks": [95, 90, 100]},
            {"name": "Maya", "marks": [70, 75, 80]},
        ]

        self.assertEqual(find_top_student(students)["name"], "Ravi")

    def test_find_top_student_uses_first_student_for_ties(self):
        students = [
            {"name": "Anya", "marks": [90, 90, 90]},
            {"name": "Ravi", "marks": [90, 90, 90]},
        ]

        self.assertEqual(find_top_student(students)["name"], "Anya")

    def test_empty_inputs(self):
        self.assertEqual(calculate_average([]), 0)
        self.assertIsNone(find_top_student([]))
        self.assertEqual(generate_report([]), "No student records available.")

    def test_generate_report_contents(self):
        students = [
            {"name": "Anya", "marks": [90, 95, 100]},
            {"name": "Ravi", "marks": [70, 75, 80]},
        ]

        report = generate_report(students)

        self.assertIn("Student Performance Report", report)
        self.assertIn("Anya: Total = 285.00, Average = 95.00, Grade = A", report)
        self.assertIn("Ravi: Total = 225.00, Average = 75.00, Grade = C", report)
        self.assertIn("Top Student: Anya (Average = 95.00, Grade = A)", report)


if __name__ == "__main__":
    unittest.main()
