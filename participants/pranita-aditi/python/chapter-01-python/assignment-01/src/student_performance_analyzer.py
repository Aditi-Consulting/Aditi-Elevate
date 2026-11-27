students={}

#Calculate total marks and Average marks
def calculate_total(marks):
    return sum(marks)
def calculate_average(marks):
    return sum(marks)/len(marks)

#Assigning grades base on average
def assign_grade(average):
    if average>=90:
        return 'A'
    elif average>=80:
        return 'B'
    elif average>=70:
        return 'C' 
    elif average>=60:
        return 'D'
    else:
        return 'F'

#Display student performance report

def display_report(students):
    highest_average = 0
    top_student = ""

    print("\nStudent Performance Report")

    for student, marks in students.items():
        total = calculate_total(marks)
        average = calculate_average(marks)
        grade = assign_grade(average)

        print(f"Student: {student}, Total Marks: {total}, Average Marks: {average:.2f}, Grade: {grade}")

        # Find the student with highest average
        if average > highest_average:
            highest_average = average
            top_student = student

    # Display topper after the loop finishes
    print("\nTop Performing Student:", top_student)
    print("Highest Average Marks:", highest_average)


#user input for student names and marks
def main():
    try:
        n=int(input("Enter number of students: "))
        #Input Validation
        if n<=0:
            print("Number of students should be greater than 0")
            return
        #student details
        for i in range(n):
            name=input("Enter student name:").strip()
            #Input Validation
            if name == "":
                print("Student name cannot be empty")
                return

            #prevent duplicate student names
            if name in students:
                print("Student name already exists. Please enter a unique name.")
                return
            marks = []

            subjects = int(input("Enter number of subjects: "))

            # Number of subjects must be positive
            if subjects <= 0:
                raise ValueError("Enter at least one subject.")

            # Loop to enter subject marks
            for j in range(subjects):

                mark = float(input("Enter marks: "))

                # Marks must be between 0 and 100
                if mark < 0 or mark > 100:
                    raise ValueError(
                        "Marks must be between 0 and 100."
                    )

                marks.append(mark)

            # Store student name and marks in dictionary
            students[name] = marks

        # Calling function to display final report
        display_report(students)

    # Exception handling:
    # Handles invalid number input and invalid marks
    except ValueError as e:
        print("Invalid Input:", e)


# Program execution starts here
if __name__ == "__main__":
    main()