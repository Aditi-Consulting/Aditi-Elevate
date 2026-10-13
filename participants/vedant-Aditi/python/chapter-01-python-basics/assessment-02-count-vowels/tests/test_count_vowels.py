import os
import sys


CURRENT_DIR = os.path.dirname(__file__)
ASSESSMENT_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(ASSESSMENT_DIR, "src")
sys.path.insert(0, SRC_DIR)

from main import count_vowels


def test_lowercase_vowels():
    assert count_vowels("aeiou") == 5


def test_uppercase_vowels():
    assert count_vowels("AEIOU") == 5


def test_mixed_case_text():
    assert count_vowels("Hello Universe") == 6


def test_no_vowels():
    assert count_vowels("rhythm") == 0


def test_empty_string():
    assert count_vowels("") == 0


def test_spaces_digits_and_punctuation():
    assert count_vowels("A1! e2? I3. o4, U5") == 5


if __name__ == "__main__":
    test_lowercase_vowels()
    test_uppercase_vowels()
    test_mixed_case_text()
    test_no_vowels()
    test_empty_string()
    test_spaces_digits_and_punctuation()
    print("All tests passed.")
