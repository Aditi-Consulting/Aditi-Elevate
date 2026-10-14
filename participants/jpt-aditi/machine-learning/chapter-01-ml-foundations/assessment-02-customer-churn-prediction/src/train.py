from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.data_utils import build_preprocessor_pipeline


def build_models(X_train):
    """Return a dictionary of models, each wrapped with a preprocessing pipeline.
    The parameters may not be optimal, but they are reasonable for this dataset.
    We can improve them using hyperparameter tuning later."""
    return {
        "Logistic Regression": Pipeline([
            ("prep", build_preprocessor_pipeline(X_train)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced",
                                       random_state=20)),
        ]),
        "Random Forest": Pipeline([
            ("prep", build_preprocessor_pipeline(X_train)),
            ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                           class_weight="balanced",
                                           random_state=20, n_jobs=-1)),
        ]),
    }


def train_models(models, X_train, y_train):
    """Fit every model on the training data only. 
    We will evaluate them on the test set."""
    for model in models.values():
        model.fit(X_train, y_train)
    return models