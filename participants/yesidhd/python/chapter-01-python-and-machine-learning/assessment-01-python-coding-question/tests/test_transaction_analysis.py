"""Tests for transaction_analysis.analyze_transactions."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transaction_analysis import analyze_transactions


class TestAnalyzeTransactions(unittest.TestCase):
    def test_typical_list(self):
        amounts = [120.50, 75.25, 300.00, 50.75, 200.00, 40.00]
        results = analyze_transactions(amounts)
        self.assertEqual(results["total"], 786.50)
        self.assertAlmostEqual(results["average"], 131.0833333333, places=10)
        self.assertEqual(results["max"], 300.00)
        self.assertEqual(results["above_average_count"], 2)

    def test_empty_list(self):
        results = analyze_transactions([])
        self.assertEqual(results["total"], 0.0)
        self.assertEqual(results["average"], 0.0)
        self.assertIsNone(results["max"])
        self.assertEqual(results["above_average_count"], 0)

    def test_single_transaction(self):
        results = analyze_transactions([100.0])
        self.assertEqual(results["total"], 100.0)
        self.assertEqual(results["average"], 100.0)
        self.assertEqual(results["max"], 100.0)
        # The only transaction equals the average, so nothing is above it.
        self.assertEqual(results["above_average_count"], 0)

    def test_all_equal_amounts(self):
        results = analyze_transactions([50, 50, 50])
        self.assertEqual(results["total"], 150)
        self.assertEqual(results["average"], 50)
        self.assertEqual(results["max"], 50)
        self.assertEqual(results["above_average_count"], 0)

    def test_all_equal_fractional_amounts(self):
        # Regression: float arithmetic makes sum([0.7, 0.7, 0.7]) come out
        # as 2.0999999999999996, so a float mean is below 0.7 and would
        # count every transaction as above average instead of none.
        results = analyze_transactions([0.7, 0.7, 0.7])
        self.assertEqual(results["total"], 2.1)
        self.assertEqual(results["average"], 0.7)
        self.assertEqual(results["max"], 0.7)
        self.assertEqual(results["above_average_count"], 0)

    def test_all_above_average_except_one(self):
        # Average is 82.75, so 100, 110, and 120 are all above it.
        results = analyze_transactions([1, 100, 110, 120])
        self.assertEqual(results["above_average_count"], 3)

    def test_negative_amounts(self):
        results = analyze_transactions([-20.0, 10.0, 30.0])
        self.assertEqual(results["total"], 20.0)
        self.assertAlmostEqual(results["average"], 6.6666666667, places=10)
        self.assertEqual(results["max"], 30.0)
        self.assertEqual(results["above_average_count"], 2)


if __name__ == "__main__":
    unittest.main()
