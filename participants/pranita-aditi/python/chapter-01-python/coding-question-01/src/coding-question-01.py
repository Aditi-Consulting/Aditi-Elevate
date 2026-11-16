try:
    with open("test.txt", 'r') as file:
        lines=file.readlines()
        print(len(lines))
 
except FileNotFoundError:
    print("File not found")