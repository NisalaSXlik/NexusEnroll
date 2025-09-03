"""
User models for the NexusEnroll system.
Implements the base User class and specific user types (Student, Faculty, Administrator).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserType(Enum):
    """Enumeration for different user types."""
    STUDENT = "student"
    FACULTY = "faculty"
    ADMINISTRATOR = "administrator"


class User(ABC):
    """
    Abstract base class for all users in the system.
    Demonstrates the Template Method pattern and follows SOLID principles.
    """
    
    def __init__(self, user_id: str, name: str, email: str, user_type: UserType):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._user_type = user_type
        self._created_at = datetime.now()
        self._is_active = True
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def user_type(self) -> UserType:
        return self._user_type
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def deactivate(self):
        """Deactivate the user account."""
        self._is_active = False
    
    def activate(self):
        """Activate the user account."""
        self._is_active = True
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        """Get list of permissions for this user type."""
        pass
    
    def __str__(self) -> str:
        return f"{self._user_type.value.title()}: {self._name} ({self._user_id})"


class Student(User):
    """
    Student user class with specific student-related functionality.
    """
    
    def __init__(self, user_id: str, name: str, email: str, major: str, advisor_id: Optional[str] = None):
        super().__init__(user_id, name, email, UserType.STUDENT)
        self._major = major
        self._advisor_id = advisor_id
        self._enrolled_courses: List[str] = []
        self._completed_courses: List[dict] = []
        self._gpa = 0.0
    
    @property
    def major(self) -> str:
        return self._major
    
    @property
    def advisor_id(self) -> Optional[str]:
        return self._advisor_id
    
    @property
    def enrolled_courses(self) -> List[str]:
        return self._enrolled_courses.copy()
    
    @property
    def completed_courses(self) -> List[dict]:
        return self._completed_courses.copy()
    
    @property
    def gpa(self) -> float:
        return self._gpa
    
    def enroll_in_course(self, course_id: str):
        """Enroll student in a course."""
        if course_id not in self._enrolled_courses:
            self._enrolled_courses.append(course_id)
    
    def drop_course(self, course_id: str):
        """Drop a course."""
        if course_id in self._enrolled_courses:
            self._enrolled_courses.remove(course_id)
    
    def complete_course(self, course_id: str, grade: str, credits: int):
        """Mark a course as completed with grade and credits."""
        self._completed_courses.append({
            'course_id': course_id,
            'grade': grade,
            'credits': credits,
            'completed_at': datetime.now()
        })
        self._calculate_gpa()
    
    def _calculate_gpa(self):
        """Calculate GPA based on completed courses."""
        if not self._completed_courses:
            self._gpa = 0.0
            return
        
        total_points = 0
        total_credits = 0
        
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        
        for course in self._completed_courses:
            grade = course['grade'].upper()
            credits = course['credits']
            if grade in grade_points:
                total_points += grade_points[grade] * credits
                total_credits += credits
        
        self._gpa = total_points / total_credits if total_credits > 0 else 0.0
    
    def get_permissions(self) -> List[str]:
        return [
            "browse_courses",
            "enroll_courses",
            "drop_courses",
            "view_schedule",
            "view_grades",
            "view_progress"
        ]


class Faculty(User):
    """
    Faculty user class with instructor-specific functionality.
    """
    
    def __init__(self, user_id: str, name: str, email: str, department: str):
        super().__init__(user_id, name, email, UserType.FACULTY)
        self._department = department
        self._teaching_courses: List[str] = []
        self._max_courses = 4  # Maximum courses per semester
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def teaching_courses(self) -> List[str]:
        return self._teaching_courses.copy()
    
    def assign_course(self, course_id: str) -> bool:
        """Assign a course to this faculty member."""
        if len(self._teaching_courses) < self._max_courses:
            if course_id not in self._teaching_courses:
                self._teaching_courses.append(course_id)
                return True
        return False
    
    def remove_course(self, course_id: str):
        """Remove a course assignment."""
        if course_id in self._teaching_courses:
            self._teaching_courses.remove(course_id)
    
    def get_permissions(self) -> List[str]:
        return [
            "view_roster",
            "submit_grades",
            "manage_course_info",
            "view_teaching_schedule"
        ]


class Administrator(User):
    """
    Administrator user class with system management capabilities.
    """
    
    def __init__(self, user_id: str, name: str, email: str, department: str):
        super().__init__(user_id, name, email, UserType.ADMINISTRATOR)
        self._department = department
        self._admin_level = "standard"  # standard, senior, super
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def admin_level(self) -> str:
        return self._admin_level
    
    def set_admin_level(self, level: str):
        """Set administrator level."""
        if level in ["standard", "senior", "super"]:
            self._admin_level = level
    
    def get_permissions(self) -> List[str]:
        base_permissions = [
            "manage_courses",
            "manage_users",
            "view_reports",
            "override_enrollment",
            "system_configuration"
        ]
        
        if self._admin_level == "senior":
            base_permissions.extend(["manage_faculty", "financial_override"])
        elif self._admin_level == "super":
            base_permissions.extend(["system_admin", "user_management", "audit_logs"])
        
        return base_permissions
