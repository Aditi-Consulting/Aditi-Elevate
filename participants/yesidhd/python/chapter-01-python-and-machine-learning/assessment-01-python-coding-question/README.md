# Assessment 01 — Python Coding Question: Transaction Analysis

## Participant

- Name: Yesid Herrera
- GitHub username: `yesidhd`

## Assessment

- Learning area: Python (Pillar 2, Chapter 01 — Python and Machine Learning)
- Chapter: 01 — Python and Machine Learning
- Assessment: 01 — Python coding question

## Objective

Write a function that accepts a list of transaction amounts and returns:

1. Total amount.
2. Average amount.
3. Maximum transaction.
4. Number of transactions above the average.

The function must handle an empty list.

## Approach

- `src/transaction_analysis.py` defines `analyze_transactions(amounts)`, which
  returns a dictionary with the keys `total`, `average`, `max`, and
  `above_average_count`.
- The empty-list case is handled first: it returns `0.0` for `total` and
  `average`, `None` for `max` (there is no transaction), and `0` for
  `above_average_count`.
- "Above the average" is interpreted as strictly greater than the average, so
  transactions equal to the average are not counted. To avoid float rounding
  miscounting amounts equal to the mean (e.g. `[0.7, 0.7, 0.7]`), the total,
  average, and comparisons use exact decimal arithmetic; the reported
  `total` and `average` are floats converted from those exact results.
- The module also includes a `main()` demo that runs the function on sample
  data and prints the results, including the empty-list case.
- Tests in `tests/test_transaction_analysis.py` cover the typical case, the
  empty list, a single transaction, all-equal amounts (integers and
  fractions), and negative amounts,
  using only the standard-library `unittest` framework.

## Setup

- Python 3.9 or newer (developed and validated with Python 3.9.6).
- No third-party dependencies; see `requirements.txt`.

## How to run

From this assessment folder:

```bash
# Run the demo
python3 src/transaction_analysis.py

# Run the tests
python3 -m unittest discover -s tests -v
```

## Validation and results

Executed `python3 -m unittest discover -s tests -v` — all 7 tests pass.
Executed `python3 src/transaction_analysis.py` — sample output:

```text
Transactions: [120.5, 75.25, 300.0, 50.75, 200.0, 40.0]
Total amount:              786.50
Average amount:            131.08
Maximum transaction:       300.00
Transactions above average: 2

Empty list results: {'total': 0.0, 'average': 0.0, 'max': None, 'above_average_count': 0}
```

## References and limitations

- Python standard library documentation: `builtins.sum`, `builtins.max`, and
  the `unittest` framework.
- Assumption: amounts are numeric (`int` or `float`) and the list contains no
  non-numeric values; input validation beyond the empty-list case is out of
  scope for this assessment.
- Known limitations: none.
