import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from transaction_analysis import analyze_transactions  # noqa: E402


class TestAnalyzeTransactions(unittest.TestCase):
    def test_typical(self):
        r = analyze_transactions([100, 200, 300, 400])
        self.assertEqual(r["total"], 1000.0)
        self.assertEqual(r["average"], 250.0)
        self.assertEqual(r["max"], 400)
        self.assertEqual(r["above_average_count"], 2)

    def test_empty(self):
        self.assertEqual(
            analyze_transactions([]),
            {"total": 0.0, "average": 0.0, "max": None, "above_average_count": 0},
        )

    def test_single(self):
        self.assertEqual(analyze_transactions([50])["above_average_count"], 0)

    def test_all_equal_floats(self):
        self.assertEqual(analyze_transactions([0.7, 0.7, 0.7])["above_average_count"], 0)

    def test_negative(self):
        r = analyze_transactions([-10, -20, 30])
        self.assertEqual(r["max"], 30)
        self.assertEqual(r["above_average_count"], 1)


if __name__ == "__main__":
    unittest.main()
