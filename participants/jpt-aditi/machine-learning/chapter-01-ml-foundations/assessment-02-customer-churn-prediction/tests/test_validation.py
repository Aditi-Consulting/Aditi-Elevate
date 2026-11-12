import warnings
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression

from src.validation import cross_validate_models


def test_cross_validate_models_returns_mean_and_std_per_model_without_warnings():
    rng = np.random.default_rng(0)
    X = pd.DataFrame({"a": rng.normal(size=100)})
    y = pd.Series((X["a"] + rng.normal(scale=0.5, size=100) > 0.8).astype(int))
    models = {"baseline": DummyClassifier(strategy="most_frequent"),
              "logreg": LogisticRegression()}

    with warnings.catch_warnings():
        warnings.simplefilter("error")   # the baseline never predicts "Yes": no warning allowed
        table = cross_validate_models(models, X, y)

    assert list(table.index) == ["baseline", "logreg"]
    assert list(table.columns) == ["accuracy", "precision", "recall", "f1", "roc_auc"]
    assert "±" in table.loc["logreg", "recall"]