"""
Strategy Pattern implementation for different enrollment validation strategies.
This pattern allows the system to use different validation algorithms interchangeably.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from models.user import Student
from models.course import Course


class ValidationStrategy(ABC):
    """
    Abstract strategy interface for enrollment validation.
    """
    
    @abstractmethod
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """
        Validate enrollment request.
        
        Args:
            student: Student requesting enrollment
            course: Course to enroll in
            all_courses: Dictionary of all available courses
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass


class PrerequisiteValidationStrategy(ValidationStrategy):
    """
    Strategy for validating course prerequisites.
    """
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate that student meets all course prerequisites."""
        for prerequisite in course.prerequisites:
            # Check if student has completed the prerequisite course
            completed_course_ids = [c['course_id'] for c in student.completed_courses]
            
            if prerequisite.course_id not in completed_course_ids:
                return False, f"Prerequisite not met: {prerequisite.course_id}"
            
            # Check if student met the minimum grade requirement
            for completed_course in student.completed_courses:
                if completed_course['course_id'] == prerequisite.course_id:
                    grade = completed_course['grade'].upper()
                    min_grade = prerequisite.min_grade.upper()
                    
                    if not self._grade_satisfies_requirement(grade, min_grade):
                        return False, f"Grade requirement not met for {prerequisite.course_id}: need {min_grade}, got {grade}"
                    break
        
        return True, "Prerequisites satisfied"
    
    def _grade_satisfies_requirement(self, grade: str, min_grade: str) -> bool:
        """Check if a grade satisfies the minimum requirement."""
        grade_values = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        
        if grade not in grade_values or min_grade not in grade_values:
            return False
        
        return grade_values[grade] >= grade_values[min_grade]


class CapacityValidationStrategy(ValidationStrategy):
    """
    Strategy for validating course capacity.
    """
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate that course has available capacity."""
        if course.is_full:
            return False, f"Course {course.course_id} is full"
        
        return True, "Capacity available"


class ScheduleConflictValidationStrategy(ValidationStrategy):
    """
    Strategy for validating schedule conflicts.
    """
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate that the course doesn't conflict with student's schedule."""
        # Get all courses the student is currently enrolled in
        enrolled_course_ids = student.enrolled_courses
        
        for enrolled_course_id in enrolled_course_ids:
            if enrolled_course_id in all_courses:
                enrolled_course = all_courses[enrolled_course_id]
                
                # Check for schedule conflict
                if course.schedule.conflicts_with(enrolled_course.schedule):
                    return False, f"Schedule conflict with {enrolled_course_id}"
        
        return True, "No schedule conflicts"


class MajorValidationStrategy(ValidationStrategy):
    """
    Strategy for validating major-specific requirements.
    """
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate that the course is appropriate for the student's major."""
        # Some courses might be restricted to specific majors
        # This is a simplified implementation
        if hasattr(course, 'restricted_majors') and course.restricted_majors:
            if student.major not in course.restricted_majors:
                return False, f"Course restricted to majors: {', '.join(course.restricted_majors)}"
        
        return True, "Major requirements satisfied"


class GPAValidationStrategy(ValidationStrategy):
    """
    Strategy for validating GPA requirements.
    """
    
    def __init__(self, min_gpa: float = 2.0):
        self.min_gpa = min_gpa
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate that student meets GPA requirements."""
        if student.gpa < self.min_gpa:
            return False, f"GPA requirement not met: need {self.min_gpa}, current {student.gpa}"
        
        return True, "GPA requirements satisfied"


class CompositeValidationStrategy(ValidationStrategy):
    """
    Composite strategy that combines multiple validation strategies.
    """
    
    def __init__(self, strategies: List[ValidationStrategy]):
        self.strategies = strategies
    
    def validate(self, student: Student, course: Course, 
                all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate using all strategies in sequence."""
        for strategy in self.strategies:
            is_valid, message = strategy.validate(student, course, all_courses)
            if not is_valid:
                return False, message
        
        return True, "All validations passed"
    
    def add_strategy(self, strategy: ValidationStrategy):
        """Add a new validation strategy."""
        self.strategies.append(strategy)
    
    def remove_strategy(self, strategy: ValidationStrategy):
        """Remove a validation strategy."""
        if strategy in self.strategies:
            self.strategies.remove(strategy)


class ValidationContext:
    """
    Context class that uses validation strategies.
    """
    
    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: ValidationStrategy):
        """Set the validation strategy."""
        self._strategy = strategy
    
    def validate_enrollment(self, student: Student, course: Course, 
                           all_courses: Dict[str, Course]) -> Tuple[bool, str]:
        """Validate enrollment using the current strategy."""
        return self._strategy.validate(student, course, all_courses)


class ValidationStrategyFactory:
    """
    Factory for creating different validation strategies.
    """
    
    @staticmethod
    def create_standard_validation() -> CompositeValidationStrategy:
        """Create a standard validation strategy with common validations."""
        strategies = [
            PrerequisiteValidationStrategy(),
            CapacityValidationStrategy(),
            ScheduleConflictValidationStrategy(),
            GPAValidationStrategy(min_gpa=2.0)
        ]
        return CompositeValidationStrategy(strategies)
    
    @staticmethod
    def create_strict_validation() -> CompositeValidationStrategy:
        """Create a strict validation strategy with higher requirements."""
        strategies = [
            PrerequisiteValidationStrategy(),
            CapacityValidationStrategy(),
            ScheduleConflictValidationStrategy(),
            GPAValidationStrategy(min_gpa=3.0),
            MajorValidationStrategy()
        ]
        return CompositeValidationStrategy(strategies)
    
    @staticmethod
    def create_basic_validation() -> CompositeValidationStrategy:
        """Create a basic validation strategy with minimal requirements."""
        strategies = [
            CapacityValidationStrategy(),
            ScheduleConflictValidationStrategy()
        ]
        return CompositeValidationStrategy(strategies)
