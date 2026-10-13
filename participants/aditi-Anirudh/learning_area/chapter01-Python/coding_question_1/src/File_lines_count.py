def files_lines_count(file_path):
    """
    Count the number of lines in a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The number of lines in the file.
    """
    try:
        with open(file_path, 'r') as file:
            return sum(1 for line in file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
print(files_lines_count("text1.txt"))