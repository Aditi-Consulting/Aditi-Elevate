from typing import TypedDict


class TransactionSummary(TypedDict):
    """Structured output returned by transactions_summary."""
    total: float | int
    average: float
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
            "total": 0,
            "average": 0,
            "maximum": None,
            "above_average_count": 0,
        }

    try:
        total = sum(amounts)
        average = total / len(amounts)
        maximum = max(amounts)
        above_average_count = sum(1 for a in amounts if a > average)
    except (TypeError, ValueError) as e:
        raise TypeError("amounts must contain only finite numeric values") from e

    return {
        "total": total,
        "average": average,
        "maximum": maximum,
        "above_average_count": above_average_count,
    }