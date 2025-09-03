"""
Course models for the NexusEnroll system.
Implements Course, Prerequisite, and related classes.
"""

from typing import List, Optional, Dict
from datetime import datetime, time
from enum import Enum


class CourseStatus(Enum):
    """Enumeration for course status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    FULL = "full"


class DayOfWeek(Enum):
    """Enumeration for days of the week."""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Prerequisite:
    """
    Represents a course prerequisite.
    """
    
    def __init__(self, course_id: str, min_grade: str = "C"):
        self.course_id = course_id
        self.min_grade = min_grade.upper()
    
    def __str__(self) -> str:
        return f"Course {self.course_id} (min grade: {self.min_grade})"


class Schedule:
    """
    Represents a course schedule with days and times.
    """
    
    def __init__(self, days: List[DayOfWeek], start_time: time, end_time: time, location: str):
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
    
    def conflicts_with(self, other_schedule) -> bool:
        """Check if this schedule conflicts with another schedule."""
        # Check if any days overlap
        common_days = set(self.days) & set(other_schedule.days)
        if not common_days:
            return False
        
        # Check if times overlap
        return not (self.end_time <= other_schedule.start_time or 
                   other_schedule.end_time <= self.start_time)
    
    def __str__(self) -> str:
        days_str = ", ".join([day.value for day in self.days])
        return f"{days_str} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} at {self.location}"


class Course:
    """
    Course model representing a university course.
    """
    
    def __init__(self, course_id: str, name: str, description: str, 
                 department: str, credits: int, instructor_id: str,
                 capacity: int, schedule: Schedule):
        self._course_id = course_id
        self._name = name
        self._description = description
        self._department = department
        self._credits = credits
        self._instructor_id = instructor_id
        self._capacity = capacity
        self._schedule = schedule
        self._prerequisites: List[Prerequisite] = []
        self._enrolled_students: List[str] = []
        self._waitlist: List[str] = []
        self._status = CourseStatus.ACTIVE
        self._created_at = datetime.now()
    
    @property
    def course_id(self) -> str:
        return self._course_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def credits(self) -> int:
        return self._credits
    
    @property
    def instructor_id(self) -> str:
        return self._instructor_id
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def schedule(self) -> Schedule:
        return self._schedule
    
    @property
    def prerequisites(self) -> List[Prerequisite]:
        return self._prerequisites.copy()
    
    @property
    def enrolled_students(self) -> List[str]:
        return self._enrolled_students.copy()
    
    @property
    def waitlist(self) -> List[str]:
        return self._waitlist.copy()
    
    @property
    def status(self) -> CourseStatus:
        return self._status
    
    @property
    def available_seats(self) -> int:
        return max(0, self._capacity - len(self._enrolled_students))
    
    @property
    def is_full(self) -> bool:
        return len(self._enrolled_students) >= self._capacity
    
    def add_prerequisite(self, prerequisite: Prerequisite):
        """Add a prerequisite to the course."""
        if prerequisite not in self._prerequisites:
            self._prerequisites.append(prerequisite)
    
    def remove_prerequisite(self, course_id: str):
        """Remove a prerequisite by course ID."""
        self._prerequisites = [p for p in self._prerequisites if p.course_id != course_id]
    
    def enroll_student(self, student_id: str) -> bool:
        """
        Enroll a student in the course.
        Returns True if successful, False if added to waitlist.
        """
        if student_id in self._enrolled_students:
            return True  # Already enrolled
        
        if not self.is_full:
            self._enrolled_students.append(student_id)
            # Remove from waitlist if they were there
            if student_id in self._waitlist:
                self._waitlist.remove(student_id)
            return True
        else:
            # Add to waitlist if not already there
            if student_id not in self._waitlist:
                self._waitlist.append(student_id)
            return False
    
    def drop_student(self, student_id: str) -> bool:
        """
        Drop a student from the course.
        Returns True if a waitlisted student was moved to enrolled.
        """
        if student_id in self._enrolled_students:
            self._enrolled_students.remove(student_id)
            
            # Move first waitlisted student to enrolled if any
            if self._waitlist:
                next_student = self._waitlist.pop(0)
                self._enrolled_students.append(next_student)
                return True
        
        # Remove from waitlist if present
        if student_id in self._waitlist:
            self._waitlist.remove(student_id)
        
        return False
    
    def cancel_course(self):
        """Cancel the course."""
        self._status = CourseStatus.CANCELLED
    
    def activate_course(self):
        """Activate the course."""
        self._status = CourseStatus.ACTIVE
    
    def deactivate_course(self):
        """Deactivate the course."""
        self._status = CourseStatus.INACTIVE
    
    def update_capacity(self, new_capacity: int):
        """Update the course capacity."""
        if new_capacity >= len(self._enrolled_students):
            self._capacity = new_capacity
    
    def get_enrollment_info(self) -> Dict:
        """Get comprehensive enrollment information."""
        return {
            'course_id': self._course_id,
            'name': self._name,
            'enrolled_count': len(self._enrolled_students),
            'capacity': self._capacity,
            'available_seats': self.available_seats,
            'waitlist_count': len(self._waitlist),
            'is_full': self.is_full,
            'status': self._status.value
        }
    
    def __str__(self) -> str:
        return f"{self._course_id}: {self._name} ({self._department}) - {len(self._enrolled_students)}/{self._capacity}"


class DegreeProgram:
    """
    Represents a degree program with required courses.
    """
    
    def __init__(self, program_id: str, name: str, department: str, total_credits: int):
        self._program_id = program_id
        self._name = name
        self._department = department
        self._total_credits = total_credits
        self._required_courses: List[str] = []
        self._elective_courses: List[str] = []
        self._core_credits = 0
        self._elective_credits = 0
    
    @property
    def program_id(self) -> str:
        return self._program_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def total_credits(self) -> int:
        return self._total_credits
    
    @property
    def required_courses(self) -> List[str]:
        return self._required_courses.copy()
    
    @property
    def elective_courses(self) -> List[str]:
        return self._elective_courses.copy()
    
    def add_required_course(self, course_id: str, credits: int):
        """Add a required course to the program."""
        if course_id not in self._required_courses:
            self._required_courses.append(course_id)
            self._core_credits += credits
    
    def add_elective_course(self, course_id: str, credits: int):
        """Add an elective course to the program."""
        if course_id not in self._elective_courses:
            self._elective_courses.append(course_id)
            self._elective_credits += credits
    
    def get_remaining_requirements(self, completed_courses: List[str]) -> Dict:
        """Get remaining course requirements for a student."""
        remaining_required = [c for c in self._required_courses if c not in completed_courses]
        remaining_electives = [c for c in self._elective_courses if c not in completed_courses]
        
        return {
            'required_courses': remaining_required,
            'elective_courses': remaining_electives,
            'core_credits_needed': self._core_credits,
            'elective_credits_needed': self._elective_credits
        }
