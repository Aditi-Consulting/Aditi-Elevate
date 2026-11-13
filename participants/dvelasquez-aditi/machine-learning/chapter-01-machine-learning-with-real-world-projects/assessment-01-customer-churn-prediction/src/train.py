"""Train and compare churn classifiers.

Usage:
    python src/train.py [path/to/customers.csv] [--target-recall 0.85]

With --target-recall, each model's decision threshold is also tuned to reach that
recall. The threshold is chosen on out-of-fold training predictions (never on the
test set) and then evaluated once on the test set.
"""
import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline

from churn_utils import (build_preprocessor, check_data_quality, clean_data, compute_metrics,
                         confusion_counts, load_data, split_features_target,
                         threshold_for_recall, top_features)

ROOT = Path(__file__).resolve().parents[1]
RANDOM_STATE = 42


def print_confusions(title, confusions) -> None:
    print(f"\n=== {title} ===")
    print(pd.DataFrame(confusions).T[["tp", "fn", "fp", "tn"]].to_string())
    print("(tp = churners caught, fn = churners missed, fp = false alarms, tn = loyal kept)")


def main(csv_path: Path, target_recall: float = None) -> None:
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
    fitted, rows, confusions = {}, {}, {}
    tuned_rows, tuned_confusions = {}, {}
    for name, clf in models.items():
        pipe = Pipeline([("prep", build_preprocessor(X_train)), ("model", clf)])
        if target_recall is not None:
            # Out-of-fold probabilities: the threshold is picked without touching the test set.
            oof = cross_val_predict(pipe, X_train, y_train, cv=5, method="predict_proba")[:, 1]
            threshold = threshold_for_recall(y_train, oof, target_recall)
        pipe.fit(X_train, y_train)
        fitted[name] = pipe
        proba = pipe.predict_proba(X_test)[:, 1]
        pred = pipe.predict(X_test)
        rows[name] = compute_metrics(y_test, pred, proba)
        confusions[name] = confusion_counts(y_test, pred)
        if target_recall is not None:
            tuned_pred = (proba >= threshold).astype(int)
            tuned_rows[name] = {"threshold": threshold, **compute_metrics(y_test, tuned_pred, proba)}
            tuned_confusions[name] = confusion_counts(y_test, tuned_pred)

    results = pd.DataFrame(rows).T.round(3)
    print("\n=== Model comparison (test set, default 0.5 threshold) ===")
    print(results.to_string())
    print_confusions("Confusion counts (test set, default 0.5 threshold)", confusions)

    if target_recall is not None:
        tuned = pd.DataFrame(tuned_rows).T.round(3)
        print(f"\n=== Threshold tuned for recall >= {target_recall} (chosen on training data) ===")
        print(tuned.to_string())
        print_confusions("Confusion counts (test set, tuned threshold)", tuned_confusions)

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
    if target_recall is not None:
        tuned.to_csv(out / "model_comparison_tuned.csv")
        print(f"Saved tuned metrics to {out / 'model_comparison_tuned.csv'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("csv", nargs="?", type=Path, default=ROOT / "data" / "customers.csv")
    parser.add_argument("--target-recall", type=float, default=None,
                        help="tune each model's decision threshold to reach this recall (0-1]")
    args = parser.parse_args()
    main(args.csv, args.target_recall)
