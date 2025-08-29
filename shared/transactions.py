from abc import ABC, abstractmethod

class Transaction(ABC):
    def execute(self):
        try:
            self._do_execute()
        except Exception as e:
            self.rollback()
            print(f"Transaction failed: {e}")

    @abstractmethod
    def _do_execute(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

class EnrolmentTransaction(Transaction):
    def __init__(self, enrolment_service, student, course):
        self.enrolment_service = enrolment_service
        self.student = student
        self.course = course
        self._enrolled = False

    def _do_execute(self):
        self._enrolled = self.enrolment_service.enrol(self.student, self.course)
        if not self._enrolled:
            raise Exception("Enrolment failed")

    def rollback(self):
        if self._enrolled:
            self.enrolment_service.drop(self.student, self.course)
            print("Enrolment rolled back.")

class GradeTransaction(Transaction):
    def __init__(self, grade_command):
        self.grade_command = grade_command
        self._submitted = False

    def _do_execute(self):
        self.grade_command.execute()
        self._submitted = True

    def rollback(self):
        if self._submitted:
            self.grade_command.undo()
            print("Grade submission rolled back.")
