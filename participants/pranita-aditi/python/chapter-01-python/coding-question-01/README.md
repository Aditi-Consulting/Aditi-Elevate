
# Python File Line Counter

## Project Description

This Python program reads a text file named `test.txt`, counts the total number of lines, and handles the case where the file does not exist using exception handling.

## Project Structure

```text
coding-question-01/
│
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
2. Open the terminal in the `src` directory.
3. Run the following command:

```bash
python coding-question-01.py
```

## Expected Output

```text
4
```

The output is `4` because `test.txt` contains four lines.

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
