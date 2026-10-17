# Student Marks Assignment

This project contains a simple Python assignment for managing student marks.
# Question
Practical Assignment 
Assignment: Student Performance Analyzer 
Develop a Python application that accepts student names and marks, then produces a performance report. 
The application must: 
Store student data using appropriate Python data structures. 
Calculate total marks and average marks. 
Assign grades based on the average. 
Display the highest-performing student. 
Validate that marks are between 0 and 100. 
Handle invalid user input. 
Include at least three reusable functions. 
Include at least five unit tests. 
Include a README file explaining how to execute the application. 




## Files

- `src/Student_marks.py` - Student class with methods to add students, calculate totals/averages, find the highest mark, and assign grades.
- `src/test.py` - Unit tests for the Student class.
- `src/main.py` - Simple command-line runner for entering student names and marks.

## Run the tests

From the project root:

```bash
cd src
py -m unittest -v
```

## Run the program

```bash
cd src
py main.py
```

## Notes

- Marks must be between 0 and 100.
- Invalid marks raise a `ValueError`.
