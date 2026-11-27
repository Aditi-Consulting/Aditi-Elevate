
# Python File Line Counter

## Assigned Question

> **Coding Question**
>
> Write a Python program that:
>
> - Reads a text file.
> - Counts the number of lines.
> - Handles the case where the file does not exist.

### Requirements derived from the question

| Item | Value |
| --- | --- |
| Input | A text file. This submission supplies `src/test.txt` (2 lines). |
| Output | The number of lines in the file, printed to stdout. |
| Constraint | A missing file must be handled, not crash. This program prints `File not found`. |

## Project Description

This Python program reads a text file named `test.txt`, counts the total number of lines, and handles the case where the file does not exist using exception handling.

## Project Structure

```text
coding-question-01/
│
├── README.md
└── src/
    ├── coding-question-01.py
    └── test.txt
```

## Sample Input (`test.txt`)

```text
AI/ML stands for Artificial Intelligence/Machine Learning.
Deep Learning is subset of AI/ML.
```

## How to Run the Program

1. Make sure Python is installed on your system.
2. Run from the chapter directory (`chapter-01-python`) — or any directory, since the script locates `test.txt` relative to itself:

```bash
python coding-question-01/src/coding-question-01.py
```

## Expected Output

```text
2
```

The output is `2` because `test.txt` contains two lines.

## Exception Handling

If the `test.txt` file is missing, the program displays:

```text
File not found
```

This is handled using the `FileNotFoundError` exception.

## Python Concepts Used

- File Handling
- `open()` function
- `readlines()` method
- `len()` function
- `with` statement
- `try-except` block
- `FileNotFoundError`

## Conclusion

This program demonstrates how to read a text file, count its lines, and handle file-related errors using Python exception handling.
