from Student_marks import Student

student = Student()
while True :
    name = input("Enter student name (or 'exit' to quit): ")
    if name.lower() == 'exit':
        break
    try:
        marks = int(input("Enter student marks: "))
        student.add_student(name, marks)
    except ValueError as e:
        print(e)
        continue
