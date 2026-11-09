# Coding Question 1 — Vowel Counter

## Participant

- Name: Nisarg Patel
- GitHub username: `NisargPatelK`

## Assessment

- Learning area: Python
- Chapter: Chapter 01
- Assessment: Coding Question 1 — Vowel Counter

## Objective

Write a Python program that accepts a string from the user and counts the number of vowels (`a`, `e`, `i`, `o`, `u`) present in it, ignoring case.

## Approach

`count_vowels(text)` converts the input to lowercase and counts characters that appear in `aeiou`. No third-party packages are used.

## Setup and run

- Python 3.8 or later; no third-party dependencies are required.
- From this assessment folder, run `python vowels.py`.

## Validation and results

| Input | Expected count |
| --- | --- |
| `Hello World` | `3` |
| `AEIOU` | `5` |
| `rhythm` | `0` |
| `Aditi Consulting` | `6` |

## Limitations

Only the five standard English vowels are counted; `y` is not treated as a vowel.
