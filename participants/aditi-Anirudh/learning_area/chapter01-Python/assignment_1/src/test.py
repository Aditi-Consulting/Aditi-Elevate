import unittest
from Student_marks import Student

class TestStudent(unittest.TestCase):
    def setUp(self):
        '''
        Set up a new Student instance before each test.
        '''
        self.student = Student()

    def test_add_student(self):
        '''
        Test adding a student with valid marks.
        '''
        self.student.add_student("Alice", 85)
        self.assertIn("Alice", self.student.students)
        self.assertEqual(self.student.students["Alice"], 85)

    def test_add_student_invalid_marks(self):
        '''
        Test adding a student with invalid marks.
        '''
        with self.assertRaises(ValueError):
            self.student.add_student("Bob", -5)
        with self.assertRaises(ValueError):
            self.student.add_student("Charlie", 105)
    def test_calculate_total_and_average(self):
        '''
        Test calculating total and average marks.
        '''
        self.student.add_student("Alice", 85)
        self.student.add_student("Bob", 90)
        total, avg = self.student.calculate_total_and_average()
        self.assertEqual(total, 175)
        self.assertEqual(avg, 87.5)
    def test_get_highest_mark(self):
        '''
        Test getting the student with the highest mark.
        '''
        self.student.add_student("Alice", 85)
        self.student.add_student("Bob", 90)
        highest_student, highest_mark = self.student.get_highest_mark()
        self.assertEqual(highest_student, "Bob")
        self.assertEqual(highest_mark, 90)
    def test_assign_grade(self):
        '''
        Test assigning grades to students.
        '''
        self.student.add_student("Alice", 85)
        self.student.add_student("Bob", 90)
        self.student.assign_grade()
        self.assertEqual(self.student.students["Alice"]["grade"], 'F')
        self.assertEqual(self.student.students["Bob"]["grade"], 'P')
    