from Student_marks import Student

student = Student()
while True :
    name = input("Enter student name (or 'exit' to quit): ")
    if name.lower() == 'exit':
        break
    marks = int(input("Enter student marks: "))
    try:
        student.add_student(name, marks)
    except ValueError as e:
        print(e)
        continue
