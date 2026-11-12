# Assessment 01 — Python Coding Question: Transaction Analysis

- GitHub username: `dvelasquez-aditi`
- Area / chapter: Python — Chapter 01, Python and Machine Learning

## Objective
`analyze_transactions(amounts)` returns the total, average, maximum, and the
number of transactions strictly above the average. It handles an empty list.

## Approach
- Empty list returns `0.0` totals, `None` max and `0` count.
- Decimal arithmetic is used for the comparison so equal amounts such as
  `[0.7, 0.7, 0.7]` are never counted as above average due to float error.

## How to run
```bash
python src/transaction_analysis.py
python -m unittest discover -s tests -v
```

## Assumptions
Inputs are numeric; other validation is out of scope. Python 3.9+, stdlib only.
