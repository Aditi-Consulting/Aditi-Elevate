# Student Performance Analyzer

A Python command-line application that collects student names and subject marks, validates user input, calculates totals and averages, assigns letter grades, and identifies the top-performing student.

---

## What It Does

* **Student Record Management:** Stores student names, subject scores, totals, averages, and grades using a list of dictionaries.
* **Score Calculation:** Computes total marks and average marks across subjects (`calculate_summary`).
* **Automated Grading:** Assigns letter grades (`A`, `B`, `C`, `D`, `F`) based on the student's average score (`assign_grades`).
* **Top Performer Identification:** Evaluates all entered records and highlights the student with the highest average (`get_top_scorer`).
* **Input Validation:** Ensures student names are non-empty and marks are valid numbers strictly between `0` and `100` (`validate_marks`, `get_valid_mark`), handling invalid text or out-of-range values gracefully without crashing.
* **Unit Testing:** Includes automated unit tests using Python's built-in `unittest` framework to verify calculations, grading boundaries, top-scorer selection, and input validation.

---

## Project Structure

```text
Assignment/
├── src/
│   └── main.py          # Main application logic and CLI prompts
├── tests/
│   └── test_main.py     # Unit tests
└── README.md            # Project documentation
```

---

## Prerequisites

* Python 3.10 or higher

---

## How to Execute

### 1. Navigate to the Project Directory
Open your terminal and move into the `Assignment` folder:

```powershell
cd "Aditi-Elevate\participants\DharmikPatel-Aditi\Python\Chapter-01\Assignment"
```

### 2. Run the Application
Execute the main script:

```powershell
python src/main.py
```

**Usage Flow:**
1. Enter a student's name when prompted.
2. Enter marks (`0–100`) for each of the 3 subjects.
3. Repeat for additional students, or type `done` when asked for a student name to generate the final performance report and see the top performer.

### 3. Run the Unit Tests
Run the `unittest` discovery tool from the `Assignment` folder to execute `tests/test_main.py`:

```powershell
python -m unittest discover -s tests -v
```

---

## Example Output

```text
Student Management System

Enter student name (or type 'done' to finish): Dharmik
Enter marks for subject 1 (0-100): 75
Enter marks for subject 2 (0-100): 80
Enter marks for subject 3 (0-100): 80

Enter student name (or type 'done' to finish): Swara
Enter marks for subject 1 (0-100): 85
Enter marks for subject 2 (0-100): 88
Enter marks for subject 3 (0-100): 87

Enter student name (or type 'done' to finish): done

--- Performance Report ---
Student: Dharmik, Total Marks: 235.0, Average Marks: 78.33, Grade: C
Student: Swara, Total Marks: 260.0, Average Marks: 86.67, Grade: B

Top Performer: Swara (Average: 86.67, Grade: B)
```