"""
Grade Service - Business logic for grade management operations.
Handles grade submission, validation, and academic record management.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from models.user import Student
from models.course import Course
from patterns.observer import Subject
from patterns.command import CommandInvoker, SubmitGradeCommand


class GradeService(Subject):
    """
    Service for managing grades and academic records.
    Implements the Observer pattern for grade-related notifications.
    """
    
    def __init__(self):
        super().__init__()
        self._grades: Dict[str, Dict[str, str]] = {}  # course_id -> {student_id: grade}
        self._grade_history: Dict[str, List[Dict]] = {}  # student_id -> list of grade records
        self._pending_grades: Dict[str, List[Dict]] = {}  # course_id -> list of pending grade submissions
        self._command_invoker = CommandInvoker()
    
    def submit_grades(self, course_id: str, grade_submissions: List[Dict]) -> bool:
        """
        Submit grades for a course.
        
        Args:
            course_id: ID of the course
            grade_submissions: List of grade submissions with student_id, grade, credits
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate grade submissions
            if not self._validate_grade_submissions(grade_submissions):
                return False
            
            # Store pending grades
            self._pending_grades[course_id] = grade_submissions.copy()
            
            # Process each grade submission
            for submission in grade_submissions:
                student_id = submission['student_id']
                grade = submission['grade']
                credits = submission['credits']
                
                # Update grades dictionary
                if course_id not in self._grades:
                    self._grades[course_id] = {}
                
                self._grades[course_id][student_id] = grade
                
                # Update student's academic record
                self._update_student_record(student_id, course_id, grade, credits)
                
                # Notify observers
                self.notify("grade_submitted", {
                    'student_id': student_id,
                    'course_id': course_id,
                    'grade': grade,
                    'credits': credits,
                    'timestamp': datetime.now()
                })
            
            # Clear pending grades after successful submission
            del self._pending_grades[course_id]
            
            print(f"Successfully submitted grades for course {course_id}")
            return True
            
        except Exception as e:
            print(f"Grade submission failed: {str(e)}")
            return False
    
    def _validate_grade_submissions(self, grade_submissions: List[Dict]) -> bool:
        """Validate grade submissions."""
        valid_grades = {'A', 'B', 'C', 'D', 'F', 'A+', 'A-', 'B+', 'B-', 'C+', 'C-', 'D+', 'D-'}
        
        for submission in grade_submissions:
            # Check required fields
            if not all(field in submission for field in ['student_id', 'grade', 'credits']):
                print("Missing required fields in grade submission")
                return False
            
            # Validate grade
            if submission['grade'].upper() not in valid_grades:
                print(f"Invalid grade: {submission['grade']}")
                return False
            
            # Validate credits
            if not isinstance(submission['credits'], int) or submission['credits'] <= 0:
                print(f"Invalid credits: {submission['credits']}")
                return False
        
        return True
    
    def _update_student_record(self, student_id: str, course_id: str, grade: str, credits: int):
        """Update student's academic record."""
        if student_id not in self._grade_history:
            self._grade_history[student_id] = []
        
        # Add grade record
        grade_record = {
            'course_id': course_id,
            'grade': grade,
            'credits': credits,
            'submitted_at': datetime.now()
        }
        
        self._grade_history[student_id].append(grade_record)
    
    def get_student_grade(self, course_id: str, student_id: str) -> Optional[str]:
        """Get a student's grade for a specific course."""
        if course_id in self._grades and student_id in self._grades[course_id]:
            return self._grades[course_id][student_id]
        return None
    
    def get_student_grades(self, student_id: str) -> List[Dict]:
        """Get all grades for a student."""
        return self._grade_history.get(student_id, []).copy()
    
    def get_course_grades(self, course_id: str) -> Dict[str, str]:
        """Get all grades for a course."""
        return self._grades.get(course_id, {}).copy()
    
    def calculate_student_gpa(self, student_id: str) -> float:
        """Calculate GPA for a student."""
        if student_id not in self._grade_history:
            return 0.0
        
        total_points = 0
        total_credits = 0
        
        # Grade point mapping
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        
        for record in self._grade_history[student_id]:
            grade = record['grade'].upper()
            credits = record['credits']
            
            if grade in grade_points:
                total_points += grade_points[grade] * credits
                total_credits += credits
        
        return total_points / total_credits if total_credits > 0 else 0.0
    
    def get_grade_statistics(self, course_id: str) -> Dict:
        """Get grade statistics for a course."""
        if course_id not in self._grades:
            return {}
        
        grades = self._grades[course_id]
        grade_counts = {}
        total_students = len(grades)
        
        # Count grades
        for grade in grades.values():
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        # Calculate percentages
        grade_percentages = {}
        for grade, count in grade_counts.items():
            grade_percentages[grade] = (count / total_students) * 100 if total_students > 0 else 0
        
        return {
            'total_students': total_students,
            'grade_distribution': grade_counts,
            'grade_percentages': grade_percentages
        }
    
    def restore_grades(self, course_id: str, original_grades: Dict[str, str]) -> bool:
        """Restore original grades for undo operations."""
        try:
            if course_id in self._grades:
                self._grades[course_id] = original_grades.copy()
            return True
        except:
            return False
    
    def execute_grade_command(self, course_id: str, grade_submissions: List[Dict]) -> bool:
        """Execute a grade submission command using the Command pattern."""
        command = SubmitGradeCommand(course_id, grade_submissions, self)
        return self._command_invoker.execute_command(command)
    
    def undo_last_grade_submission(self) -> bool:
        """Undo the last grade submission."""
        return self._command_invoker.undo_last_command()
    
    def get_grade_submission_history(self) -> List[str]:
        """Get the grade submission command history."""
        history = []
        for command in self._command_invoker.get_command_history():
            history.append(command.get_description())
        return history
    
    def get_pending_grades(self, course_id: str) -> List[Dict]:
        """Get pending grade submissions for a course."""
        return self._pending_grades.get(course_id, []).copy()
    
    def approve_grades(self, course_id: str) -> bool:
        """Approve pending grades for a course."""
        if course_id not in self._pending_grades:
            return False
        
        # Process pending grades
        success = self.submit_grades(course_id, self._pending_grades[course_id])
        
        if success:
            # Notify observers of approval
            self.notify("grades_approved", {
                'course_id': course_id,
                'timestamp': datetime.now()
            })
        
        return success
    
    def reject_grades(self, course_id: str, reason: str) -> bool:
        """Reject pending grades for a course."""
        if course_id not in self._pending_grades:
            return False
        
        # Clear pending grades
        del self._pending_grades[course_id]
        
        # Notify observers of rejection
        self.notify("grades_rejected", {
            'course_id': course_id,
            'reason': reason,
            'timestamp': datetime.now()
        })
        
        print(f"Grades rejected for course {course_id}: {reason}")
        return True
    
    def get_academic_progress(self, student_id: str) -> Dict:
        """Get academic progress summary for a student."""
        if student_id not in self._grade_history:
            return {
                'total_courses': 0,
                'total_credits': 0,
                'gpa': 0.0,
                'completed_courses': []
            }
        
        records = self._grade_history[student_id]
        total_credits = sum(record['credits'] for record in records)
        gpa = self.calculate_student_gpa(student_id)
        
        return {
            'total_courses': len(records),
            'total_credits': total_credits,
            'gpa': gpa,
            'completed_courses': records.copy()
        }
