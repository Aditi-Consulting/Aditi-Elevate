# Assessment 01 – Count Lines in a Text File

## Participant
Name: <Medisetti Jayaramakrishna>
GitHub username: jayaram-aditi

## Assessment
Learning area: python
Chapter: 01 – Python
Assessment: 01 – Count lines in a text file

## Objective
Write a Python program that reads a text file, counts the number of lines,
and handles the case where the file does not exist.

## Approach
The program asks the user for a file path and opens it with `with open()`.
It reads all lines with `readlines()` and counts them with `len()`.
A `try/except FileNotFoundError` block prints an error message if the file
does not exist, so the program does not crash.

## Setup
- Python version: <your version, run `python --version`>
- Dependencies: None (standard library only)
- Configuration/environment variables: None

## How to run
From the assessment folder:

    python src/count_lines_program.py

When prompted, enter `src/text_sample.txt` to test an existing file,
or any wrong name (for example `abc.txt`) to test the missing-file case.

## Validation and results
- Existing file (`src/text_sample.txt`): prints the number of lines in the file.
- Missing file (`abc.txt`): prints "Error: the file does not exist."

## References and limitations
- Python docs: `open()` and `FileNotFoundError`.
- Only the missing-file error is handled.