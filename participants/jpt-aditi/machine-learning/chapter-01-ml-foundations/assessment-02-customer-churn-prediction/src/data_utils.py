import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DISGUISED_NA = {"", "na", "n/a", "nan", "null", "none", "?", "-", "--", "unknown", "missing"}
TEXT_TYPES = ["object", "string"] 

def load_csv_file(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError(f"File {file_path} contains no rows")
    return df


def check_data_quality(df: pd.DataFrame, target: str) -> dict:
    """Return a summary of basic data quality metrics."""
    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found")
    return {
        "n_rows": len(df),
        "n_cols": df.shape[1],
        "missing_per_column": df.isna().sum()[df.isna().sum() > 0].to_dict(),
        "n_duplicates": int(df.duplicated().sum()),
        "target_distribution": df[target].value_counts(normalize=True).round(3).to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

def find_disguised_missing(df):
    """Return {column: count} of text values that aren't NaN but are clearly meant to be missing. 
    For example, "", "null", "unknown", etc. are often used to hide missing values."""
    found = {}
    for col in df.select_dtypes(include=TEXT_TYPES).columns:
        s = df[col].dropna().astype(str).str.strip().str.lower()
        n = int(s.isin(DISGUISED_NA).sum())
        if n:
            found[col] = n
    return found



def find_numeric_as_text(df, min_parse_rate=0.9):
    """Return {column: bad_values} for text columns that should be numeric but aren't, 
    e.g. "123", "456", "N/A", "unknown"."""
    found = {}
    for col in df.select_dtypes(include=TEXT_TYPES).columns:
        s = df[col].dropna().astype(str).str.strip()
        parsed = pd.to_numeric(s, errors="coerce")
        rate = parsed.notna().mean()
        if min_parse_rate <= rate < 1.0:
            found[col] = sorted(set(s[parsed.isna()]))[:5]
    return found

def clean_rows(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """Drop duplicate rows and rows with a missing target."""
    out = df.drop_duplicates().dropna(subset=[target])
    return out.reset_index(drop=True)

def split_features_and_target(df, target, drop_cols=None):
    """Return X (features) and y (binary target: Yes -> 1, No -> 0).
    Labels are matched ignoring case and surrounding spaces ("yes", " No ").
    Any other label raises ValueError instead of being silently treated as 0.
    """
    drop_cols = list(drop_cols) if drop_cols else []
    labels = df[target].astype(str).str.strip().str.lower()
    unexpected = sorted(set(labels) - {"yes", "no"})
    if unexpected:
        raise ValueError(f"Unexpected values in target '{target}': {unexpected}")
    y = (labels == "yes").astype(int)
    X = df.drop(columns=[target] + drop_cols)
    return X, y

def convert_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Convert columns to numbers; unparseable values (e.g. ' ') become NaN."""
    out = df.copy()
    for col in columns:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def build_preprocessor_pipeline(features: pd.DataFrame) -> ColumnTransformer:
    """Return a ColumnTransformer that imputes, scales and one-hot encodes features.
    For Numeric columns Impute and scale ; For categorical columns impute + one-hot encode."""
    numeric_cols = features.select_dtypes(include="number").columns.tolist()
    categorical_cols = features.select_dtypes(exclude="number").columns.tolist()

    # strategy = "median" will replace missing values with the median of the column, which is robust to outliers.
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # strategy="most_frequent" will replace missing values with the most frequent value in the column, 
    # which is a common choice for categorical data.
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    
    return ColumnTransformer([
        ("num", numeric_pipe, numeric_cols),
        ("cat", categorical_pipe, categorical_cols),
    ])

