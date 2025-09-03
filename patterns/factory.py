"""
Factory Method Pattern implementation for creating users and courses.
This pattern provides a way to create objects without specifying their exact classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from models.user import User, Student, Faculty, Administrator, UserType
from models.course import Course, Schedule, DayOfWeek, Prerequisite
from datetime import time


class UserFactory(ABC):
    """
    Abstract factory for creating user objects.
    """
    
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a user object based on the provided data."""
        pass


class StudentFactory(UserFactory):
    """
    Concrete factory for creating Student objects.
    """
    
    def create_user(self, user_data: Dict[str, Any]) -> Student:
        """Create a Student object."""
        required_fields = ['user_id', 'name', 'email', 'major']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        return Student(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email'],
            major=user_data['major'],
            advisor_id=user_data.get('advisor_id')
        )


class FacultyFactory(UserFactory):
    """
    Concrete factory for creating Faculty objects.
    """
    
    def create_user(self, user_data: Dict[str, Any]) -> Faculty:
        """Create a Faculty object."""
        required_fields = ['user_id', 'name', 'email', 'department']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        return Faculty(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email'],
            department=user_data['department']
        )


class AdministratorFactory(UserFactory):
    """
    Concrete factory for creating Administrator objects.
    """
    
    def create_user(self, user_data: Dict[str, Any]) -> Administrator:
        """Create an Administrator object."""
        required_fields = ['user_id', 'name', 'email', 'department']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        admin = Administrator(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email'],
            department=user_data['department']
        )
        
        # Set admin level if provided
        if 'admin_level' in user_data:
            admin.set_admin_level(user_data['admin_level'])
        
        return admin


class UserFactoryProducer:
    """
    Factory producer that returns the appropriate factory based on user type.
    """
    
    @staticmethod
    def get_factory(user_type: UserType) -> UserFactory:
        """Get the appropriate factory for the given user type."""
        factories = {
            UserType.STUDENT: StudentFactory(),
            UserType.FACULTY: FacultyFactory(),
            UserType.ADMINISTRATOR: AdministratorFactory()
        }
        
        if user_type not in factories:
            raise ValueError(f"Unknown user type: {user_type}")
        
        return factories[user_type]


class CourseFactory:
    """
    Factory for creating Course objects with different configurations.
    """
    
    @staticmethod
    def create_course(course_data: Dict[str, Any]) -> Course:
        """Create a Course object from course data."""
        required_fields = [
            'course_id', 'name', 'description', 'department', 
            'credits', 'instructor_id', 'capacity', 'schedule'
        ]
        
        for field in required_fields:
            if field not in course_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Create schedule object
        schedule_data = course_data['schedule']
        schedule = CourseFactory._create_schedule(schedule_data)
        
        # Create course
        course = Course(
            course_id=course_data['course_id'],
            name=course_data['name'],
            description=course_data['description'],
            department=course_data['department'],
            credits=course_data['credits'],
            instructor_id=course_data['instructor_id'],
            capacity=course_data['capacity'],
            schedule=schedule
        )
        
        # Add prerequisites if provided
        if 'prerequisites' in course_data:
            for prereq_data in course_data['prerequisites']:
                prereq = Prerequisite(
                    course_id=prereq_data['course_id'],
                    min_grade=prereq_data.get('min_grade', 'C')
                )
                course.add_prerequisite(prereq)
        
        return course
    
    @staticmethod
    def _create_schedule(schedule_data: Dict[str, Any]) -> Schedule:
        """Create a Schedule object from schedule data."""
        # Parse days
        days = []
        for day_str in schedule_data['days']:
            try:
                day = DayOfWeek(day_str.title())
                days.append(day)
            except ValueError:
                raise ValueError(f"Invalid day: {day_str}")
        
        # Parse times
        start_time = time.fromisoformat(schedule_data['start_time'])
        end_time = time.fromisoformat(schedule_data['end_time'])
        
        return Schedule(
            days=days,
            start_time=start_time,
            end_time=end_time,
            location=schedule_data['location']
        )
    
    @staticmethod
    def create_lecture_course(course_id: str, name: str, department: str, 
                            instructor_id: str, capacity: int = 30) -> Course:
        """Create a standard lecture course."""
        course_data = {
            'course_id': course_id,
            'name': name,
            'description': f"Lecture course: {name}",
            'department': department,
            'credits': 3,
            'instructor_id': instructor_id,
            'capacity': capacity,
            'schedule': {
                'days': ['Monday', 'Wednesday', 'Friday'],
                'start_time': '10:00',
                'end_time': '10:50',
                'location': 'Lecture Hall A'
            }
        }
        return CourseFactory.create_course(course_data)
    
    @staticmethod
    def create_lab_course(course_id: str, name: str, department: str, 
                         instructor_id: str, capacity: int = 20) -> Course:
        """Create a lab course."""
        course_data = {
            'course_id': course_id,
            'name': name,
            'description': f"Lab course: {name}",
            'department': department,
            'credits': 1,
            'instructor_id': instructor_id,
            'capacity': capacity,
            'schedule': {
                'days': ['Tuesday', 'Thursday'],
                'start_time': '14:00',
                'end_time': '16:00',
                'location': 'Lab Room B'
            }
        }
        return CourseFactory.create_course(course_data)
    
    @staticmethod
    def create_seminar_course(course_id: str, name: str, department: str, 
                            instructor_id: str, capacity: int = 15) -> Course:
        """Create a seminar course."""
        course_data = {
            'course_id': course_id,
            'name': name,
            'description': f"Seminar course: {name}",
            'department': department,
            'credits': 2,
            'instructor_id': instructor_id,
            'capacity': capacity,
            'schedule': {
                'days': ['Wednesday'],
                'start_time': '15:00',
                'end_time': '17:00',
                'location': 'Seminar Room C'
            }
        }
        return CourseFactory.create_course(course_data)


class EnrollmentFactory:
    """
    Factory for creating enrollment-related objects.
    """
    
    @staticmethod
    def create_enrollment_request(student_id: str, course_id: str, 
                                 request_type: str = "enroll") -> Dict[str, Any]:
        """Create an enrollment request object."""
        return {
            'student_id': student_id,
            'course_id': course_id,
            'request_type': request_type,
            'timestamp': None,  # Will be set when processed
            'status': 'pending'
        }
    
    @staticmethod
    def create_grade_submission(course_id: str, student_id: str, 
                               grade: str, credits: int) -> Dict[str, Any]:
        """Create a grade submission object."""
        return {
            'course_id': course_id,
            'student_id': student_id,
            'grade': grade,
            'credits': credits,
            'submitted_at': None,  # Will be set when processed
            'status': 'pending'
        }
