# Customer Feedback Analyzer

A Jupyter Notebook project that loads customer feedback from a CSV file, cleans and normalizes text using NLP preprocessing, classifies sentiment using Machine Learning (`TF-IDF` + `Multinomial Naive Bayes`), extracts city entities, and visualizes sentiment insights.

## What It Does

* **Data Loading:** Reads `customer_feedback.csv` into a Pandas `DataFrame` (`pd.read_csv()`).
* **Text Cleaning & Normalization:** Lowercases text, strips punctuation/special characters using regular expressions, and removes extra whitespace (`cleaned_feedback`).
* **Sentiment Classification (ML & NLP):** Vectorizes normalized text with `TfidfVectorizer` (removing English stopwords) and trains a `MultinomialNB` classifier to label reviews as **Positive**, **Neutral**, or **Negative**.
* **City Entity Extraction:** Identifies and extracts Indian city names (`Mumbai`, `Delhi`, `Bangalore`, `Pune`, `Chennai`, `Hyderabad`, `Goa`, `Kolkata`, `Ahmedabad`) mentioned in each review.
* **Distribution & Visualization:** Computes sentiment category counts and percentages, and generates two bar charts—overall sentiment distribution and sentiment breakdown by city.
* **Assumptions & Limitations:** Documents dataset assumptions and model constraints inside the notebook.

## Project Structure

```text
Assignment_Customer_Feedback_Analyzer/
├── src/
│   ├── main.ipynb               # Jupyter Notebook containing the NLP & ML analysis
│   └── customer_feedback.csv    # Dataset containing 60 customer feedback records
└── README.md                    # Project documentation
```

## Prerequisites

* Python 3.10 or higher
* `pandas`, `scikit-learn`, `matplotlib`, and `ipykernel` installed:
  ```bash
  pip install pandas scikit-learn matplotlib ipykernel
  ```

## How to Execute

1. Open `src/main.ipynb` in VS Code (or Jupyter Notebook).
2. Click **Select Kernel** in the top-right corner and choose your Python environment.
3. Ensure `customer_feedback.csv` is located in the same `src/` folder as `main.ipynb`.
4. Click **Run All** at the top of the notebook to execute all cells sequentially.

## Example Output

**Sample Classified Reviews & Extracted Cities:**

| feedback_id | customer_name | city | sentiment |
| :--- | :--- | :--- | :--- |
| 1 | Customer_1 | Mumbai | Neutral |
| 2 | Customer_2 | Pune | Neutral |
| 3 | Customer_3 | Delhi | Positive |
| 4 | Customer_4 | Goa | Neutral |
| 5 | Customer_5 | Delhi | Positive |

**Sentiment Distribution (`df["sentiment"].value_counts()`):**

```text
Sentiment Counts:
Neutral     24
Positive    18
Negative    18
Name: sentiment, dtype: int64
```