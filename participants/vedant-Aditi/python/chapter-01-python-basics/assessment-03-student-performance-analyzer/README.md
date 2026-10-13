# Assessment 03 - Student Performance Analyzer

## Participant

- Name: Vedant
- GitHub username: vedant-Aditi

## Assessment

- Learning area: Python
- Chapter: Chapter 01 - Python Basics
- Assessment: Assessment 03 - Student Performance Analyzer

## Objective

Create a Python application that accepts student names and marks, calculates each student's total and average marks, assigns grades, identifies the top-performing student, validates input, handles errors, and generates a readable performance report.

## Directory Structure

```text
assessment-03-student-performance-analyzer/
├── README.md
├── requirements.txt
├── src/
│   └── main.py
├── notebooks/
│   └── .gitkeep
└── tests/
    └── test_student_performance.py
```

## Approach

The application stores each student as a dictionary with a name and a list of marks. Separate reusable functions handle total calculation, average calculation, grade assignment, mark validation, top-student selection, and report generation. The interactive `main()` function handles user input and re-prompts for invalid values.

## Setup

Python 3 is required. No third-party packages are required for this assessment.

## Student Data Entry

The program prompts for:

- the number of students
- each student's name
- three marks for each student

Assumption: each student has exactly three subject marks.

## Grading Scale

- A: average >= 90
- B: average >= 80 and < 90
- C: average >= 70 and < 80
- D: average >= 60 and < 70
- F: average < 60

Decimal averages are handled using the same boundaries. For example, 89.5 receives B and 79.9 receives C.

## Input Validation and Error Handling

- The student count must be a positive integer.
- Student names cannot be empty.
- Marks must be numeric values between 0 and 100, inclusive.
- Invalid input is rejected with an error message, and the program asks again instead of crashing.
- Empty mark lists return an average of `0`.
- Empty student lists return no top student and generate the message `No student records available.`
- If multiple students tie for the highest average, the first student entered is selected as the top student.

## How to Run

From the repository root, run:

```bash
cd participants/vedant-Aditi/python/chapter-01-python-basics/assessment-03-student-performance-analyzer
python src/main.py
```

## How to Run Tests

From the repository root, run:

```bash
cd participants/vedant-Aditi/python/chapter-01-python-basics/assessment-03-student-performance-analyzer
python -m unittest discover -s tests -v
```

## Validation and Results

The test suite checks:

- total calculation
- average calculation, including decimal averages
- grade boundaries
- invalid marks
- highest-performing student selection
- tie handling
- empty input behavior
- report contents

Expected result:

```text
OK
```

## References and Limitations

Uses Python's standard library only. The application assumes three subject marks per student.
