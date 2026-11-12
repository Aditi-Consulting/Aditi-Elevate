import unittest
from unittest.mock import patch

import assignment1


class TestStudentPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        assignment1.leaderboard.clear()

    def test_handle_input_accepts_mark_between_zero_and_hundred(self):
        with patch("builtins.input", return_value="75"):
            result = assignment1.handle_input(0, "Physics")
        self.assertEqual(result, 75)

    def test_handle_input_rejects_invalid_mark_before_accepting_valid_mark(self):
        with patch("builtins.input", side_effect=["-1", "101", "85"]):
            result = assignment1.handle_input(0, "Physics")
        self.assertEqual(result, 85)

    def test_grader_assigns_expected_grade(self):
        self.assertEqual(assignment1.grader(100), "A")
        self.assertEqual(assignment1.grader(80), "B")
        self.assertEqual(assignment1.grader(60), "C")
        self.assertEqual(assignment1.grader(40), "D")
        self.assertEqual(assignment1.grader(39), "F")

    def test_add_student_data_calculates_total_and_average(self):
        inputs = ["Alice", "80", "90", "70", "60", "100"]
        with patch("builtins.input", side_effect=inputs):
            assignment1.add_student_data()
        self.assertEqual(assignment1.total, 400)
        self.assertEqual(assignment1.average, 80)

    def test_add_student_data_stores_student_in_leaderboard(self):
        inputs = ["Bob", "90", "90", "90", "90", "90"]
        with patch("builtins.input", side_effect=inputs):
            assignment1.add_student_data()
        self.assertEqual(assignment1.leaderboard["Bob"], 450)


if __name__ == "__main__":
    unittest.main()
