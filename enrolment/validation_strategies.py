from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, student, course):
        pass

class PrerequisiteValidation(ValidationStrategy):
    def validate(self, student, course):
        # Assume student.completed_courses is a list of course ids
        return all(prereq in getattr(student, "completed_courses", []) for prereq in course.prerequisites)

class CapacityValidation(ValidationStrategy):
    def validate(self, student, course):
        return len(course.enrolled_students) < course.capacity

class ScheduleConflictValidation(ValidationStrategy):
    def validate(self, student, course):
        # Assume student.enrolled_courses is a list of Course objects
        for enrolled in getattr(student, "enrolled_courses", []):
            # Ignore unknown schedules
            if enrolled.schedule is None or course.schedule is None:
                continue
            if enrolled.schedule == course.schedule:
                return False
        return True
