"""
Enrollment Service - Core business logic for course enrollment operations.
Implements the business tier of the 3-tier architecture.
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime
from models.user import Student
from models.course import Course
from patterns.observer import Subject
from patterns.strategy import ValidationContext, ValidationStrategyFactory
from patterns.command import CommandInvoker, EnrollStudentCommand, DropStudentCommand


class EnrollmentService(Subject):
    """
    Service for managing course enrollments.
    Implements the Observer pattern as a Subject for notifications.
    """
    
    def __init__(self):
        super().__init__()
        self._students: Dict[str, Student] = {}
        self._courses: Dict[str, Course] = {}
        self._enrollments: Dict[str, List[str]] = {}  # student_id -> list of course_ids
        self._validation_context = ValidationContext(
            ValidationStrategyFactory.create_standard_validation()
        )
        self._command_invoker = CommandInvoker()
    
    def register_student(self, student: Student):
        """Register a student in the system."""
        self._students[student.user_id] = student
        self._enrollments[student.user_id] = []
    
    def register_course(self, course: Course):
        """Register a course in the system."""
        self._courses[course.course_id] = course
    
    def enroll_student(self, student_id: str, course_id: str) -> bool:
        """
        Enroll a student in a course.
        Returns True if successful, False otherwise.
        """
        # Validate inputs
        if student_id not in self._students:
            return False
        
        if course_id not in self._courses:
            return False
        
        student = self._students[student_id]
        course = self._courses[course_id]
        
        # Validate enrollment using strategy pattern
        is_valid, error_message = self._validation_context.validate_enrollment(
            student, course, self._courses
        )
        
        if not is_valid:
            print(f"Enrollment validation failed: {error_message}")
            return False
        
        # Check if already enrolled
        if course_id in self._enrollments[student_id]:
            print(f"Student {student_id} is already enrolled in {course_id}")
            return True
        
        # Attempt enrollment
        success = course.enroll_student(student_id)
        
        if success:
            # Update student's enrolled courses
            student.enroll_in_course(course_id)
            self._enrollments[student_id].append(course_id)
            
            # Notify observers
            self.notify("enrollment_success", {
                'student_id': student_id,
                'student_email': student.email,
                'course_id': course_id,
                'course_name': course.name,
                'timestamp': datetime.now()
            })
            
            print(f"Student {student_id} successfully enrolled in {course_id}")
            return True
        else:
            # Student was added to waitlist
            self.notify("waitlist_added", {
                'student_id': student_id,
                'student_email': student.email,
                'course_id': course_id,
                'course_name': course.name,
                'timestamp': datetime.now()
            })
            
            print(f"Student {student_id} added to waitlist for {course_id}")
            return False
    
    def drop_student(self, student_id: str, course_id: str) -> bool:
        """
        Drop a student from a course.
        Returns True if successful, False otherwise.
        """
        # Validate inputs
        if student_id not in self._students:
            return False
        
        if course_id not in self._courses:
            return False
        
        student = self._students[student_id]
        course = self._courses[course_id]
        
        # Check if enrolled
        if course_id not in self._enrollments[student_id]:
            print(f"Student {student_id} is not enrolled in {course_id}")
            return False
        
        # Drop student from course
        waitlist_promoted = course.drop_student(student_id)
        
        # Update student's enrolled courses
        student.drop_course(course_id)
        self._enrollments[student_id].remove(course_id)
        
        # Notify observers
        self.notify("course_dropped", {
            'student_id': student_id,
            'student_email': student.email,
            'course_id': course_id,
            'course_name': course.name,
            'timestamp': datetime.now()
        })
        
        # If a waitlisted student was promoted, notify them
        if waitlist_promoted:
            self.notify("waitlist_available", {
                'course_id': course_id,
                'course_name': course.name,
                'timestamp': datetime.now()
            })
        
        print(f"Student {student_id} dropped from {course_id}")
        return True
    
    def get_student_schedule(self, student_id: str) -> List[Dict]:
        """Get a student's current schedule."""
        if student_id not in self._students:
            return []
        
        schedule = []
        for course_id in self._enrollments[student_id]:
            if course_id in self._courses:
                course = self._courses[course_id]
                schedule.append({
                    'course_id': course_id,
                    'name': course.name,
                    'department': course.department,
                    'credits': course.credits,
                    'instructor_id': course.instructor_id,
                    'schedule': str(course.schedule),
                    'location': course.schedule.location
                })
        
        return schedule
    
    def get_course_roster(self, course_id: str) -> List[Dict]:
        """Get the roster for a course."""
        if course_id not in self._courses:
            return []
        
        course = self._courses[course_id]
        roster = []
        
        for student_id in course.enrolled_students:
            if student_id in self._students:
                student = self._students[student_id]
                roster.append({
                    'student_id': student_id,
                    'name': student.name,
                    'email': student.email,
                    'major': student.major
                })
        
        return roster
    
    def get_enrollment_statistics(self) -> Dict:
        """Get enrollment statistics for the system."""
        total_students = len(self._students)
        total_courses = len(self._courses)
        total_enrollments = sum(len(enrollments) for enrollments in self._enrollments.values())
        
        # Calculate average enrollments per student
        avg_enrollments = total_enrollments / total_students if total_students > 0 else 0
        
        # Calculate course capacity utilization
        course_utilization = {}
        for course_id, course in self._courses.items():
            utilization = len(course.enrolled_students) / course.capacity if course.capacity > 0 else 0
            course_utilization[course_id] = {
                'name': course.name,
                'enrolled': len(course.enrolled_students),
                'capacity': course.capacity,
                'utilization': utilization
            }
        
        return {
            'total_students': total_students,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'average_enrollments_per_student': avg_enrollments,
            'course_utilization': course_utilization
        }
    
    def get_enrollment_state(self, student_id: str, course_id: str) -> Dict:
        """Get the current enrollment state for undo operations."""
        return {
            'student_id': student_id,
            'course_id': course_id,
            'enrolled': course_id in self._enrollments.get(student_id, []),
            'timestamp': datetime.now()
        }
    
    def restore_enrollment_state(self, student_id: str, course_id: str, state: Dict) -> bool:
        """Restore enrollment state for undo operations."""
        try:
            if state['enrolled']:
                # Restore enrollment
                return self.enroll_student(student_id, course_id)
            else:
                # Restore drop
                return self.drop_student(student_id, course_id)
        except:
            return False
    
    def execute_enrollment_command(self, command_type: str, student_id: str, course_id: str) -> bool:
        """Execute an enrollment command using the Command pattern."""
        if command_type == "enroll":
            command = EnrollStudentCommand(student_id, course_id, self)
        elif command_type == "drop":
            command = DropStudentCommand(student_id, course_id, self)
        else:
            return False
        
        return self._command_invoker.execute_command(command)
    
    def undo_last_enrollment(self) -> bool:
        """Undo the last enrollment operation."""
        return self._command_invoker.undo_last_command()
    
    def get_enrollment_history(self) -> List[str]:
        """Get the enrollment command history."""
        history = []
        for command in self._command_invoker.get_command_history():
            history.append(command.get_description())
        return history
    
    def set_validation_strategy(self, strategy_name: str):
        """Set the validation strategy."""
        if strategy_name == "standard":
            self._validation_context.set_strategy(
                ValidationStrategyFactory.create_standard_validation()
            )
        elif strategy_name == "strict":
            self._validation_context.set_strategy(
                ValidationStrategyFactory.create_strict_validation()
            )
        elif strategy_name == "basic":
            self._validation_context.set_strategy(
                ValidationStrategyFactory.create_basic_validation()
            )
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get a course by its ID."""
        return self._courses.get(course_id)
    
    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Get a student by their ID."""
        return self._students.get(student_id)
