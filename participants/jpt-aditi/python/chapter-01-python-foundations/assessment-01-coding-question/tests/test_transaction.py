import sys
from pathlib import Path

import pytest

""" 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
"""

from src.transaction import transactions_summary


def test_empty_list_returns_zero_summary():
    assert transactions_summary([]) == {
        "total": 0,
        "average": 0,
        "maximum": None,
        "above_average_count": 0,
    }


def test_basic_summary_values_are_calculated_correctly():
    assert transactions_summary([1, 2, 3, 4]) == {
        "total": 10,
        "average": 2.5,
        "maximum": 4,
        "above_average_count": 2,
    }


def test_basic_summary_values_using_float_and_int():
    assert transactions_summary([1.4, 2, 3.5, 4]) == {
        "total": 10.9,
        "average": 2.725,
        "maximum": 4,
        "above_average_count": 2,
    }


def test_equal_values_have_zero_above_average_count():
    assert transactions_summary([5, 5, 5]) == {
        "total": 15,
        "average": 5.0,
        "maximum": 5,
        "above_average_count": 0,
    }


def test_rejects_non_numeric_values():
    with pytest.raises(TypeError, match="amounts must contain only finite numeric values"):
        transactions_summary([100, "invalid"])
