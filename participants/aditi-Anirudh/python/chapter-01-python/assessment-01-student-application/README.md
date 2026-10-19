# Student Performance Analyzer

A command-line Python application that collects student names, user-defined subject names, and marks. It reports each student's mark and grade by subject, total, overall average and grade, plus the highest overall average. Every student is entered with one mark per subject.

## Requirements

- Python 3.8 or newer
- No third-party packages

## Run the application

From the project root, run:

```bash
py src/main.py
```

The application asks for the number of students and subjects, then asks you to name each subject. Enter each student's name and a mark for every subject. Counts must be positive whole numbers; student and subject names must be non-empty and unique; marks must be numeric values from 0 through 100. Invalid entries are reported and requested again.

## Run the tests

From the project root, run:

```bash
py -m unittest discover -s src -v
```

## Grading rule

The application uses relative P/F grades. A student's overall grade is P when their average is at least the class average; a subject grade is P when their mark is at least the class average for that subject. No fixed grade bands were provided; confirm whether this relative P/F rule is the intended grading policy.

The calculation helpers return 0 for an empty mark list. Each student's average is calculated from that student's entered marks; highest-average ties require equal calculated averages.
