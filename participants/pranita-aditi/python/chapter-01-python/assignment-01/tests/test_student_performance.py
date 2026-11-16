
# Importing unittest module for testing
import unittest
import sys
import os

# Adding src folder path to access main Python file
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

# Importing functions from main program
from student_performance_analyzer import (
    calculate_total,
    calculate_average,
    assign_grade,
    display_report
)


# Creating a test class
class TestStudentPerformance(unittest.TestCase):

    # TEST 1: Check total marks calculation
    def test_total(self):
        self.assertEqual(
            calculate_total([80, 90, 70]), 240
        )

    # TEST 2: Check average marks calculation
    def test_average(self):
        self.assertEqual(
            calculate_average([80, 90, 70]), 80
        )

    # TEST 3: Check A grade assignment
    def test_grade(self):
        self.assertEqual(assign_grade(95), "A")

    # TEST 4: Check failing grade
    def test_low_grade(self):
        self.assertEqual(assign_grade(40), "F")

    # TEST 5: Check B grade assignment
    def test_grade_b(self):
        self.assertEqual(assign_grade(75), "C")

    # TEST 6: Check topper name
    def test_topper(self):
        from io import StringIO
        from unittest.mock import patch

        students = {
            "Riya Shah": [80, 90],
            "Diya Patel": [70, 60],
            "Hiya Pathak": [89, 65]
        }

        with patch("sys.stdout", new=StringIO()) as output:
            display_report(students)

        self.assertIn(
            "Top Performing Student: Riya Shah",
            output.getvalue()
        )


# Run all test cases
if __name__ == "__main__":
    unittest.main()
