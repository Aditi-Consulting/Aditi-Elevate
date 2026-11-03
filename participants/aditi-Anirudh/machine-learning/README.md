# Machine Learning

This folder contains my Machine Learning learning work. The current project is
the Chapter 1 sales-data assessment, which loads a sales dataset with pandas and
performs a basic data-quality check.

## Project structure

```text
machine-learning/
├── README.md
└── chapter-01-machine-learning/
    └── assessment-01-machine-learning/
        ├── datasets/
        │   └── sales.csv
        ├── src/
        │   └── app.py
        └── requirements.txt
```

## What the project does

The script reads `datasets/sales.csv`, displays the first five rows, and reports
the number of missing values in each column. The dataset includes order, product,
customer, sales, cost, and profit fields. This is an introductory data-analysis
exercise; it does not yet train or evaluate a machine-learning model.

## Setup and run

From this `machine-learning` folder, create and activate a virtual environment,
install the assessment dependency, and run the script:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\chapter-01-machine-learning\assessment-01-machine-learning\requirements.txt
python .\chapter-01-machine-learning\assessment-01-machine-learning\src\app.py
```

The output contains the first five data rows followed by the missing-value count
for every column. The script loads the CSV relative to its own location, so it
does not require a separate working-directory configuration.
