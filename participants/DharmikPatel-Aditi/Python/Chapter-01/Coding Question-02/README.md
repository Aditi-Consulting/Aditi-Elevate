# String Vowel Counter

An implementation of a Python utility that analyzes a string and tallies the total occurrence of vowels.

---

### Problem Statement

> **Task:** Develop a Python function named `count_vowels(text)` that determines the number of vowels present in any provided string. The function must accurately detect both lowercase and uppercase variations (`a, e, i, o, u`, `A, E, I, O, U`).

---

### Highlights

- **Case-Insensitive Checking:** Accurately processes mixed-case inputs without requiring external libraries.
- **Defensive Design:** Safeguards against non-string inputs by returning `0`.
- **Pure Python:** Utilizes clean iteration (`for` loop) and conditional checks (`if` condition) for clarity and speed.

---

### Directory Layout

```text
assessment/
├── README.md
└── src/
    └── count_vowels.py   # Function implementation and execution test
```

---

### How to Import & Use

You can import and call `count_vowels` inside another Python module:

```python
from src.count_vowels import count_vowels

# Basic evaluation
phrase = "Cloud Computing & AI"
total = count_vowels(phrase)

print(f"Total vowels detected: {total}")  # Output: 8
```

---

### Running the Program

To run the script directly from your terminal/command prompt:

```powershell
python .\src\count_vowels.py
```

*(Alternatively, use `py .\src\count_vowels.py` on Windows)*

---

### Test Cases & Sample Output

| Test Input | Expected Result | Explanation |
| :--- | :---: | :--- |
| `"Orange"` | `3` | Matches `O`, `a`, `e` |
| `"FLY"` | `0` | No vowels present |
| `"AEIOU aeiou"` | `10` | Full set in both cases |
| `12345` | `0` | Non-string fallback |