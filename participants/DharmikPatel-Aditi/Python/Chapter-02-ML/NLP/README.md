# Sales Data Analysis with Pandas

A Jupyter Notebook project that loads sales records from a CSV file using Pandas, inspects the initial rows of the dataset, and checks for missing values across all columns.

## What It Does

* **Data Loading:** Reads `sales.csv` into a Pandas `DataFrame` (`pd.read_csv()`).
* **Data Preview:** Displays the first five rows of the dataset (`df.head()`) to verify structure and values.
* **Missing Value Detection:** Calculates and prints the count of missing (`NaN`) entries in each column (`df.isnull().sum()`).

## Project Structure

```text
NLP/
├── src/
│   ├── main.ipynb       # Jupyter Notebook containing the Pandas analysis
│   └── sales.csv        # Sample sales dataset with missing values
└── README.md            # Project documentation
```

## Prerequisites

* Python 3.10 or higher
* `pandas` and `ipykernel` installed:
  ```bash
  pip install pandas ipykernel
  ```

## How to Execute

1. Open `src/main.ipynb` in VS Code (or Jupyter Notebook).
2. Click **Select Kernel** in the top-right corner and choose your Python environment.
3. Ensure `sales.csv` is located in the same `src/` folder as `main.ipynb`.
4. Click **Run All** at the top of the notebook to execute all cells sequentially.

## Example Output

**First 5 Rows (`df.head()`):**

| Order_ID | Date | Product | Category | Quantity | Unit_Price | Region |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1001 | 2026-10-01 | Laptop | Electronics | 1.0 | 950.0 | North |
| 1002 | 2026-10-02 | Mouse | Accessories | 2.0 | 25.5 | South |
| 1003 | 2026-10-03 | Keyboard | Accessories | 1.0 | 75.0 | East |
| 1004 | 2026-10-04 | NaN | Electronics | 3.0 | 300.0 | West |
| 1005 | 2026-10-05 | Monitor | Electronics | NaN | 220.0 | North |

**Missing Values (`df.isnull().sum()`):**

```text
Missing values in each column:
Order_ID      0
Date          0
Product       2
Category      1
Quantity      1
Unit_Price    1
Region        1
dtype: int64
```