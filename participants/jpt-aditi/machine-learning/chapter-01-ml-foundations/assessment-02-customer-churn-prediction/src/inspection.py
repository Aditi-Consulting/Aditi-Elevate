import pandas as pd
from sklearn.inspection import permutation_importance


def permutation_importance_table(model, X_test, y_test, scoring="f1",
                                 n_repeats=10, random_state=20) -> pd.DataFrame:
    """Shuffle one raw column at a time; report how much the score drops.
    This will help us understand which features are most important for the model's predictions."""
    result = permutation_importance(model, X_test, y_test, scoring=scoring,
                                    n_repeats=n_repeats, random_state=random_state,
                                    n_jobs=-1)
    table = pd.DataFrame({
        "feature": X_test.columns,
        "importance": result.importances_mean,
        "std": result.importances_std,
    })
    return table.sort_values("importance", ascending=False).reset_index(drop=True)


def logistic_coefficients(model) -> pd.DataFrame:
    """Coefficient per encoded feature: positive = pushes toward churn, negative = pushes toward no churn.
    This will help us understand which features are most important for the model's predictions."""
    names = model.named_steps["prep"].get_feature_names_out()
    coefs = model.named_steps["clf"].coef_[0]
    table = pd.DataFrame({"feature": names, "coefficient": coefs})
    return table.sort_values("coefficient", ascending=False).reset_index(drop=True)