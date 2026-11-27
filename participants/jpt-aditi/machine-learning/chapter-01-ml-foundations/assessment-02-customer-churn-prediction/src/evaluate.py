import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)


def evaluate_model(model, X_test, y_test) -> dict:
    """Return the key classification metrics for one fitted model."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]      # probability of churn
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "TP": int(tp), "FP": int(fp), "FN": int(fn), "TN": int(tn),
    }


def compare_models(models: dict, X_test, y_test) -> pd.DataFrame:
    """Evaluate all models and return one row per model with the metrics as columns."""
    rows = {name: evaluate_model(m, X_test, y_test) for name, m in models.items()}
    return pd.DataFrame.from_dict(rows, orient="index").round(3)