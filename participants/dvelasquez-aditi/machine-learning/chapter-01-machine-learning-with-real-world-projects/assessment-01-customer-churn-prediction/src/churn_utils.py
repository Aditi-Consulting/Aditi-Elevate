"""Reusable utilities for the customer churn prototype."""
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET = "churn"
ID_COLUMNS = ["customer_id"]


def load_data(path: Union[str, Path]) -> pd.DataFrame:
    """Load a CSV file, raising clear errors for missing or empty files."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Data file is empty: {path}")
    return df


def check_data_quality(df: pd.DataFrame, target: str = TARGET) -> Dict:
    """Return a basic data-quality report (shape, missing values, duplicates, balance)."""
    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found")
    missing = df.isna().sum()
    return {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "missing_by_column": {c: int(n) for c, n in missing.items() if n > 0},
        "rows_with_any_missing_pct": round(float(df.isna().any(axis=1).mean() * 100), 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "target_missing": int(df[target].isna().sum()),
        "target_balance": {str(k): round(float(v), 4)
                           for k, v in df[target].value_counts(normalize=True).items()},
    }


def clean_data(df: pd.DataFrame, target: str = TARGET) -> pd.DataFrame:
    """Drop duplicate rows and rows with a missing target (the target cannot be imputed)."""
    return df.drop_duplicates().dropna(subset=[target]).reset_index(drop=True)


def split_features_target(df: pd.DataFrame, target: str = TARGET,
                          drop_cols: Optional[List[str]] = None) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate the feature matrix from the target, dropping identifier columns."""
    drop = [c for c in (drop_cols if drop_cols is not None else ID_COLUMNS) if c in df.columns]
    X = df.drop(columns=drop + [target])
    return X, df[target].astype(int)


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Impute (median / most frequent), then scale numerics and one-hot encode categoricals.

    Imputers live inside the pipeline so they are fitted on training data only,
    which avoids leaking information from the test set.
    """
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), numeric),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ])


def compute_metrics(y_true, y_pred, y_proba) -> Dict[str, float]:
    """Accuracy, precision, recall, F1 and ROC-AUC for a binary classifier."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_proba),
    }


def top_features(model, feature_names, n: int = 8) -> List[Tuple[str, float]]:
    """Most influential features: coefficients for linear models, importances for trees."""
    if hasattr(model, "coef_"):
        values = np.ravel(model.coef_)
    elif hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    else:
        raise TypeError("Model exposes neither coef_ nor feature_importances_")
    order = np.argsort(np.abs(values))[::-1][:n]
    return [(str(feature_names[i]), float(values[i])) for i in order]
