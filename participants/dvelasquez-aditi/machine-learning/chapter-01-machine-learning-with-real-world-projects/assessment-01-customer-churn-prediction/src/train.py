"""Train, compare and evaluate churn classifiers without leaking the test set.

Usage:
    python src/train.py [path/to/customers.csv] [--target-recall 0.85]

Sequence:
    1. Split the data once into train and test.
    2. Compare both models with 5-fold cross-validation on the TRAINING data only and
       pick the best one. This choice is then frozen.
    3. Fit only the selected model on the training data.
    4. Evaluate that single model once on the test set.

With --target-recall, the selected model's decision threshold is also tuned to reach
that recall, using the same training-only out-of-fold predictions.
"""
import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline

from churn_utils import (build_preprocessor, check_data_quality, clean_data, compute_metrics,
                         confusion_counts, load_data, select_best_model,
                         split_features_target, threshold_for_recall, top_features)

ROOT = Path(__file__).resolve().parents[1]
RANDOM_STATE = 42
CV_FOLDS = 5


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
    print(f"\nTrain rows: {len(X_train)}, test rows: {len(X_test)} (test set is not used until the final step)")

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                                class_weight="balanced", random_state=RANDOM_STATE),
    }
    pipelines = {name: Pipeline([("prep", build_preprocessor(X_train)), ("model", clf)])
                 for name, clf in models.items()}

    # Step 1: compare models using out-of-fold predictions on the training data only.
    oof_proba, cv_metrics, cv_confusions = {}, {}, {}
    for name, pipe in pipelines.items():
        proba = cross_val_predict(pipe, X_train, y_train, cv=CV_FOLDS, method="predict_proba")[:, 1]
        pred = (proba >= 0.5).astype(int)
        oof_proba[name] = proba
        cv_metrics[name] = compute_metrics(y_train, pred, proba)
        cv_confusions[name] = confusion_counts(y_train, pred)

    cv_table = pd.DataFrame(cv_metrics).T.round(3)
    print(f"\n=== Model comparison ({CV_FOLDS}-fold cross-validation, training data only) ===")
    print(cv_table.to_string())
    print_confusions("Confusion counts (cross-validated, training data)", cv_confusions)

    # Step 2: freeze the choice. Nothing below this line can change it.
    best = select_best_model(cv_metrics)
    print(f"\n=== Selected model: {best} (highest cross-validated ROC-AUC; frozen before testing) ===")

    # Step 3: fit only the selected model on the training data.
    pipe = pipelines[best].fit(X_train, y_train)

    # Step 4: evaluate the selected model once on the test set.
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = pipe.predict(X_test)
    test_rows = {"default_0.5": {"threshold": 0.5, **compute_metrics(y_test, pred, proba)}}
    test_confusions = {"default_0.5": confusion_counts(y_test, pred)}
    if target_recall is not None:
        threshold = threshold_for_recall(y_train, oof_proba[best], target_recall)
        tuned_pred = (proba >= threshold).astype(int)
        label = f"tuned_recall>={target_recall}"
        test_rows[label] = {"threshold": threshold, **compute_metrics(y_test, tuned_pred, proba)}
        test_confusions[label] = confusion_counts(y_test, tuned_pred)

    test_table = pd.DataFrame(test_rows).T.round(3)
    print(f"\n=== Final evaluation of {best} on the test set (evaluated once) ===")
    print(test_table.to_string())
    print_confusions("Confusion counts (test set)", test_confusions)

    names = pipe.named_steps["prep"].get_feature_names_out()
    print("\nMost influential features:")
    for feat, val in top_features(pipe.named_steps["model"], names):
        print(f"  {feat:40s} {val:+.3f}")

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    cv_table.to_csv(out / "model_comparison_cv.csv")
    test_table.to_csv(out / "selected_model_test.csv")
    print(f"\nSaved metrics to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("csv", nargs="?", type=Path, default=ROOT / "data" / "customers.csv")
    parser.add_argument("--target-recall", type=float, default=None,
                        help="also tune the selected model's decision threshold to reach this recall (0-1]")
    args = parser.parse_args()
    main(args.csv, args.target_recall)
