
# Student Performance Analyzer

---

## Project Description

This Python application accepts student names and marks, calculates total and average marks, assigns grades, and displays the highest-performing student.

It also validates marks between 0 and 100 and handles invalid input using exception handling.

## Project Structure

```text
assignment-01/
│
├── src/
│   └── student_performance.py
│
├── tests/
│   ├── __init__.py
│   └── test_student_performance.py
│
└── README.md
```

## How to Run the Program

1. Make sure Python is installed.
2. Open the terminal in the project directory.
3. Run the following command:

```bash
python src/student_performance.py
```

## How to Run Unit Tests

Run the following command:

```bash
python -m unittest discover -s tests -v
```

## Input Validation

- Student names cannot be empty or duplicated.
- Number of students and subjects must be positive.
- Marks must be between 0 and 100.
- Invalid input is handled using `try-except`.

## Python Concepts Used

- Variables and Data Structures
- Lists and Dictionaries
- Loops and Conditional Statements
- Reusable Functions
- Input Validation
- Exception Handling
- Unit Testing (`unittest`)

## Conclusion

This project demonstrates how Python can be used to manage student records, calculate academic performance, assign grades, and identify the highest-performing student using reusable functions and exception handling.

---

**Developed using Python**
