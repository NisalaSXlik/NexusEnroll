# Minimal unit tests for key business logic and design patterns
import unittest
from core.catalogue import ConcreteCourseFactory, CourseCatalogue
from core.course import Course
from enrolment.enrolment_service import EnrolmentService
from enrolment.validation_strategies import CapacityValidation, PrerequisiteValidation, ScheduleConflictValidation
from faculty.grades import Grade, DraftState, PendingState, SubmittedState

class TestEnrolmentService(unittest.TestCase):
    def setUp(self):
        self.factory = ConcreteCourseFactory()
        self.course = self.factory.create_course("Lecture", course_id="T101", name="Test Course", instructor="Dr. Test", capacity=1)
        self.student = type("Student", (), {"name": "Test", "completed_courses": [], "enrolled_courses": []})()
        self.service = EnrolmentService([CapacityValidation()])

    def test_enrol_capacity(self):
        self.assertTrue(self.service.enrol(self.student, self.course))
        # Second enrolment should fail (capacity)
        student2 = type("Student", (), {"name": "Test2", "completed_courses": [], "enrolled_courses": []})()
        self.assertFalse(self.service.enrol(student2, self.course))

class TestGradeState(unittest.TestCase):
    def setUp(self):
        self.student = type("Student", (), {"name": "Test"})()
        self.course = Course("T101", "Test Course", "Dr. Test", 1)
        self.grade = Grade(self.student, self.course, "A")

    def test_state_transitions(self):
        self.assertIsInstance(self.grade.state, DraftState)
        self.grade.submit()
        self.assertIsInstance(self.grade.state, PendingState)
        self.grade.submit()
        self.assertIsInstance(self.grade.state, SubmittedState)
        self.grade.undo()
        self.assertIsInstance(self.grade.state, PendingState)

if __name__ == "__main__":
    unittest.main()
