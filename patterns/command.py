"""
Command Pattern implementation for enrollment operations.
This pattern encapsulates enrollment requests as objects, allowing for queuing, logging, and undo operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from enum import Enum


class CommandStatus(Enum):
    """Enumeration for command status."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Command(ABC):
    """
    Abstract command interface for the Command pattern.
    """
    
    def __init__(self):
        self._status = CommandStatus.PENDING
        self._timestamp = None
        self._error_message = None
    
    @property
    def status(self) -> CommandStatus:
        return self._status
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    @property
    def error_message(self) -> str:
        return self._error_message
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command. Returns True if successful, False otherwise."""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo the command. Returns True if successful, False otherwise."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of the command."""
        pass


class EnrollStudentCommand(Command):
    """
    Command for enrolling a student in a course.
    """
    
    def __init__(self, student_id: str, course_id: str, enrollment_service):
        super().__init__()
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_service = enrollment_service
        self._original_state = None
    
    def execute(self) -> bool:
        """Execute the enrollment command."""
        try:
            self._status = CommandStatus.EXECUTING
            self._timestamp = datetime.now()
            
            # Store original state for potential undo
            self._original_state = self.enrollment_service.get_enrollment_state(
                self.student_id, self.course_id
            )
            
            # Execute enrollment
            success = self.enrollment_service.enroll_student(self.student_id, self.course_id)
            
            if success:
                self._status = CommandStatus.COMPLETED
                return True
            else:
                self._status = CommandStatus.FAILED
                self._error_message = "Enrollment failed"
                return False
                
        except Exception as e:
            self._status = CommandStatus.FAILED
            self._error_message = str(e)
            return False
    
    def undo(self) -> bool:
        """Undo the enrollment command."""
        try:
            if self._original_state is None:
                return False
            
            # Restore original state
            success = self.enrollment_service.restore_enrollment_state(
                self.student_id, self.course_id, self._original_state
            )
            
            if success:
                self._status = CommandStatus.CANCELLED
                return True
            else:
                return False
                
        except Exception as e:
            self._error_message = f"Undo failed: {str(e)}"
            return False
    
    def get_description(self) -> str:
        return f"Enroll student {self.student_id} in course {self.course_id}"


class DropStudentCommand(Command):
    """
    Command for dropping a student from a course.
    """
    
    def __init__(self, student_id: str, course_id: str, enrollment_service):
        super().__init__()
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_service = enrollment_service
        self._original_state = None
    
    def execute(self) -> bool:
        """Execute the drop command."""
        try:
            self._status = CommandStatus.EXECUTING
            self._timestamp = datetime.now()
            
            # Store original state for potential undo
            self._original_state = self.enrollment_service.get_enrollment_state(
                self.student_id, self.course_id
            )
            
            # Execute drop
            success = self.enrollment_service.drop_student(self.student_id, self.course_id)
            
            if success:
                self._status = CommandStatus.COMPLETED
                return True
            else:
                self._status = CommandStatus.FAILED
                self._error_message = "Drop failed"
                return False
                
        except Exception as e:
            self._status = CommandStatus.FAILED
            self._error_message = str(e)
            return False
    
    def undo(self) -> bool:
        """Undo the drop command."""
        try:
            if self._original_state is None:
                return False
            
            # Restore original state
            success = self.enrollment_service.restore_enrollment_state(
                self.student_id, self.course_id, self._original_state
            )
            
            if success:
                self._status = CommandStatus.CANCELLED
                return True
            else:
                return False
                
        except Exception as e:
            self._error_message = f"Undo failed: {str(e)}"
            return False
    
    def get_description(self) -> str:
        return f"Drop student {self.student_id} from course {self.course_id}"


