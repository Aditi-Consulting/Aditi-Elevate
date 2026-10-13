# Student Marks Assignment

This project contains a simple Python assignment for managing student marks.

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
