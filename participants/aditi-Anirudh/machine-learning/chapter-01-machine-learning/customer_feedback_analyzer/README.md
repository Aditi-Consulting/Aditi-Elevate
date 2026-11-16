# Customer Feedback Analyzer

A command-line Python application that cleans customer feedback, assigns a positive, negative, or neutral label, extracts available product or location entities, prints the sentiment distribution, and saves an analyzed CSV plus two charts.

## Setup

From this directory, create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
python analyzer.py
```

By default, the application reads `data/sentiment-analysis.csv` and writes `output/analyzed_feedback.csv`, `output/sentiment_distribution.png`, and `output/entity_distribution.png`. Choose different paths with:

```powershell
python analyzer.py --input path\to\feedback.csv --output-dir path\to\results
```

The input CSV must have a `feedback`, `text`, or `review` column. A `product` column is optional; its values are used to find product names in the feedback. If a `location` column is present, location frequencies are shown in the entity chart. If a `sentiment` column is present, its original labels are preserved in the results for comparison; the analyzer still calculates its own sentiment labels. The reader also supports the updated dataset's format, where each whole CSV record is wrapped in quotes.

## Implementation

- **Loading and cleaning:** Reads UTF-8 CSV data, normalizes Unicode and HTML entities, removes URLs and punctuation, and lowercases/collapses whitespace.
- **NLP preprocessing:** Tokenizes normalized text and applies a small lexicon-based sentiment scorer, including limited nearby negation and intensifier handling.
- **Sentiment:** Positive and negative lexicon hits add to or subtract from a score; zero is neutral. The application reports counts for all three classes, including classes with no examples.
- **Entity extraction:** Finds product names from the CSV product catalog in the original feedback text, and uses supplied location values when present.
- **Visualizations:** Saves a sentiment distribution bar chart and a product or location frequency chart.

## Assumptions and limitations

- Sentiment is a transparent rule-based baseline, not a trained model. The small English vocabulary may misread sarcasm, domain-specific language, mixed opinions, or words absent from its lexicon.
- Negation is approximated using the previous three tokens; complex grammar and scope are not understood.
- Product extraction only recognizes values present in the optional `product` column. It will miss unseen products and does not resolve ambiguous names. Location analysis counts the supplied `location` values; it does not infer a location from free text.
- Text is expected to be mostly English. Results reflect the dataset's sampling and annotation quality.
- The tool does not infer sentiment confidence or account for differences in feedback length.

## Tests

```powershell
python -m unittest discover -s tests -v
```
