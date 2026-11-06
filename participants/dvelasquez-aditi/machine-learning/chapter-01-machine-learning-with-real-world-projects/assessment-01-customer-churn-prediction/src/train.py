"""Train and compare churn classifiers.

Usage: python src/train.py [path/to/customers.csv]
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from churn_utils import (build_preprocessor, check_data_quality, clean_data, compute_metrics,
                         load_data, split_features_target, top_features)

ROOT = Path(__file__).resolve().parents[1]
RANDOM_STATE = 42


def main(csv_path: Path) -> None:
    df = load_data(csv_path)

    print("=== Data quality report ===")
    for key, value in check_data_quality(df).items():
        print(f"{key}: {value}")

    df = clean_data(df)
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE)
    print(f"\nTrain rows: {len(X_train)}, test rows: {len(X_test)}")

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                                class_weight="balanced", random_state=RANDOM_STATE),
    }
    fitted, rows = {}, {}
    for name, clf in models.items():
        pipe = Pipeline([("prep", build_preprocessor(X_train)), ("model", clf)]).fit(X_train, y_train)
        fitted[name] = pipe
        rows[name] = compute_metrics(y_test, pipe.predict(X_test), pipe.predict_proba(X_test)[:, 1])

    results = pd.DataFrame(rows).T.round(3)
    print("\n=== Model comparison (test set) ===")
    print(results.to_string())

    # ROC-AUC is threshold-independent and robust to class imbalance; F1 breaks ties.
    best = results.sort_values(["roc_auc", "f1"], ascending=False).index[0]
    pipe = fitted[best]
    names = pipe.named_steps["prep"].get_feature_names_out()
    print(f"\n=== Selected model: {best} (highest ROC-AUC) ===")
    print("Most influential features:")
    for feat, val in top_features(pipe.named_steps["model"], names):
        print(f"  {feat:40s} {val:+.3f}")

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    results.to_csv(out / "model_comparison.csv")
    print(f"\nSaved metrics to {out / 'model_comparison.csv'}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "customers.csv")
