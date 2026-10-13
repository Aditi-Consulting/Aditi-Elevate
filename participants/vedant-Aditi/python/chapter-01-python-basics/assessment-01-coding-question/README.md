# Week 1 Python Coding Question

## Participant

- Name: Vedant
- GitHub username: vedant-Aditi

## Assessment

- Learning area: Python
- Chapter: Chapter 01 - Python Basics
- Assessment: Assessment 01 - Coding Question

## Objective

Write a Python program that:

- Reads a text file.
- Counts the number of lines in the file.
- Handles the case where the file does not exist.

## Approach

Opens the specified file in read mode and counts each line using a generator expression. Uses a context manager to close the file automatically and catches FileNotFoundError.

## Setup

Python is required. No third-party packages are required for this assessment.

## How to Run

From the assessment directory, run python src/main.py, then enter sample.txt when prompted.

## Validation and Results

- When provided with `sample.txt`, the program prints `Total lines : 4`.
- When provided with a nonexistent filename, the program prints an error message indicating that the file does not exist or is not accessible.## Validation and Results



## References and Limitations

Uses Python's standard library; no third-party packages are required.
 


