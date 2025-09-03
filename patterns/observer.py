"""
Observer Pattern implementation for the notification system.
This pattern allows the system to notify multiple observers when enrollment events occur.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class Observer(ABC):
    """
    Abstract observer interface for the Observer pattern.
    """
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]):
        """
        Update method called when an event occurs.
        
        Args:
            event_type: Type of event that occurred
            data: Event data containing relevant information
        """
        pass


class Subject(ABC):
    """
    Abstract subject interface for the Observer pattern.
    """
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer from the subject."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Dict[str, Any]):
        """Notify all observers of an event."""
        for observer in self._observers:
            observer.update(event_type, data)


class EmailNotificationObserver(Observer):
    """
    Concrete observer that sends email notifications.
    """
    
    def __init__(self, email_service):
        self.email_service = email_service
    
    def update(self, event_type: str, data: Dict[str, Any]):
        """Send email notification based on event type."""
        if event_type == "enrollment_success":
            self._send_enrollment_confirmation(data)
        elif event_type == "course_dropped":
            self._send_drop_confirmation(data)
        elif event_type == "waitlist_available":
            self._send_waitlist_notification(data)
        elif event_type == "grade_submitted":
            self._send_grade_notification(data)
    
    def _send_enrollment_confirmation(self, data: Dict[str, Any]):
        """Send enrollment confirmation email."""
        student_email = data.get('student_email')
        course_name = data.get('course_name')
        
        message = f"""
        Dear Student,
        
        You have successfully enrolled in {course_name}.
        
        Best regards,
        NexusEnroll System
        """
        
        self.email_service.send_email(student_email, "Enrollment Confirmation", message)
        print(f"Email sent to {student_email}: Enrollment confirmation for {course_name}")
    
    def _send_drop_confirmation(self, data: Dict[str, Any]):
        """Send course drop confirmation email."""
        student_email = data.get('student_email')
        course_name = data.get('course_name')
        
        message = f"""
        Dear Student,
        
        You have successfully dropped {course_name}.
        
        Best regards,
        NexusEnroll System
        """
        
        self.email_service.send_email(student_email, "Course Drop Confirmation", message)
        print(f"Email sent to {student_email}: Drop confirmation for {course_name}")
    
    def _send_waitlist_notification(self, data: Dict[str, Any]):
        """Send waitlist availability notification."""
        student_email = data.get('student_email')
        course_name = data.get('course_name')
        
        message = f"""
        Dear Student,
        
        A spot has become available in {course_name} that you were waitlisted for.
        Please log in to the system to enroll if you're still interested.
        
        Best regards,
        NexusEnroll System
        """
        
        self.email_service.send_email(student_email, "Waitlist Spot Available", message)
        print(f"Email sent to {student_email}: Waitlist notification for {course_name}")
    
    def _send_grade_notification(self, data: Dict[str, Any]):
        """Send grade submission notification."""
        student_email = data.get('student_email')
        course_name = data.get('course_name')
        grade = data.get('grade')
        
        message = f"""
        Dear Student,
        
        Your grade for {course_name} has been submitted: {grade}
        
        Best regards,
        NexusEnroll System
        """
        
        self.email_service.send_email(student_email, "Grade Posted", message)
        print(f"Email sent to {student_email}: Grade notification for {course_name} - {grade}")


class AdvisorNotificationObserver(Observer):
    """
    Concrete observer that notifies academic advisors.
    """
    
    def __init__(self, advisor_service):
        self.advisor_service = advisor_service
    
    def update(self, event_type: str, data: Dict[str, Any]):
        """Notify advisor based on event type."""
        if event_type == "critical_course_dropped":
            self._notify_advisor_critical_drop(data)
        elif event_type == "low_gpa_warning":
            self._notify_advisor_low_gpa(data)
    
    def _notify_advisor_critical_drop(self, data: Dict[str, Any]):
        """Notify advisor when student drops a critical course."""
        student_id = data.get('student_id')
        course_name = data.get('course_name')
        advisor_id = data.get('advisor_id')
        
        message = f"Student {student_id} has dropped critical course {course_name}"
        self.advisor_service.notify_advisor(advisor_id, "Critical Course Drop", message)
        print(f"Advisor {advisor_id} notified: {message}")
    
    def _notify_advisor_low_gpa(self, data: Dict[str, Any]):
        """Notify advisor of low GPA warning."""
        student_id = data.get('student_id')
        gpa = data.get('gpa')
        advisor_id = data.get('advisor_id')
        
        message = f"Student {student_id} has a low GPA: {gpa}"
        self.advisor_service.notify_advisor(advisor_id, "Low GPA Warning", message)
        print(f"Advisor {advisor_id} notified: {message}")


class SystemLogObserver(Observer):
    """
    Concrete observer that logs system events.
    """
    
    def __init__(self, logger):
        self.logger = logger
    
    def update(self, event_type: str, data: Dict[str, Any]):
        """Log the event."""
        timestamp = datetime.now().isoformat()
        log_message = f"[{timestamp}] {event_type}: {data}"
        self.logger.log(log_message)
        print(f"System Log: {log_message}")


class EmailService:
    """
    Mock email service for demonstration purposes.
    In a real system, this would integrate with an actual email service.
    """
    
    def send_email(self, to_email: str, subject: str, message: str):
        """Send an email (mock implementation)."""
        # In a real implementation, this would send actual emails
        pass


class AdvisorService:
    """
    Mock advisor service for demonstration purposes.
    """
    
    def notify_advisor(self, advisor_id: str, subject: str, message: str):
        """Notify an advisor (mock implementation)."""
        # In a real implementation, this would send notifications to advisors
        pass


class Logger:
    """
    Mock logger for demonstration purposes.
    """
    
    def log(self, message: str):
        """Log a message (mock implementation)."""
        # In a real implementation, this would write to a log file or database
        pass
