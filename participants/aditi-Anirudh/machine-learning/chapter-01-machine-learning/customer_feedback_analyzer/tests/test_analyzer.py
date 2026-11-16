import tempfile
import unittest
from pathlib import Path

from src.analyzer import (
    analyze_feedback,
    clean_text,
    classify_sentiment,
    extract_product_mentions,
    run_analysis,
)


class AnalyzerTests(unittest.TestCase):
    def test_clean_text_removes_urls_and_normalizes_punctuation(self):
        self.assertEqual(clean_text("  GREAT! Visit https://example.com now. "), "great visit now")

    def test_sentiment_classification_includes_neutral_and_negation(self):
        self.assertEqual(classify_sentiment("the package arrived today"), ("neutral", 0))
        self.assertEqual(classify_sentiment("not good"), ("negative", -1))
        self.assertEqual(classify_sentiment("very good"), ("positive", 2))

    def test_extract_product_mentions_matches_whole_names_case_insensitively(self):
        self.assertEqual(
            extract_product_mentions("I love the aer buds case", ["AeroBuds", "Case"]),
            ["Case"],
        )
        self.assertEqual(extract_product_mentions("AeroBuds are great", ["AeroBuds"]), ["AeroBuds"])

    def test_analyze_feedback_and_write_outputs(self):
        rows = [
            {"feedback": "I love AeroBuds, excellent sound!", "product": "AeroBuds", "location": ""},
            {"feedback": "The setup was slow.", "product": "HomeHub", "location": ""},
            {"feedback": "It arrived today.", "product": "", "location": ""},
        ]
        analyzed = analyze_feedback(rows)
        self.assertEqual([row["sentiment"] for row in analyzed], ["positive", "negative", "neutral"])
        self.assertEqual(analyzed[0]["products"], "AeroBuds")

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "feedback.csv"
            source.write_text(
                "feedback,product\n"
                '"I love AeroBuds, excellent sound!",AeroBuds\n'
                '"The setup was slow.",HomeHub\n'
                '"It arrived today.",\n',
                encoding="utf-8",
            )
            output_dir = Path(temp_dir) / "results"
            counts = run_analysis(source, output_dir)
            self.assertEqual(counts, {"positive": 1, "negative": 1, "neutral": 1})
            self.assertTrue((output_dir / "analyzed_feedback.csv").is_file())
            self.assertTrue((output_dir / "sentiment_distribution.png").is_file())
            self.assertTrue((output_dir / "entity_distribution.png").is_file())

    def test_load_feedback_accepts_wrapped_text_and_location_columns(self):
        from src.analyzer import load_feedback

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "feedback.csv"
            source.write_text(
                '"Text, Sentiment, Location"\n'
                '"The service was great, Positive, North"\n',
                encoding="utf-8",
            )
            rows = load_feedback(source)
            self.assertEqual(
                rows,
                [
                    {
                        "feedback": "The service was great",
                        "product": "",
                        "location": "North",
                        "original_sentiment": "Positive",
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
