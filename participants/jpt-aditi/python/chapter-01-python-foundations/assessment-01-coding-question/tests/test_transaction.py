from fractions import Fraction

import pytest

from src.transaction import transactions_summary


def test_empty_list_returns_zero_summary():
    assert transactions_summary([]) == {
        "total": 0,
        "average": Fraction(0),
        "maximum": None,
        "above_average_count": 0,
    }


def test_basic_summary_values_are_calculated_correctly():
    assert transactions_summary([1, 2, 3, 4]) == {
        "total": 10,
        "average": Fraction(5, 2),
        "maximum": 4,
        "above_average_count": 2,
    }


def test_basic_summary_values_using_float_and_int():
    assert transactions_summary([1.4, 2, 3.5, 4]) == {
        "total": Fraction(109, 10),
        "average": Fraction(109, 40),
        "maximum": 4,
        "above_average_count": 2,
    }


def test_equal_values_have_zero_above_average_count():
    assert transactions_summary([5, 5, 5]) == {
        "total": 15,
        "average": Fraction(5),
        "maximum": 5,
        "above_average_count": 0,
    }


def test_rejects_non_numeric_values():
    with pytest.raises(TypeError, match="amounts must contain only finite numeric values"):
        transactions_summary([100, "invalid"])

def test_rejects_non_finite_values():
    with pytest.raises(TypeError, match="amounts must contain only finite numeric values"):
        transactions_summary([1.0, float("inf")])

def test_rejects_nan_values():
    with pytest.raises(TypeError, match="amounts must contain only finite numeric values"):
        transactions_summary([1.0, float("nan")])


def test_large_integer_average_is_exact_without_overflow():
    large_amount = 10**1000

    summary = transactions_summary([large_amount])

    assert summary["total"] == large_amount
    assert summary["average"] == Fraction(large_amount)
    assert summary["maximum"] == large_amount
    assert summary["above_average_count"] == 0


def test_total_of_large_integer_and_float_is_exact_without_overflow():
    large_amount = 10**1000

    summary = transactions_summary([large_amount, 1.0])

    assert summary["total"] == Fraction(large_amount + 1)
    assert summary["average"] == Fraction(large_amount + 1, 2)


def test_total_of_finite_floats_does_not_overflow_to_infinity():
    summary = transactions_summary([1e308, 1e308])

    assert summary["total"] == Fraction("2e308")
    assert summary["average"] == Fraction("1e308")

