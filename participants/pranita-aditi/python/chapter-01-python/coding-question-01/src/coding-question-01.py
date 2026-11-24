from pathlib import Path

# Resolve test.txt relative to this script, not the current working directory.
INPUT_FILE = Path(__file__).resolve().parent / "test.txt"

try:
    with open(INPUT_FILE, "r") as file:
        lines = file.readlines()
        print(len(lines))

except FileNotFoundError:
    print("File not found")
