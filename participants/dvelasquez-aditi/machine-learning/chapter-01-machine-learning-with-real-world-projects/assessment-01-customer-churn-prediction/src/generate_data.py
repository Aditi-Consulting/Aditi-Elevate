"""Generate a synthetic customer churn dataset (with realistic data-quality issues).

Usage: python src/generate_data.py [output_csv] [n_rows]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def generate(n_rows: int = 2000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 73, n_rows)
    contract = rng.choice(["month-to-month", "one-year", "two-year"], n_rows, p=[0.55, 0.25, 0.20])
    internet = rng.choice(["dsl", "fiber", "none"], n_rows, p=[0.35, 0.45, 0.20])
    payment = rng.choice(["card", "bank-transfer", "electronic-check", "mail"], n_rows)
    support_calls = rng.poisson(1.5, n_rows)
    base = np.where(internet == "fiber", 70, np.where(internet == "dsl", 50, 25))
    monthly = np.round(base + rng.normal(0, 8, n_rows), 2).clip(10)
    total = np.round(monthly * tenure + rng.normal(0, 20, n_rows), 2).clip(0)

    logit = (
        -0.8
        + 1.2 * (contract == "month-to-month")
        - 0.9 * (contract == "two-year")
        - 0.04 * tenure
        + 0.015 * (monthly - 55)
        + 0.35 * support_calls
        + 0.5 * (payment == "electronic-check")
    )
    churn = (rng.random(n_rows) < 1 / (1 + np.exp(-logit))).astype(int)

    df = pd.DataFrame({
        "customer_id": [f"C{i:05d}" for i in range(n_rows)],
        "tenure_months": tenure.astype(float),
        "monthly_charges": monthly,
        "total_charges": total,
        "support_calls": support_calls.astype(float),
        "contract_type": contract,
        "internet_service": internet,
        "payment_method": payment,
        "churn": churn,
    })
    # Inject missing values and a few duplicate rows.
    for col, frac in [("total_charges", 0.04), ("tenure_months", 0.02),
                      ("contract_type", 0.03), ("support_calls", 0.02)]:
        df.loc[rng.random(n_rows) < frac, col] = np.nan
    return pd.concat([df, df.sample(15, random_state=seed)], ignore_index=True)


if __name__ == "__main__":
    default = Path(__file__).resolve().parents[1] / "data" / "customers.csv"
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    rows = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    out.parent.mkdir(parents=True, exist_ok=True)
    generate(rows).to_csv(out, index=False)
    print(f"Wrote {out}")
