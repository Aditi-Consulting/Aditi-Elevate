# Line Counter (`main.py`)

A lightweight Python script that opens a text file, counts the total number of lines, and handles missing file errors gracefully.

---

## Overview

The program implements a dedicated function, `count_lines_in_file`, designed to read an input file and report its line count while preventing unexpected program termination if the target file cannot be found.

---

## Code Implementation

```python
def count_lines_in_file(filename) -> None:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            line_count = sum(1 for line in file)
        print(f"The file '{filename}' contains {line_count} line(s).")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

filename = "sample.txt"
count_lines_in_file(filename)
```

---

## Key Features

- **Memory Efficiency**: Utilizes a generator expression (`sum(1 for line in file)`) to process the file line by line without loading the entire content into memory.
- **Exception Handling**: Catches `FileNotFoundError` specifically to output an informative message instead of crashing.
- **Standard Encoding**: Sets `encoding="utf-8"` explicitly for consistent behavior across different operating systems.

---

## Project Structure

Ensure both the script and the target text file reside in the same directory:

```text
assessment/
├── main.py
└── sample.txt
```

---

## Usage Instructions

1. Open a terminal or shell prompt.
2. Navigate to the directory containing both `main.py` and `sample.txt`:
   ```bash
   cd path/to/your/folder
   ```
3. Run the script using Python:
   ```bash
   python main.py
   ```

---

## Output Examples

### Case 1: File Exists
```text
The file 'sample.txt' contains 3 line(s).
```

### Case 2: File Not Found
```text
Error: The file 'sample.txt' does not exist.
```