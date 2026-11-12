# Student Performance Analyser

## Participant

- Name: Nisarg Patel
- GitHub username: `NisargPatelK`

## Assessment

- Learning area: Python
- Chapter: Chapter 01
- Assessment: Student Performance Analyser

## Objective

Collect a student's marks in five subjects, calculate the total and average, assign a grade, and display the current highest-performing student.

## Setup and run

- Python 3.8 or later; no third-party dependencies are required.
- From this assessment folder, run `python assignment1.py`.

Enter marks from 0 to 100 when prompted. The program validates invalid and out-of-range values.

## Validation and results

Run the automated tests from this assessment folder:

```bash
python -m unittest discover -s tests -v
```

The tests cover mark validation, grade assignment, total and average calculation, and leaderboard storage.

## Limitations

The interactive program continues accepting student records until it is stopped manually.
