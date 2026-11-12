import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.evaluate import (
    evaluate_model, 
    compare_models
)

# ---------- evaluate_model ----------

def test_evaluate_model_confusion_counts_add_up():
    X = pd.DataFrame({"a": [0, 1, 2, 3, 4, 5, 6, 7]})
    y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1])
    model = LogisticRegression().fit(X, y)

    m = evaluate_model(model, X, y)

    assert m["TP"] + m["FP"] + m["FN"] + m["TN"] == len(y)
    assert 0.0 <= m["precision"] <= 1.0
    assert 0.0 <= m["recall"] <= 1.0

def test_compare_models():
    X = pd.DataFrame({"a": [0, 1, 2, 3, 4, 5, 6, 7]})
    y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1])
    m1 = LogisticRegression(C=10.0).fit(X, y)
    m2 = LogisticRegression(C=0.1).fit(X, y)

    results = compare_models({"strong": m1, "weak": m2}, X, y)
    assert len(results) == 2
    assert results.index.tolist() == ["strong", "weak"]
    assert "recall" in results.columns
    assert "f1" in results.columns
    assert "precision" in results.columns
