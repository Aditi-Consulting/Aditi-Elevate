class Student:
    student_data = {}

    def add_student(self, name, marks):
        '''
        Add a student with their marks to the class-level dictionary.
        '''
        if not isinstance(marks, int):
            raise ValueError("Marks should be an integer")
        if marks < 0 or marks > 100:
            raise ValueError("Marks should be between 0 and 100")

        Student.student_data[name] = marks

    def _get_mark(self, name):
        '''
        Helper method to retrieve the marks for a given student name.
        '''
        return Student.student_data.get(name)

    def calculate_total_and_average(self):
        '''
        Calculate the total and average marks of all students.
        '''
        if not Student.student_data:
            return 0, 0

        total = sum(Student.student_data[name] for name in Student.student_data)
        average = total / len(Student.student_data)
        return total, average

    def get_highest_mark(self):
        '''
        Get the student with the highest mark.
        '''
        if not Student.student_data:
            return None, None

        highest_student = None
        highest_mark = None

        for name, marks in Student.student_data.items():
            if highest_mark is None or marks > highest_mark:
                highest_mark = marks
                highest_student = name

        return highest_student, highest_mark

    def assign_grade(self):
        '''
        Assign grades to students based on their marks.
        '''
        _, avg = self.calculate_total_and_average()

        for name, marks in list(Student.student_data.items()):
            grade = 'P' if marks > avg else 'F'
            Student.student_data[name] = {"marks": marks, "grade": grade}

