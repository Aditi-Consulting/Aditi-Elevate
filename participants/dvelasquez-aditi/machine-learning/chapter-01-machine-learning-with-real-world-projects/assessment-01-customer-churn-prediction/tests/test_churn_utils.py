import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from churn_utils import (build_preprocessor, check_data_quality, clean_data,  # noqa: E402
                         compute_metrics, load_data, split_features_target)


@pytest.fixture
def df():
    return pd.DataFrame({
        "customer_id": ["a", "b", "c", "c"],
        "tenure": [1.0, np.nan, 5.0, 5.0],
        "contract": ["m", "y", None, None],
        "churn": [1, 0, 1, 1],
    })


def test_load_data_errors_and_reads(tmp_path, df):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "missing.csv")
    path = tmp_path / "d.csv"
    df.to_csv(path, index=False)
    assert load_data(path).shape == df.shape


def test_check_data_quality_reports_issues(df):
    report = check_data_quality(df)
    assert report["rows"] == 4
    assert report["missing_by_column"] == {"tenure": 1, "contract": 2}
    assert report["duplicate_rows"] == 1
    assert report["target_balance"]["1"] == 0.75
    with pytest.raises(KeyError):
        check_data_quality(df, target="nope")


def test_clean_data_removes_duplicates_and_missing_target(df):
    df.loc[0, "churn"] = np.nan
    cleaned = clean_data(df)
    assert len(cleaned) == 2 and cleaned["churn"].notna().all()


def test_split_features_target_drops_id_and_target(df):
    X, y = split_features_target(df)
    assert list(X.columns) == ["tenure", "contract"]
    assert y.tolist() == [1, 0, 1, 1]


def test_build_preprocessor_imputes_missing_values(df):
    X, _ = split_features_target(df)
    out = build_preprocessor(X).fit_transform(X)
    assert not np.isnan(np.asarray(out, dtype=float)).any()


def test_compute_metrics_perfect_and_worst():
    perfect = compute_metrics([0, 1, 1, 0], [0, 1, 1, 0], [0.1, 0.9, 0.8, 0.2])
    assert all(v == 1.0 for v in perfect.values())
    assert compute_metrics([0, 1], [1, 0], [0.9, 0.1])["accuracy"] == 0.0
