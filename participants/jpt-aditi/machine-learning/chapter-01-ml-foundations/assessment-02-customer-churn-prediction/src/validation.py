import pandas as pd
from sklearn.metrics import f1_score, make_scorer, precision_score
from sklearn.model_selection import StratifiedKFold, cross_validate

# zero_division=0: a model that never predicts "Yes" (e.g the baseline model) scores 0, without warnings
SCORING = {
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": "recall",
    "f1": make_scorer(f1_score, zero_division=0),
    "roc_auc": "roc_auc",
}


def cross_validate_models(models: dict, X, y) -> pd.DataFrame:
    """Cross-validate every model; show 'mean ± std' of each metric across folds."""

    # setup 5-fold stratified cross-validation
    # StratifiedKFold ensures that each fold has the same proportion of classes as the original dataset, 
    # which is important for imbalanced datasets. (in this case, only about 26.5% of customers churn)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=20) 
    rows = {}
    for name, model in models.items():
        scores = cross_validate(model, X, y, cv=cv, scoring=SCORING)
        rows[name] = {
            metric: f"{scores[f'test_{metric}'].mean():.3f} ± {scores[f'test_{metric}'].std():.3f}"
            for metric in SCORING
        }
    return pd.DataFrame.from_dict(rows, orient="index")