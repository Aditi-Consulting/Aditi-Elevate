"""Customer churn prototype - run this file to read the whole story top to bottom."""
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split

from src.data_utils import (build_preprocessor_pipeline, check_data_quality, clean_rows,
                            convert_to_numeric, find_disguised_missing,
                            find_numeric_as_text, load_csv_file,
                            split_features_and_target)
from src.evaluate import compare_models
from src.inspection import logistic_coefficients, permutation_importance_table
from src.train import build_models, train_models
from src.validation import cross_validate_models

TARGET = "Churn"
FILE_PATH = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
BASELINE = "Baseline (always No)"

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


color = "\033[33m"
reset = "\033[0m"
def log_step(number: int, title: str, description: str):
    print(f"\n{color}{'=' * 78}\nSTEP {number}: {title}\nDesc: {description}\n{'-' * 78}{reset}\n")


# --------------------------------------------------------------------------
log_step(1, "Load the data", "Everything starts from what the file really contains.")
df = load_csv_file(FILE_PATH)
print(f"{len(df)} customers, {df.shape[1]} columns.")

# --------------------------------------------------------------------------
log_step(2, "Check data quality",
     "We need to know what is missing, duplicated, disguised as missing, or stored as the wrong type.\n" \
     "We will use \"Churn\" as the target column.")
raw_report = check_data_quality(df, TARGET)
print("- Rows with a real missing value (NaN):", raw_report["missing_per_column"] or "none")
print("- Duplicate rows:", raw_report["n_duplicates"])
print("- Blank/placeholder text hiding as data:", find_disguised_missing(df) or "none")
print("- Numbers stored as text:", find_numeric_as_text(df) or "none")

print("\n* NaN count says 'all fine', but the property checks found a problem.")
print("... Fix: convert those columns to numbers; blanks become real NaN.")
df = convert_to_numeric(df, ["TotalCharges"])
df = clean_rows(df, TARGET)
fixed = check_data_quality(df, TARGET)
print("\nAfter the fix, missing values per column:", fixed["missing_per_column"])
print("(They are filled later, inside the pipeline, using training data only.)")
print("\nTarget balance:", fixed["target_distribution"])
print("* Only about a quarter of customers churn, so we have an imbalanced dataset. This will affect how we evaluate models.")

# --------------------------------------------------------------------------
log_step(3, "Separate features from the target and split",
     "We will separate the features from the target, then split into a training set and a test set. \n" \
     "The test set plays 'future customers', so it must stay unseen until the end.")
X, y = split_features_and_target(df, TARGET, drop_cols=["customerID"])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=20)
print(f"Train: {X_train.shape[0]} rows   Test: {X_test.shape[0]} rows   "
      f"Features: {X_train.shape[1]}")
print(f"Churn rate  train: {y_train.mean():.3f}   test: {y_test.mean():.3f}"
      "   (stratify keeps them equal)")
print("\n... The preprocessor pipeline will fill missing values, scale numeric features, and one-hot encode categorical features.")
n_features = build_preprocessor_pipeline(X_train).fit_transform(X_train).shape[1]
print(f"\nAfter imputing, scaling and one-hot encoding: {n_features} model inputs.")

# --------------------------------------------------------------------------
log_step(4, "Train two models and compare them on the test set",
     "Different models make different trade-offs. Several metrics expose them.")

print("... Creating Baseline Model: always answer 'No' (no churn).\n")
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(f"Always answering 'No' scores {baseline.score(X_test, y_test):.3f} accuracy "
      "and finds 0 churners.")
print("* Any real model must do better than the baseline (on recall, not just accuracy).")

print("\n... Creating two real models: Logistic Regression and Random Forest.\n")
models = train_models(build_models(X_train), X_train, y_train)
results = compare_models({BASELINE: baseline, **models}, X_test, y_test)
print(results)
rf, lr = results.loc["Random Forest"], results.loc["Logistic Regression"]
print(f"\n* Random Forest raises fewer false alarms ({int(rf.FP)} vs {int(lr.FP)}) "
      f"and has higher precision ({rf.precision:.3f} vs {lr.precision:.3f}).")
print(f"* Logistic Regression catches {int(lr.TP) - int(rf.TP)} more churner(s) "
      f"(recall {lr.recall:.3f} vs {rf.recall:.3f}).")
print(f"* ROC-AUC is nearly identical ({rf.roc_auc:.3f} vs {lr.roc_auc:.3f}).")

# --------------------------------------------------------------------------
log_step(5, "Check the comparison with 5-fold cross-validation",
     "On the test set, Random Forest and Logistic Regression are close. Let's see if that holds across folds. \n" \
     "We will use 5-fold stratified cross-validation, which keeps the churn rate equal in every fold.")
cv_results = cross_validate_models(
    {BASELINE: baseline, **build_models(X_train)}, X_train, y_train)
print(cv_results)
print("\n* We will call it a tie if the mean ± std of every metric overlaps.")
print("* Overall the models are close; the real difference is precision vs recall.")

# --------------------------------------------------------------------------
log_step(6, "Explain what drives churn",
     "A prediction is more useful when we know what pushes it up or down.")
print("Random Forest - features whose shuffling hurts F1 most (permutation importance):")
print(permutation_importance_table(models["Random Forest"], X_test, y_test).head(8).round(4))
coefs = logistic_coefficients(models["Logistic Regression"])
print("\nLogistic Regression - strongest push TOWARD churn:")
print(coefs.head(6).round(3))
print("\nLogistic Regression - strongest push AWAY from churn:")
print(coefs.tail(6).round(3))
print("\nNote: Importance shows what the model uses, not what causes churn.")

# --------------------------------------------------------------------------
log_step(7, "Select Model", "Explain the selected model and the assumption behind it.")
print("Selected model: Random Forest.")
print("Overall both models are close, but Random Forest has a slight edge in terms of precision.")
print("Assumption: Wasting a retention offer on a loyal customer costs more than")
print("missing a churner. If missing a churner is costlier, or individual predictions")
print("must be explained, choose Logistic Regression instead.")
