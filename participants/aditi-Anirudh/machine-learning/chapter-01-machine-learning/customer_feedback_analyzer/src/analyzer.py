"""Analyze customer feedback from a CSV file."""

from __future__ import annotations

import argparse
import csv
import html
import io
import re
import unicodedata
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SENTIMENTS = ("positive", "negative", "neutral")
POSITIVE_WORDS = {
    "amazing",
    "awesome",
    "best",
    "excellent",
    "fantastic",
    "friendly",
    "good",
    "great",
    "love",
    "loved",
    "perfect",
    "quick",
    "recommend",
    "reliable",
    "smooth",
}
NEGATIVE_WORDS = {
    "awful",
    "bad",
    "broken",
    "disappointed",
    "hate",
    "horrible",
    "late",
    "poor",
    "problem",
    "refund",
    "slow",
    "terrible",
    "unhelpful",
    "worst",
}
NEGATIONS = {"cannot", "don't", "isn't", "never", "no", "not", "wasn't", "won't"}
INTENSIFIERS = {"extremely", "really", "so", "very"}
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
TOKEN_PATTERN = re.compile(r"\b[\w']+\b", re.UNICODE)


def clean_text(text: str) -> str:
    """Normalize Unicode, remove URLs and punctuation, and lowercase text."""
    normalized = unicodedata.normalize("NFKC", html.unescape(text))
    normalized = URL_PATTERN.sub(" ", normalized)
    normalized = re.sub(r"[^\w\s']", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.lower().split())


def classify_sentiment(cleaned_text: str) -> tuple[str, int]:
    """Classify text with a small lexicon and nearby negation handling."""
    tokens = TOKEN_PATTERN.findall(cleaned_text)
    score = 0
    for index, token in enumerate(tokens):
        direction = 1 if token in POSITIVE_WORDS else -1 if token in NEGATIVE_WORDS else 0
        if direction == 0:
            continue

        context = tokens[max(0, index - 3) : index]
        multiplier = 2 if any(word in INTENSIFIERS for word in context) else 1
        if any(word in NEGATIONS for word in context):
            direction *= -1
        score += direction * multiplier

    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return sentiment, score


def extract_product_mentions(text: str, product_catalog: list[str]) -> list[str]:
    """Find catalog product names mentioned in text, preserving catalog spelling."""
    mentions = []
    for product in product_catalog:
        product = product.strip()
        if product and re.search(rf"(?<!\w){re.escape(product)}(?!\w)", text, re.IGNORECASE):
            mentions.append(product)
    return mentions


def load_feedback(csv_path: Path) -> list[dict[str, str]]:
    """Read standard CSV files and records wrapped as a single quoted CSV field."""
    contents = csv_path.read_text(encoding="utf-8-sig")
    records = list(csv.reader(io.StringIO(contents)))
    if records and len(records[0]) == 1 and "," in records[0][0]:
        records = [
            next(csv.reader([line[1:-1]], skipinitialspace=True))
            if line.startswith('"') and line.endswith('"')
            else next(csv.reader([line], skipinitialspace=True))
            for line in contents.splitlines()
        ]

    if not records:
        raise ValueError("CSV file is empty.")
    headers = [header.strip().casefold() for header in records[0]]
    feedback_column = next(
        (name for name in ("feedback", "text", "review") if name in headers), None
    )
    if feedback_column is None:
        raise ValueError("CSV file must contain a 'feedback', 'text', or 'review' column.")

    rows = []
    for values in records[1:]:
        row = dict(zip(headers, values))
        rows.append(
            {
                "feedback": row.get(feedback_column, ""),
                "product": row.get("product", ""),
                "location": row.get("location", ""),
                "original_sentiment": row.get("sentiment", ""),
            }
        )
    return rows


def analyze_feedback(rows: list[dict[str, str]]) -> list[dict[str, str | int]]:
    """Clean and classify each row, and extract product and location entities."""
    catalog = list(dict.fromkeys(row["product"].strip() for row in rows if row["product"].strip()))
    analyzed = []
    for row in rows:
        feedback = row["feedback"]
        cleaned = clean_text(feedback)
        sentiment, score = classify_sentiment(cleaned)
        mentions = extract_product_mentions(feedback, catalog)
        analyzed.append(
            {
                "feedback": feedback,
                "cleaned_feedback": cleaned,
                "sentiment": sentiment,
                "sentiment_score": score,
                "products": "; ".join(mentions),
                "location": row.get("location", "").strip(),
                "original_sentiment": row.get("original_sentiment", "").strip(),
            }
        )
    return analyzed


def write_results(rows: list[dict[str, str | int]], output_path: Path) -> None:
    """Write analyzed feedback as a CSV file."""
    fieldnames = (
        "feedback",
        "cleaned_feedback",
        "sentiment",
        "sentiment_score",
        "original_sentiment",
        "products",
        "location",
    )
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_visualizations(rows: list[dict[str, str | int]], output_dir: Path) -> None:
    """Save sentiment distribution and entity distribution charts."""
    sentiment_counts = Counter(str(row["sentiment"]) for row in rows)
    fig, axis = plt.subplots(figsize=(7, 4))
    axis.bar(SENTIMENTS, [sentiment_counts[label] for label in SENTIMENTS], color=("#4C9F70", "#D95D5D", "#8A8F98"))
    axis.set(title="Customer Feedback Sentiment", xlabel="Sentiment", ylabel="Number of responses")
    fig.tight_layout()
    fig.savefig(output_dir / "sentiment_distribution.png", dpi=150)
    plt.close(fig)

    location_counts = Counter(str(row["location"]) for row in rows if row["location"])
    product_counts: Counter[str] = Counter()
    for row in rows:
        product_counts.update(product for product in str(row["products"]).split("; ") if product)
    entity_counts = location_counts or product_counts
    entity_label = "Location" if location_counts else "Product"
    top_entities = entity_counts.most_common(10)
    fig, axis = plt.subplots(figsize=(8, 4))
    if top_entities:
        names, counts = zip(*top_entities)
        axis.bar(names, counts, color="#4C78A8")
        axis.tick_params(axis="x", labelrotation=30)
    else:
        axis.text(0.5, 0.5, "No product or location entities found", ha="center", va="center")
        axis.set_xticks([])
    axis.set(
        title=f"Most Frequent {entity_label}s",
        xlabel=entity_label,
        ylabel="Number of feedback entries",
    )
    fig.tight_layout()
    fig.savefig(output_dir / "entity_distribution.png", dpi=150)
    plt.close(fig)


def run_analysis(input_path: Path, output_dir: Path) -> dict[str, int]:
    """Run the full analysis and return category counts."""
    rows = analyze_feedback(load_feedback(input_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_results(rows, output_dir / "analyzed_feedback.csv")
    create_visualizations(rows, output_dir)
    counts = Counter(str(row["sentiment"]) for row in rows)
    return {sentiment: counts[sentiment] for sentiment in SENTIMENTS}


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze customer feedback in a CSV file.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sentiment-analysis.csv"),
        help="Input CSV containing a feedback or text column.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    counts = run_analysis(args.input, args.output_dir)
    print("Sentiment distribution:")
    for sentiment, count in counts.items():
        print(f"  {sentiment.capitalize()}: {count}")
    print(f"Results and visualizations saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
