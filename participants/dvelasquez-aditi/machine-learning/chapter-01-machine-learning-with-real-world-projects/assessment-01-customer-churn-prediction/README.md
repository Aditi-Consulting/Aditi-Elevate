# Assessment 01 — Customer Churn Prediction Prototype

- Participant: Daniel Velasquez (`dvelasquez-aditi`)
- Area / chapter: Machine Learning — Chapter 01, Machine Learning with Real World Projects

## Objective
Predict whether a customer is likely to churn. The prototype loads a CSV, checks
data quality, handles missing values, splits features and target, trains two
classifiers, compares them on several metrics and explains the selected model.

## Project layout
```
data/customers.csv       Synthetic dataset (regenerate with generate_data.py)
src/generate_data.py     Creates the dataset with missing values and duplicates
src/churn_utils.py       Utility functions (load, quality check, clean, split, preprocess, metrics)
src/train.py             End-to-end pipeline: quality report, training, comparison, explanation
tests/test_churn_utils.py  Unit tests for the utility functions
```

## Setup
Python 3.9+.
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## How to run
```bash
python src/generate_data.py          # optional: recreate data/customers.csv
python src/train.py                  # or: python src/train.py path/to/your.csv
python src/train.py --target-recall 0.85   # also tune the threshold for 85% recall
python -m pytest -q                  # unit tests
```
To use another dataset, supply a CSV with a binary `churn` column (0/1) and an
optional `customer_id` column; other columns are treated as features.

## Approach
1. **Load:** `load_data` reads the CSV and fails clearly on a missing or empty file.
2. **Data quality:** `check_data_quality` reports shape, missing values per column,
   duplicate rows and target balance. `clean_data` drops duplicates and rows with a
   missing target.
3. **Missing values:** numeric columns use median imputation and categorical columns
   use most-frequent imputation. Imputers sit inside the sklearn pipeline, so they
   are fitted on training data only and the test set does not leak.
4. **Features and target:** `split_features_target` drops the ID column and separates `churn`.
   Numerics are standardised and categoricals one-hot encoded.
5. **Split:** 80/20 train/test, stratified on the target, fixed seed.
6. **Models:** Logistic Regression and Random Forest, both with balanced class weights
   because churners are the minority class (about 31%).
7. **Model selection (training data only):** both models are compared with 5-fold
   cross-validation on the training set, using accuracy, precision, recall, F1, ROC-AUC
   and exact confusion counts. The best model (highest cross-validated ROC-AUC, F1 as
   tie-break) is chosen by `select_best_model` and **frozen**.
8. **Final evaluation (test set, once):** only the selected model is fitted on the
   training set and evaluated once on the held-out test set. The test set plays no part
   in choosing between models, so the reported performance is an unbiased estimate.
9. **Optional threshold tuning:** a recall-targeted decision threshold, chosen from the
   same training-only out-of-fold predictions (see below).

## Results
Run on the included synthetic data (1,600 training rows, 400 test rows).

**Step 1 — model comparison, 5-fold cross-validation on the training data:**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.706 | 0.514 | 0.729 | 0.603 | 0.778 |
| Random Forest | 0.691 | 0.496 | 0.639 | 0.558 | 0.748 |

Logistic Regression is selected and frozen here, before the test set is touched.

**Step 2 — final evaluation of Logistic Regression on the test set (evaluated once):**

| Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | --- | --- | --- | --- |
| 0.698 | 0.505 | 0.764 | 0.608 | 0.802 |

## Selected model and explanation
**Logistic Regression** is selected from the training-only cross-validation. It has the
highest ROC-AUC (0.778 vs 0.748), which does not depend on a decision threshold and suits
an imbalanced target. It also has the higher recall (0.73 vs 0.64), and for churn recall
is the metric that matters most.

**Why recall matters more than precision for churn.** The two errors do not cost the same:
- A *false negative* (a churner we miss) means the customer leaves and we lose all of
  their future revenue. Winning a replacement customer typically costs several times
  more than keeping an existing one.
- A *false positive* (a loyal customer we flag) costs one retention action, such as a
  call, an email or a modest discount. That is cheap, and the customer is still
  retained.

Because a missed churner costs much more than a wasted offer, we want to catch as many
churners as possible and accept some extra false alarms. Precision still matters, since
retention budgets are limited and flagging everyone is not a strategy, so F1 and
precision are monitored as guard rails rather than as the goal.

**What the numbers mean here.** Exact confusion counts from the cross-validation on the
1,600 training rows (490 churners, 1,110 loyal customers), at the default 0.5 threshold:

| Model | Churners caught (TP) | Churners missed (FN) | False alarms (FP) | Loyal kept (TN) |
| --- | --- | --- | --- | --- |
| Logistic Regression | 357 | 133 | 337 | 773 |
| Random Forest | 313 | 177 | 318 | 792 |

Logistic Regression catches 44 more churners than Random Forest at the cost of only 19
more false alarms. That is a very favourable trade: the extra recall pays off as long as
saving one churner is worth more than about 0.4 retention offers (19 / 44), which holds
for essentially any subscription business. Random Forest would be the better pick only if
retention actions were extremely expensive. These cost ratios are an assumption, since no
real cost data was provided.

### Threshold tuning for recall
The default 0.5 threshold is not tied to the business goal. `--target-recall` tunes the
**selected** model's threshold to reach a recall target. The threshold is chosen on
out-of-fold predictions from the **training** data, the same data used for model
selection, and only then applied to the test set. The test set is never used for tuning
or selection.

```bash
python src/train.py --target-recall 0.85
```

Final test-set evaluation of Logistic Regression at both operating points (both fixed
before looking at the test set):

| Operating point | Threshold | Precision | Recall | F1 | TP | FN | FP | TN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Default | 0.500 | 0.505 | 0.764 | 0.608 | 94 | 29 | 92 | 185 |
| Tuned for recall ≥ 0.85 | 0.354 | 0.431 | 0.894 | 0.582 | 110 | 13 | 145 | 132 |

Lowering the threshold raises recall (0.76 to 0.89) and misses far fewer churners
(29 down to 13). The price is more false alarms (92 up to 145), which is the
precision-for-recall trade-off argued above. Recall on the test set lands above the 0.85
target because the threshold was fitted on training data, so some variation is expected.

The coefficients are directly interpretable. Churn risk goes up with
month-to-month contracts (+0.89), more support calls (+0.54), higher monthly
charges (+0.45) and electronic-check payment (+0.41). It goes down with two-year
contracts (-0.80) and longer tenure (-0.61).

## Testing
`python -m pytest -q` runs 9 tests covering `load_data`, `check_data_quality`,
`clean_data`, `split_features_target`, `build_preprocessor`, `compute_metrics`,
`confusion_counts`, `threshold_for_recall` and `select_best_model`.
All pass.

## Limitations
- The dataset is **synthetic**, generated by `generate_data.py` with churn driven by a
  known formula. The metrics show the pipeline works, not real-world performance.
- Models use fixed hyperparameters; there is no hyperparameter search. Cross-validation is
  used only for model selection and threshold tuning.
- The test set has 400 rows (123 churners), so test metrics carry a few points of noise.