class SubmitGradeCommand(Command):
    """
    Command for submitting grades for a course.
    """
    
    def __init__(self, course_id: str, grade_submissions: List[Dict[str, Any]], grade_service):
        super().__init__()
        self.course_id = course_id
        self.grade_submissions = grade_submissions
        self.grade_service = grade_service
        self._original_grades = None
    
    def execute(self) -> bool:
        """Execute the grade submission command."""
        try:
            self._status = CommandStatus.EXECUTING
            self._timestamp = datetime.now()
            
            # Store original grades for potential undo
            self._original_grades = {}
            for submission in self.grade_submissions:
                student_id = submission['student_id']
                original_grade = self.grade_service.get_student_grade(self.course_id, student_id)
                self._original_grades[student_id] = original_grade
            
            # Submit grades
            success = self.grade_service.submit_grades(self.course_id, self.grade_submissions)
            
            if success:
                self._status = CommandStatus.COMPLETED
                return True
            else:
                self._status = CommandStatus.FAILED
                self._error_message = "Grade submission failed"
                return False
                
        except Exception as e:
            self._status = CommandStatus.FAILED
            self._error_message = str(e)
            return False
    
    def undo(self) -> bool:
        """Undo the grade submission command."""
        try:
            if self._original_grades is None:
                return False
            
            # Restore original grades
            success = self.grade_service.restore_grades(self.course_id, self._original_grades)
            
            if success:
                self._status = CommandStatus.CANCELLED
                return True
            else:
                return False
                
        except Exception as e:
            self._error_message = f"Undo failed: {str(e)}"
            return False
    
    def get_description(self) -> str:
        return f"Submit grades for course {self.course_id} ({len(self.grade_submissions)} students)"


class CommandInvoker:
    """
    Invoker class that executes commands and maintains command history.
    """
    
    def __init__(self):
        self._command_history: List[Command] = []
        self._current_command: Command = None
    
    def execute_command(self, command: Command) -> bool:
        """Execute a command and add it to history."""
        self._current_command = command
        success = command.execute()
        
        if success:
            self._command_history.append(command)
        
        return success
    
    def undo_last_command(self) -> bool:
        """Undo the last executed command."""
        if not self._command_history:
            return False
        
        last_command = self._command_history[-1]
        success = last_command.undo()
        
        if success:
            self._command_history.remove(last_command)
        
        return success
    
    def get_command_history(self) -> List[Command]:
        """Get the command execution history."""
        return self._command_history.copy()
    
    def get_last_command(self) -> Command:
        """Get the last executed command."""
        return self._command_history[-1] if self._command_history else None
    
    def clear_history(self):
        """Clear the command history."""
        self._command_history.clear()


class CommandQueue:
    """
    Queue for managing multiple commands.
    """
    
    def __init__(self):
        self._commands: List[Command] = []
        self._processing = False
    
    def add_command(self, command: Command):
        """Add a command to the queue."""
        self._commands.append(command)
    
    def process_commands(self, invoker: CommandInvoker) -> List[bool]:
        """Process all commands in the queue."""
        if self._processing:
            return []
        
        self._processing = True
        results = []
        
        try:
            while self._commands:
                command = self._commands.pop(0)
                result = invoker.execute_command(command)
                results.append(result)
                
                # Stop processing if a command fails
                if not result:
                    break
        finally:
            self._processing = False
        
        return results
    
    def get_queue_size(self) -> int:
        """Get the number of commands in the queue."""
        return len(self._commands)
    
    def clear_queue(self):
        """Clear all commands from the queue."""
        self._commands.clear()


class BatchCommand(Command):
    """
    Command that executes multiple commands as a batch.
    """
    
    def __init__(self, commands: List[Command]):
        super().__init__()
        self.commands = commands
        self._executed_commands = []
    
    def execute(self) -> bool:
        """Execute all commands in the batch."""
        try:
            self._status = CommandStatus.EXECUTING
            self._timestamp = datetime.now()
            
            for command in self.commands:
                success = command.execute()
                if success:
                    self._executed_commands.append(command)
                else:
                    # If any command fails, undo all executed commands
                    self._undo_executed_commands()
                    self._status = CommandStatus.FAILED
                    self._error_message = f"Batch execution failed at command: {command.get_description()}"
                    return False
            
            self._status = CommandStatus.COMPLETED
            return True
            
        except Exception as e:
            self._undo_executed_commands()
            self._status = CommandStatus.FAILED
            self._error_message = str(e)
            return False
    
    def undo(self) -> bool:
        """Undo all executed commands in reverse order."""
        try:
            success = True
            for command in reversed(self._executed_commands):
                if not command.undo():
                    success = False
            
            if success:
                self._status = CommandStatus.CANCELLED
            
            return success
            
        except Exception as e:
            self._error_message = f"Batch undo failed: {str(e)}"
            return False
    
    def _undo_executed_commands(self):
        """Undo all executed commands in reverse order."""
        for command in reversed(self._executed_commands):
            try:
                command.undo()
            except:
                pass  # Continue undoing other commands even if one fails
    
    def get_description(self) -> str:
        return f"Batch command with {len(self.commands)} operations"
