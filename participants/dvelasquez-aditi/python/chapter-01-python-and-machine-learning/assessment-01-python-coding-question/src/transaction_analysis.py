"""Transaction analysis: total, average, max and count above average."""
from decimal import Decimal
from typing import Dict, List, Optional, Union

Number = Union[int, float]


def analyze_transactions(amounts: List[Number]) -> Dict[str, Optional[Number]]:
    """Return total, average, max and the count of amounts strictly above average.

    An empty list returns zeros and ``None`` for the maximum.
    Decimal arithmetic avoids float rounding errors when comparing to the mean.
    """
    if not amounts:
        return {"total": 0.0, "average": 0.0, "max": None, "above_average_count": 0}

    exact = [Decimal(str(a)) for a in amounts]
    total = sum(exact)
    average = total / len(exact)
    return {
        "total": float(total),
        "average": float(average),
        "max": max(amounts),
        "above_average_count": sum(1 for a in exact if a > average),
    }


def main() -> None:
    sample = [120.5, 75.25, 300.0, 50.75, 200.0, 40.0]
    print(sample, analyze_transactions(sample))
    print([], analyze_transactions([]))


if __name__ == "__main__":
    main()
