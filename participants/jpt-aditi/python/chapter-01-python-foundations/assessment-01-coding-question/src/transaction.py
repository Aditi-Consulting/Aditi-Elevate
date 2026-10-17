import math
from fractions import Fraction
from typing import TypedDict


class TransactionSummary(TypedDict):
    """Structured output returned by transactions_summary."""
    total: Fraction
    average: Fraction
    maximum: float | int | None
    above_average_count: int


def transactions_summary(amounts: list[int | float]) -> TransactionSummary:
    """Return a numeric summary for a sequence of transaction amounts.

    Args:
        amounts: A list of numeric values such as floats or integers.

    Returns:
        TransactionSummary: A summary with the total, average, maximum value,
        and the number of values above the average.

    Raises:
        TypeError: If the input contains values that cannot be used in numeric
            aggregation, such as strings or None.
    """
    if not amounts:
        return {
            "total": Fraction(0),
            "average": Fraction(0),
            "maximum": None,
            "above_average_count": 0,
        }

    try:
        if any(isinstance(amount, float) and not math.isfinite(amount) for amount in amounts):
            raise ValueError("Amounts must contain only finite numeric values")
        exact_amounts = [
            Fraction(amount) if isinstance(amount, int) else Fraction(str(amount))
            for amount in amounts
        ]
        total = sum(exact_amounts, Fraction(0))
        average = total / len(exact_amounts)
        maximum = max(amounts)
        above_average_count = sum(1 for amount in exact_amounts if amount > average)
    except (TypeError, ValueError) as e:
        raise TypeError("amounts must contain only finite numeric values") from e

    return {
        "total": total,
        "average": average,
        "maximum": maximum,
        "above_average_count": above_average_count,
    }