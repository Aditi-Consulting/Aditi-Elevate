import unittest
from unittest.mock import patch

from src.student_performance_analyzer import (
    assign_grade,
    calculate_average,
    calculate_total,
    create_student_record,
    find_top_student,
    get_valid_mark,
)


class StudentMarksTests(unittest.TestCase):
    def test_calculate_total(self):
        self.assertEqual(calculate_total({"English": 80, "Maths": 90}), 170)

    def test_calculate_average(self):
        self.assertEqual(calculate_average({"English": 80, "Maths": 90}), 85)

    def test_calculate_average_rejects_empty_marks(self):
        with self.assertRaises(ValueError):
            calculate_average({})

    def test_assign_grade_thresholds(self):
        cases = ((100, "A"), (80, "B"), (60, "C"), (40, "D"), (39, "F"))
        for average, expected_grade in cases:
            with self.subTest(average=average):
                self.assertEqual(assign_grade(average), expected_grade)

    def test_get_valid_mark_accepts_zero_and_one_hundred(self):
        for mark in ("0", "100"):
            with self.subTest(mark=mark), patch("builtins.input", return_value=mark):
                self.assertEqual(get_valid_mark("English"), int(mark))

    def test_get_valid_mark_retries_invalid_values(self):
        with patch("builtins.input", side_effect=("abc", "101", "-1", "75")):
            with patch("builtins.print"):
                self.assertEqual(get_valid_mark("Maths"), 75)

    def test_create_student_record(self):
        record = create_student_record(
            {"English": 100, "Maths": 80, "Environment": 60, "Gujarati": 40}
        )
        self.assertEqual(record["total"], 280)
        self.assertEqual(record["average"], 70)
        self.assertEqual(record["grade"], "C")

    def test_find_top_student(self):
        students = {
            "Asha": create_student_record({"English": 80, "Maths": 80}),
            "Ravi": create_student_record({"English": 95, "Maths": 90}),
        }
        self.assertEqual(find_top_student(students), ("Ravi", students["Ravi"]))

    def test_find_top_student_returns_none_when_empty(self):
        self.assertIsNone(find_top_student({}))


if __name__ == "__main__":
    unittest.main()
