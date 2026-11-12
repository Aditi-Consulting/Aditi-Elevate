import pytest
import numpy as np
import pandas as pd

from src.data_utils import (
    build_preprocessor_pipeline,
    check_data_quality,
    clean_rows,
    convert_to_numeric,
    find_disguised_missing,
    find_numeric_as_text,
    load_csv_file,
    split_features_and_target,
)


# ---------- convert_to_numeric ----------

def test_convert_to_numeric_turns_blank_into_nan():
    df = pd.DataFrame({"TotalCharges": ["29.85", " ", "1889.5", 3.6]})

    out = convert_to_numeric(df, ["TotalCharges"])

    assert pd.api.types.is_numeric_dtype(out["TotalCharges"])
    assert out["TotalCharges"].isna().tolist() == [False, True, False, False]
    assert out["TotalCharges"].iloc[0] == pytest.approx(29.85)

# I added a numeric value to df to check that convert_to_numeric handles a mix of numeric and text values correctly.

def test_convert_to_numeric_does_not_modify_original():
    df = pd.DataFrame({"TotalCharges": ["1.5", " "]})

    convert_to_numeric(df, ["TotalCharges"])

    assert df["TotalCharges"].tolist() == ["1.5", " "]   # input untouched


# ---------- find_numeric_as_text ----------

def test_find_numeric_as_text_flags_mostly_numeric_text_column():
    # 9 numbers + 1 blank -> parse rate 0.9, which meets the default threshold
    df = pd.DataFrame({"amount": [str(i) for i in range(1, 10)] + [" "]})

    assert find_numeric_as_text(df) == {"amount": [""]}


def test_find_numeric_as_text_ignores_real_text_columns():
    df = pd.DataFrame({"gender": ["Male", "Female", "Male", "Female"]})

    assert find_numeric_as_text(df) == {}


def test_find_numeric_as_text_respects_min_parse_rate():
    df = pd.DataFrame({"mixed": ["1", "2", "three", "four"]})   # parse rate 0.5

    assert find_numeric_as_text(df, min_parse_rate=0.9) == {}
    assert "mixed" in find_numeric_as_text(df, min_parse_rate=0.4)


# ---------- find_disguised_missing ----------

def test_find_disguised_missing_counts_placeholders():
    df = pd.DataFrame({
        "a": ["x", " ", "N/A", "?"],      # three placeholders
        "b": ["x", "y", "z", "w"],        # clean
    })

    assert find_disguised_missing(df) == {"a": 3}


def test_find_disguised_missing_ignores_real_nan():
    df = pd.DataFrame({"a": ["x", np.nan, "y"]})   # NaN is "real" missing, not disguised

    assert find_disguised_missing(df) == {}


# ---------- split_features_target ----------

def test_split_features_target_encodes_target_and_drops_columns():
    df = pd.DataFrame({
        "customerID": ["a", "b", "c"],
        "tenure": [1, 2, 3],
        "Churn": ["Yes", "No", "Yes"],
    })

    X, y = split_features_and_target(df, "Churn", drop_cols=["customerID"])

    assert list(X.columns) == ["tenure"]
    assert y.tolist() == [1, 0, 1]


def test_split_features_target_keeps_all_features_by_default():
    df = pd.DataFrame({"id": [1, 2], "Churn": ["No", "Yes"]})

    X, _ = split_features_and_target(df, "Churn")

    assert list(X.columns) == ["id"]

def test_split_features_target_ignores_case_and_spaces():
    df = pd.DataFrame({"f": [1, 2, 3, 4], "Churn": ["yes", " No ", "YES", "no"]})

    _, y = split_features_and_target(df, "Churn")

    assert y.tolist() == [1, 0, 1, 0]


def test_split_features_target_rejects_unexpected_label():
    df = pd.DataFrame({"f": [1, 2], "Churn": ["Yes", "Maybe"]})

    with pytest.raises(ValueError, match="maybe"):
        split_features_and_target(df, "Churn")

# ---------- clean_rows ----------

def test_clean_rows_drops_duplicates_and_missing_target_and_resets_index():
    df = pd.DataFrame({
        "x": [1, 1, 2, 3],
        "Churn": ["No", "No", np.nan, "Yes"],
    })

    out = clean_rows(df, "Churn")

    assert len(out) == 2                       # duplicate and NaN-target rows removed
    assert out.index.tolist() == [0, 1]        # index reset


# ---------- check_data_quality / load_data ----------

def test_check_data_quality_reports_counts():
    df = pd.DataFrame({
        "a": [1.0, np.nan, 3.0, 3.0],
        "Churn": ["No", "No", "Yes", "Yes"],
    })

    report = check_data_quality(df, "Churn")

    assert report["n_rows"] == 4
    assert report["missing_per_column"] == {"a": 1}
    assert report["n_duplicates"] == 1
    assert report["target_distribution"] == {"No": 0.5, "Yes": 0.5}


def test_check_data_quality_raises_for_unknown_target():
    with pytest.raises(KeyError):
        check_data_quality(pd.DataFrame({"a": [1]}), "Churn")


def test_load_data_raises_for_file_with_no_rows(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("a,b\n")                   # header only

    with pytest.raises(ValueError):
        load_csv_file(str(path))


# ---------- build_preprocessor ----------

def test_preprocessor_fills_missing_values_and_handles_unseen_category():
    X_train = pd.DataFrame({
        "tenure": [1.0, 2.0, np.nan, 4.0],
        "contract": ["Month", "Year", "Month", np.nan],
    })
    X_new = pd.DataFrame({"tenure": [np.nan], "contract": ["Two year"]})   # unseen label

    prep = build_preprocessor_pipeline(X_train)
    Xt = prep.fit_transform(X_train)
    Xt = Xt.toarray() if hasattr(Xt, "toarray") else Xt
    Xn = prep.transform(X_new)                 # must not crash
    Xn = Xn.toarray() if hasattr(Xn, "toarray") else Xn

    assert not np.isnan(Xt).any()
    assert not np.isnan(Xn).any()
    assert Xt.shape[0] == 4


