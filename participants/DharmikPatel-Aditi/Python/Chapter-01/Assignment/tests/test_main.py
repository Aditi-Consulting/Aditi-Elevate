import unittest
from src.main import (
    assign_grades,
    calculate_summary,
    get_top_scorer,
    validate_marks,
)


class TestStudentAnalyzer(unittest.TestCase):
    def test_calculate_summary(self):
        total, avg = calculate_summary([80, 90, 100])
        self.assertEqual(total, 270)
        self.assertEqual(avg, 90.0)

    def test_assign_grades(self):
        self.assertEqual(assign_grades(95), "A")
        self.assertEqual(assign_grades(82), "B")
        self.assertEqual(assign_grades(75), "C")
        self.assertEqual(assign_grades(65), "D")
        self.assertEqual(assign_grades(40), "F")

    def test_get_top_scorer(self):
        students = [
            {"name": "Alice", "average": 78.0},
            {"name": "Bob", "average": 92.5},
            {"name": "Charlie", "average": 85.0},
        ]
        top = get_top_scorer(students)
        self.assertIsNotNone(top)
        self.assertEqual(top["name"], "Bob")

    def test_validate_marks_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_marks("-5")
        with self.assertRaises(ValueError):
            validate_marks("105")

    def test_validate_marks_invalid_text(self):
        with self.assertRaises(ValueError):
            validate_marks("abc")


if __name__ == "__main__":
    unittest.main()