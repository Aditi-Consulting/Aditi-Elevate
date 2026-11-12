# Customer Churn Prediction Prototype

## Assessment details
Participant:- Jyoti Prakash Thakur
GitHub username:- jpt-aditi
Learning area:- Machine Learning
Chapter:- Python and Machine Learning Foundations (Week 1)
Assessment title / number:- Customer Churn Prediction Prototype

## Project structure

```
assessment-02-customer-churn-prediction/
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Kaggle dataset
├── src/
│   ├── data_utils.py       # load, quality checks, cleaning, split helpers, preprocessor
│   ├── train.py            # builds and fits the model pipelines
│   ├── evaluate.py         # metrics and model comparison table
│   ├── explain.py          # permutation importance and coefficient tables
│   ├── validation.py       # stratified 5-fold cross-validation helpers
├── tests/
│   ├── test_data_utils.py
│   ├── test_evaluate.py
│   └── test_validation.py
├── pytest.ini              # lets pytest import the `src` package
├── main.py                 # runs the whole workflow and prints the results and explanation
├── playground.ipynb        # scratch notebook
└── requirements.txt
```

## How to run

Requires **Python 3.12 or newer**. Run everything from the project root.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m pytest -v
```

## Summary

A Python machine-learning prototype that predicts whether a telecom customer is likely to churn. Below are the details on assessment required steps. There are 19 unit tests covering 15 functions.

### 1. Load data from a CSV file

Dataset: [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/data)

`load_csv_file(file_path)` reads the CSV with pandas and raises an error if the file is empty.

**Findings.** 7,043 customers, 21 columns. The target is `Churn` (Yes/No).

### 2. Perform basic data-quality checks

`check_data_quality` reports shape, missing values per column, duplicate rows, target distribution and dtypes. We then added two checks that look inside text columns: `find_disguised_missing` (values like a blank space, `?`, `N/A` that mean "missing" but are not NaN) and `find_numeric_as_text` (text columns that are mostly numbers, using a parse rate against a `min_parse_rate` threshold of 0.9).

**Findings.**
- Shape: 7,043 rows x 21 columns
- Duplicates: 0 => nothing to remove
- Real NaN values: none 
- `TotalCharges` is text, not a number => convert to numeric
- Disguised missing: 11 blank values in `TotalCharges` => become NaN after conversion
- `tenure = 0` and `Churn = No` => brand-new customers not billed yet, so not random errors; median imputation is fine and 0 is a defensible alternative
- `customerID` has 7,043 unique values => an ID, not a signal, so we can drop it
- Category labels: consistent (`value_counts` shows no `yes`/`Y` variants) => no relabeling needed
- `No phone service` (682 rows), `No internet service` (1,526 rows) are redundant with `PhoneService` and `InternetService`, but not errors. Considering to keep it for now and may be simplify later.
- Target balance: 26.5% churn, 73.5% stay 

### 3. Handle missing values

Fixed the type first (`convert_to_numeric` turns the 11 blanks in `TotalCharges` into NaN). Imputation happens inside the preprocessing pipeline: numeric columns use the **median**, categorical columns use the **most frequent** value. Rows with a missing *target* would be dropped, not imputed, because you cannot invent the answer you are trying to predict (none exist in this dataset).

### 4. Separate features and target

`split_features_target` turns `Churn` into a 0/1 target (`Yes` = 1) and drops the target and `customerID` from the features, leaving 19 feature columns. `customerID` is a unique label. Keeping it would only let a model memorize individual customers.

### 5. Split the data into training and testing sets

`train_test_split` will split the data and gives 5,634 training rows and 1,409 test rows. `stratify=y` keeps the 26.5% churn rate equal in both sets, so a random split cannot skew the evaluation. `random_state=20` makes the split reproducible. Scaling helps Logistic Regression because `TotalCharges` (thousands) would otherwise dominate small-range columns. One-hot encoding turns categories into numbers a model can use.

The preprocessor (`ColumnTransformer`) treats 4 numeric columns (median fill, then standard scaling) and 15 categorical columns (most-frequent fill, then one-hot encoding with `handle_unknown="ignore"`). The 15 categorical columns become 41 binary columns, so the transformed training data has 4 + 41 = 45 columns.

### 6. Train at least two classification models

Built a full `Pipeline` (preprocessor + classifier) for each model in `src/train.py`, and also added a baseline that always predicts "No".

Logistic Regression: Simple and interpretable
Random Forest: Flexible, captures interactions
Baseline: The bar every real model must clear

**Parameter Details:**
* Note: The settings are not tuned. They were chosen as reasonable starting points. We can do hyperparameter tuning to for better values.

| Parameter | Model | What it does | Effect here |
|---|---|---|---|
| `max_iter=1000` | Logistic Regression | Upper limit on optimizer steps. The default (100) can stop before the optimizer has finished. | A safe ceiling. If the optimizer already converged, the result does not change. |
| `class_weight="balanced"` | both | Each class gets the weight `n_samples / (n_classes * n_in_class)`. With 26.5% churners, a churner counts about 1.9 and a non-churner about 0.7, so a missed churner costs the model about 2.8 times more. | Higher recall, lower precision. The predicted probabilities are inflated, so they are not true churn rates. |
| `random_state=20` | both | Fixes the random choices so a rerun gives the same result. | Logistic Regression's default solver is deterministic, so the seed is harmless there. For Random Forest it fixes which rows and features each tree sees. |
| `n_estimators=300` | Random Forest | Number of trees. Each tree trains on a random resample of the rows and considers random subsets of features. The forest averages their votes. | More trees give more stable results with diminishing returns, and training takes longer. It does not cause overfitting. The default is 100. |
| `min_samples_leaf=5` | Random Forest | Every leaf must contain at least 5 training customers. The default of 1 lets a tree memorize individual customers. | Limits overfitting and smooths the probabilities. A train/test gap remains. |
| `n_jobs=-1` | Random Forest | Train trees in parallel on all CPU cores. | Speed only. The results do not change. |

**Findings (accuracy).**

| Model | Train accuracy | Test accuracy |
|---|---|---|
| Baseline (always No) | - | 0.735 |
| Logistic Regression | 0.748 | 0.757 |
| Random Forest | about 0.83 | 0.766 |

- Random Forest shows a train/test gap of about 0.065 (**overfitting**: it fits training quirks that do not carry over). 
- Logistic Regression's train and test accuracy are within 0.01 of each other (test is slightly higher by chance), so it shows no overfitting. 
- Accuracy barely beats the baseline, which is the sign that accuracy is the wrong yardstick here.

### 7. Compare the models using at least three relevant metrics

`compare_models` in `src/evaluate.py` computes accuracy, precision, recall, F1 and ROC-AUC, plus the confusion-matrix counts, for every model on the test set.

Precision: Of the customers I flagged as churners, how many really churned?
Recall: Of the customers who really churned, how many did I catch?
F1: One number balancing precision and recall (harmonic mean, so a weak one drags it down)
ROC-AUC: How well does the model rank churners above non-churners, regardless of cutoff? (0.5 = coin flip, 1.0 = perfect)

**Results (test set: 374 churners, 1,035 non-churners).**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (always No) | 0.735 | 0.000 | 0.000 | 0.000 | 0.500 | 0 | 0 | 374 | 1035 |
| Logistic Regression | 0.757 | 0.529 | 0.789 | 0.633 | 0.847 | 295 | 263 | 79 | 772 |
| Random Forest | 0.766 | 0.542 | 0.767 | 0.635 | 0.844 | 287 | 243 | 87 | 792 |

**Findings and reasoning.**

- The baseline reaches 0.735 accuracy with **recall 0**: it never finds a single churner. Accuracy hid that, which is why we use several metrics.
- Both real models catch roughly 77% to 79% of churners (recall) at about 53% to 54% precision, and both rank customers equally well (ROC-AUC about 0.84 to 0.85).
- The two models are close. Logistic Regression caught 8 more churners (295 vs 287), but raised 20 more false alarms (263 vs 243). Random Forest is slightly ahead on precision, F1 and accuracy.
- Precision matters when each retention offer is expensive (false alarms waste money); recall matters when losing a customer costs far more than an offer. 

**Leading candidate.** Random Forest, because on this split it has slightly better precision, F1 and accuracy at slightly lower recall. We will perform cross-validation and examine both models before the final choice.

### 8. Check the comparison with 5-fold stratified cross-validation 

`src/validation.py` has `cross_validate_models()` (a `StratifiedKFold` with 5 folds, shuffling and `random_state=20`), which scores every full pipeline on the same folds and reports each metric as mean +/- standard deviation. It runs on the **training set only** (5,634 rows), so the test set stays untouched as a final, honest check.

A single split gives a single score, and with only 374 churners in the test set small differences are noise. Cross-validation repeats the evaluation 5 times (train on 4 folds, score on the 5th, rotate) and shows how much each metric moves. *Stratified* keeps the 26.5% churn rate in every fold. 

**Results** (mean +/- std across the 5 folds):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Baseline (always No) | 0.735 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.500 +/- 0.000 |
| Logistic Regression | 0.744 +/- 0.015 | 0.512 +/- 0.018 | 0.805 +/- 0.024 | 0.626 +/- 0.016 | 0.844 +/- 0.013 |
| Random Forest | 0.762 +/- 0.013 | 0.537 +/- 0.017 | 0.763 +/- 0.026 | 0.630 +/- 0.016 | 0.845 +/- 0.014 |

**Findings.**

- ROC-AUC (0.844 vs 0.845) and F1 (0.626 vs 0.630) are effectively tied: the F1 gap of 0.004 is far smaller than the fold-to-fold spread of 0.016.
- Random Forest has higher precision (0.537 vs 0.512) and accuracy (0.762 vs 0.744). Logistic Regression has higher recall (0.805 vs 0.763). Each gap is roughly one to two standard deviations, so these are tendencies, not firm differences.
- This corrects a conclusion from the single split, where recall looked identical: across folds, Logistic Regression catches about 4 points more churners on average.
- Both models are far better than the baseline, which has recall 0 and ROC-AUC 0.5.

**Model Choice.** On the metrics alone the models are close, so the choice depends on what the business cares about. Random Forest fits if wasted retention offers (false alarms) matter more. Logistic Regression fits if catching every churner matters more, and it is also easier to explain. We keep Random Forest on the stated assumption that missing a churner is not very costly. 

### 9. Features Importance

`src/explain.py` looks at the models through two lenses. If both agree on the main drivers, that is stronger evidence than either alone. Permutation importance says how much the model relies on a feature, but not which direction it pushes. In case of Logistic Regression coefficients a positive coefficient pushes a customer toward churn, a negative one pushes away.

**Findings.**
Random Forest permutation importance (drop in F1, mean +/- std): 

| Feature | Importance |
|---|---|
| Contract | 0.0925 +/- 0.0106 |
| InternetService | 0.0356 +/- 0.0069 |
| tenure | 0.0259 +/- 0.0066 |
| TechSupport | 0.0073 +/- 0.0040 |
| TotalCharges | 0.0048 +/- 0.0059 |

Everything below the top three is small (0.008 or less, within about two standard deviations of zero). Features such as `PhoneService`, `Dependents` and `gender` sit at or just below zero (about -0.004 to 0 in the run we checked). Shuffling them does not hurt the model, so it does not rely on them (small negative values are noise).

Logistic Regression coefficients (numeric features are standardized, so their sizes are comparable):

| Pushes toward churn | Coefficient | Pushes away from churn | Coefficient |
|---|---|---|---|
| TotalCharges | +0.714 | tenure | -1.405 |
| Month-to-month contract | +0.663 | Two-year contract | -0.738 |
| Fiber optic internet | +0.263 | DSL internet | -0.316 |
| Electronic check payment | +0.233 | Paperless billing = No | -0.259 |

**Reading the results.** Both lenses agree on the main drivers - contract type, tenure and internet service. Customers on a month-to-month contract, with short tenure and fiber-optic internet, are at the highest risk. Long contracts and long tenure protect against churn. 

### 10. Final model decision: Random Forest.

- ROC-AUC is the same for both models (0.844 vs 0.847 on the test split; 0.845 vs 0.844 in cross-validation), so both rank churners well. F1 is effectively tied in cross-validation (0.630 vs 0.626).
- Random Forest has higher precision. On the test split, false alarms drop from 263 to 243, which is 20 fewer wasted retention offers (about 8% fewer). In cross-validation, precision is 0.537 vs 0.512.
- Logistic Regression catches slightly more churners. On the test split its recall is 0.789 vs 0.767 (8 more customers), and in cross-validation it is about 4 points higher (0.805 vs 0.763).
- Random Forest has higher accuracy (test split 0.766 vs 0.757; cross-validation 0.762 vs 0.744), though accuracy is the least informative metric on imbalanced data.
- Assumption: missing a churner is judged less costly than wasting retention offers, so precision is prioritized over recall. If the business values catching every churner, or needs a simple and easily explained model, Logistic Regression is the better pick.

## Improvements

- **No hyperparameter tuning.** Model settings were chosen for sensible defaults, not searched.
- **Redundant categories.** `No internet service` / `No phone service` duplicate information in other columns and could be simplified.
- **Interpretation limits.** Coefficients of correlated columns (`MonthlyCharges`, `TotalCharges`, `tenure`) should not be read individually, and importance describes what the model uses, not what causes churn.


## Submission checklist- 
[X] My work is in my participant folder under the correct chapter and assessment.  
[X] My assessment README includes setup and execution instructions.  
[X] I ran my code or restarted and ran all notebook cells successfully.  
[X] Required dependencies and references are documented. 
[X] I checked that the submission contains no credentials or restricted data.  
[X] I reviewed the changed files and removed unrelated changes.  

