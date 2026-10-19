# Assessment 02 - Count Vowels

## Participant

- Name: Vedant
- GitHub username: vedant-Aditi

## Assessment

- Learning area: Python
- Chapter: Chapter 01 - Python Basics
- Assessment: Assessment 02 - Count Vowels

## Objective

Write a Python function named `count_vowels(text)` that returns the number of vowels in a string. The function should count `a`, `e`, `i`, `o`, and `u` as vowels regardless of uppercase or lowercase letters.

## Approach

The solution keeps a string of lowercase vowels and loops through each character in the input text. Each character is converted to lowercase before checking whether it is a vowel. The function returns the final count as an integer.

## Setup

Python is required. No third-party packages are required for this assessment.

## How to Run

From this assessment directory, run the tests with:

```bash
python tests/test_count_vowels.py
```

To run the sample program:

```bash
python src/main.py
```

## Validation and Results

The test script checks:

- lowercase vowels
- uppercase vowels
- mixed-case text
- a string without vowels
- an empty string
- a string containing spaces, digits, and punctuation

Expected result:

```text
All tests passed.
```

## References and Limitations

Uses Python's standard library only. The assignment treats `a`, `e`, `i`, `o`, and `u` as vowels.
