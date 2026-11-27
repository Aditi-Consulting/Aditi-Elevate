input_file = input("Enter the path of the file : ")

try:
    with open(input_file,"r") as file:
        lines=file.readlines()
    num_lines=len(lines)
    print("Number of lines in the file are :",num_lines)
except FileNotFoundError as e :
    print(f"Error found as : {e}")  
finally: 
    print("Done ")