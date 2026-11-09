# Student Performance Analyzer

## Project Description

This Python application accepts student names and marks across four subjects.
It calculates each student's total marks and average, assigns a grade based on
the average, and identifies the highest-performing student.

The application validates that marks are whole numbers between 0 and 100 and
handles invalid input by displaying a message and prompting again.

## Project Structure

```text
Assignment1/
├── README.md
├── src/
│   └── student_performance_analyzer.py
└── tests/
    └── test_student_analyzer.py
```

## Requirements

- Python 3
- No third-party packages are required.

## How to Run the Application

1. Make sure Python 3 is installed.
2. Open a terminal in the `Assignment1` directory.
3. Run:

   ```bash
   python src/student_performance_analyzer.py
   ```

Enter a student name and marks for English, Maths, Environment, and Gujarati
when prompted. Press Enter without entering a name to finish and display the
highest-performing student.

## Run Unit Tests

From the `Assignment1` directory, run:

```bash
python -m unittest discover -s tests -v
```

The nine tests cover calculations, grade assignment, input validation, student
record creation, and highest-performing student identification.

## Python Concepts Used

- Dictionaries and data structures
- Reusable functions
- Loops and conditional statements
- User input
- Exception handling
- Type hints
- Unit testing with `unittest`
- Mocking with `unittest.mock`

## Conclusion

This project demonstrates Python fundamentals through a practical student
performance analyzer, including calculations, input validation, reusable
functions, and unit testing.