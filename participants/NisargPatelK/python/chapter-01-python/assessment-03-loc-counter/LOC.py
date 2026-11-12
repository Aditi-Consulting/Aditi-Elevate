try:
    with open(input("Enter the file name: "), "r") as file:
        print(f"Number of lines in the file: {len(file.readlines())} ")
except FileNotFoundError:
    print("File not found. Please check the file path and try again.")
