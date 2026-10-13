class Student:
    student_data = {}

    def __init__(self):
        self.students = {}
        Student.student_data = self.students

    def add_student(self, name, marks):
        '''
        Add a student with their marks to the students dictionary.
        '''
        if not isinstance(marks, int):
            raise ValueError("Marks should be an integer")
        if marks < 0 or marks > 100:
            raise ValueError("Marks should be between 0 and 100")

        self.students[name] = marks
        Student.student_data = self.students

    def _get_mark(self, name):
        '''
        Helper method to retrieve the marks for a given student name.
        '''
        value = self.students.get(name)
        if isinstance(value, dict):
            return value.get("marks", 0)
        return value

    def calculate_total_and_average(self):
        '''
        Calculate the total and average marks of all students.
        '''
        if not self.students:
            return 0, 0

        total = sum(self._get_mark(name) for name in self.students)
        average = total / len(self.students)
        return total, average

    def get_highest_mark(self):
        '''
        Get the student with the highest mark.
        '''
        if not self.students:
            return None, None

        highest_student = None
        highest_mark = None

        for name in self.students:
            current_mark = self._get_mark(name)
            if highest_mark is None or current_mark > highest_mark:
                highest_mark = current_mark
                highest_student = name

        return highest_student, highest_mark

    def assign_grade(self):
        '''
        Assign grades to students based on their marks.
        '''
        total , avg = self.calculate_total_and_average()

        for name in list(self.students):
            marks = self._get_mark(name)
            grade = 'P' if marks > avg else 'F'
            current_value = self.students[name]

            if isinstance(current_value, dict):
                current_value["marks"] = marks
                current_value["grade"] = grade
            else:
                self.students[name] = {"marks": marks, "grade": grade}

        Student.student_data = self.students

