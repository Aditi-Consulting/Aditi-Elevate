def count_file_lines(filename):
    try:
        with open(filename, "r") as file:
            line_count = sum(1 for line in file)

        print(f"Total lines : {line_count}")

    except FileNotFoundError:
        print("Error: The specified file does not exist or is not accessible")


if __name__ == "__main__":
    filename = input("Enter the filename: ")
    count_file_lines(filename)