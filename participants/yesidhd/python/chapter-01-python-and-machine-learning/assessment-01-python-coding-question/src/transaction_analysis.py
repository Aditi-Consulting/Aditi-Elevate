"""Transaction analysis challenge.

Provides a function that summarizes a list of transaction amounts:
total, average, maximum transaction, and the number of transactions
above the average. Empty input is handled explicitly.

"""

from decimal import Decimal
from typing import List


def analyze_transactions(amounts: List[float]) -> dict:
    if not amounts:
        return {
            "total": 0.0,
            "average": 0.0,
            "max": None,
            "above_average_count": 0,
        }

    exact_amounts = [Decimal(str(amount)) for amount in amounts]
    exact_total = sum(exact_amounts, Decimal("0"))
    exact_average = exact_total / len(amounts)

    return {
        "total": float(exact_total),
        "average": float(exact_average),
        "max": max(amounts),
        "above_average_count": sum(
            1 for amount in exact_amounts if amount > exact_average
        ),
    }


def main() -> None:
    """Run the function against sample data and print the results."""
    transactions = [120.50, 75.25, 300.00, 50.75, 200.00, 40.00]
    results = analyze_transactions(transactions)

    print(f"Transactions: {transactions}")
    print(f"Total amount:              {results['total']:.2f}")
    print(f"Average amount:            {results['average']:.2f}")
    print(f"Maximum transaction:       {results['max']:.2f}")
    print(f"Transactions above average: {results['above_average_count']}")

    empty_results = analyze_transactions([])
    print(f"\nEmpty list results: {empty_results}")


if __name__ == "__main__":
    main()
