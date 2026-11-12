def count_lines_in_file(filename) -> None:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            line_count = sum(1 for line in file)
        print(f"The file '{filename}' contains {line_count} line(s).")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
filename = "sample.txt"
count_lines_in_file(filename)