from abc import ABC, abstractmethod

# Strategy for validation
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, student, course):
        pass

class CapacityValidation(ValidationStrategy):
    def validate(self, student, course):
        return len(course.enrolled_students) < course.capacity

class PrerequisiteValidation(ValidationStrategy):
    def validate(self, student, course):
        # Assume student has attribute completed_courses (list of course ids)
        return all(prereq in getattr(student, "completed_courses", []) for prereq in course.prerequisites)

# Command pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class EnrolCommand(Command):
    def __init__(self, student, course, service):
        self.student = student
        self.course = course
        self.service = service
        self._executed = False

    def execute(self):
        result = self.service._enrol(student=self.student, course=self.course)
        self._executed = result
        return result

    def undo(self):
        if self._executed:
            return self.service._drop(student=self.student, course=self.course)
        return False

class DropCommand(Command):
    def __init__(self, student, course, service):
        self.student = student
        self.course = course
        self.service = service
        self._executed = False

    def execute(self):
        result = self.service._drop(student=self.student, course=self.course)
        self._executed = result
        return result

    def undo(self):
        if self._executed:
            return self.service._enrol(student=self.student, course=self.course)
        return False

class EnrolmentService:
    def __init__(self, validation_strategies=None):
        self.validation_strategies = validation_strategies if validation_strategies else []
        self._history = []

    def enrol(self, student, course):
        cmd = EnrolCommand(student, course, self)
        result = cmd.execute()
        if result:
            self._history.append(cmd)
        return result

    def drop(self, student, course):
        cmd = DropCommand(student, course, self)
        result = cmd.execute()
        if result:
            self._history.append(cmd)
        return result

    def undo_last(self):
        if self._history:
            cmd = self._history.pop()
            return cmd.undo()
        return False

    def _enrol(self, student, course):
        for strategy in self.validation_strategies:
            if not strategy.validate(student, course):
                return False
        return course.enrol_student(student)

    def _drop(self, student, course):
        return course.drop_student(student)
