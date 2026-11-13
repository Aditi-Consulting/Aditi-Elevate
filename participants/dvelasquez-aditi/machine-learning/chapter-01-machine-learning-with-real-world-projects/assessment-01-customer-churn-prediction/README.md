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
python src/train.py --target-recall 0.85   # also tune thresholds for 85% recall
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
7. **Metrics:** accuracy, precision, recall, F1 and ROC-AUC on the test set, plus exact
   confusion-matrix counts. An optional recall-targeted decision threshold is available.

## Results
Run on the included synthetic data (400 test rows):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.698 | 0.505 | 0.764 | 0.608 | 0.802 |
| Random Forest | 0.735 | 0.556 | 0.691 | 0.616 | 0.795 |

## Selected model and explanation
**Logistic Regression** is selected. It has the highest ROC-AUC, which does not depend
on a decision threshold and suits an imbalanced target. It also has the higher recall
(0.76 vs 0.69), and for churn recall is the metric that matters most.

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

**What the numbers mean here.** Exact confusion counts on the 400-row test set
(123 churners, 277 loyal customers), at the default 0.5 threshold:

| Model | Churners caught (TP) | Churners missed (FN) | False alarms (FP) | Loyal kept (TN) |
| --- | --- | --- | --- | --- |
| Logistic Regression | 94 | 29 | 92 | 185 |
| Random Forest | 85 | 38 | 68 | 209 |

Logistic Regression catches 9 more churners than Random Forest at the cost of 24 more
false alarms. The extra recall is worth it when saving one churner is worth more than
about 2.7 retention offers (24 / 9). That holds for most subscription businesses, where a
customer's lifetime value is far larger than the cost of an offer, even after allowing
for offers that do not work. Random Forest would be the better pick only if retention
actions were expensive or the retention team could not handle the extra volume.

These cost ratios are an assumption, since no real cost data was provided.

### Threshold tuning for recall
The default 0.5 threshold is not tied to the business goal. `--target-recall` tunes each
model's threshold to reach a recall target. The threshold is chosen on out-of-fold
predictions from the **training** data and only then applied to the test set, so the test
set is not used for tuning.

```bash
python src/train.py --target-recall 0.85
```

Result with a target of 0.85 (tuned thresholds 0.35 and 0.33):

| Model | Threshold | Precision | Recall | F1 | TP | FN | FP | TN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.354 | 0.431 | 0.894 | 0.582 | 110 | 13 | 145 | 132 |
| Random Forest | 0.332 | 0.427 | 0.927 | 0.585 | 114 | 9 | 153 | 124 |

Lowering the threshold raises recall for both models (0.76 to 0.89 for Logistic
Regression) and misses far fewer churners (29 down to 13). The price is more false alarms
(92 up to 145), which is the precision-for-recall trade-off argued above. Once both
models are tuned to the same recall goal they perform almost the same: Random Forest
catches 4 more churners for 8 more false alarms, a much smaller gap than at 0.5.
Recall on the test set lands above the 0.85 target for both models because the threshold
was fitted on training data, so some variation is expected. The selection still stands:
Logistic Regression has the higher ROC-AUC and is easier to explain.

The coefficients are directly interpretable. Churn risk goes up with
month-to-month contracts (+0.89), more support calls (+0.54), higher monthly
charges (+0.45) and electronic-check payment (+0.41). It goes down with two-year
contracts (-0.80) and longer tenure (-0.61).

## Testing
`python -m pytest -q` runs 8 tests covering `load_data`, `check_data_quality`,
`clean_data`, `split_features_target`, `build_preprocessor`, `compute_metrics`,
`confusion_counts` and `threshold_for_recall`.
All pass.

## Limitations
- The dataset is **synthetic**, generated by `generate_data.py` with churn driven by a
  known formula. The metrics show the pipeline works, not real-world performance.
- Single train/test split with no cross-validation or hyperparameter tuning.
- The ROC-AUC gap between the models (0.802 vs 0.795) is small and is within the noise
  of a 400-row test set.
