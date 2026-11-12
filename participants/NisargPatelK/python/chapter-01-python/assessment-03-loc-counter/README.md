# Coding Question 2 — Line of Code (LOC) Counter

## Participant

- Name: Nisarg Patel
- GitHub username: `NisargPatelK`

## Assessment

- Learning area: Python
- Chapter: Chapter 01
- Assessment: Coding Question 2 — Line of Code (LOC) Counter

## Objective

Write a Python program that accepts a file path from the user and counts the total number of lines in that file.

## Approach

The program prompts for a path, reads the file with a context manager, and reports `len(file.readlines())`. It handles a missing file with a clear message.

## Setup and run

- Python 3.8 or later; no third-party dependencies are required.
- From this assessment folder, run `python LOC.py`.

## Validation and results

| Scenario | Expected output |
| --- | --- |
| Valid file with 112 lines | `Number of lines in the file: 112` |
| Empty file | `Number of lines in the file: 0` |
| Non-existent file | `File not found. Please check the file path and try again.` |

## Limitations

Blank lines are included in the total. Other I/O errors, such as permission errors, are not specifically handled.
