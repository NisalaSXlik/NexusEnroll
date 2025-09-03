#!/usr/bin/env python3
"""
Simple Assignment Test Runner
This script provides a quick way to test all assignment components.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test core models
        from models.user import User, Student, Faculty, Administrator
        from models.course import Course, Schedule
        print("[OK] Models imported successfully")
        
        # Test design patterns
        from patterns.observer import Subject, Observer, EmailNotificationObserver
        from patterns.factory import UserFactory, StudentFactory, CourseFactory
        from patterns.strategy import ValidationStrategy, PrerequisiteValidationStrategy
        from patterns.command import Command, EnrollStudentCommand, CommandInvoker
        print("[OK] Design patterns imported successfully")
        
        # Test services
        from services.enrollment_service import EnrollmentService
        from services.grade_service import GradeService
        from services.user_service import UserService
        print("[OK] Services imported successfully")
        
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic system functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from models.user import Student, Faculty
        from models.course import Course
        from services.enrollment_service import EnrollmentService
        
        # Create test objects
        student = Student("S001", "John Doe", "john@university.edu", "Computer Science")
        faculty = Faculty("F001", "Dr. Smith", "smith@university.edu", "Computer Science")
        
        # Create a simple course with required parameters
        from models.course import Schedule, DayOfWeek
        from datetime import time
        schedule = Schedule([DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY], time(10, 0), time(11, 0), "Room 101")
        course = Course("CS101", "Introduction to Programming", "Basic programming course", 
                       "Computer Science", 3, "F001", 30, schedule)
        
        print("[OK] Objects created successfully")
        
        # Test enrollment service
        enrollment_service = EnrollmentService()
        print("[OK] Enrollment service created")
        
        return True
    except Exception as e:
        print(f"[ERROR] Functionality error: {e}")
        return False

def test_design_patterns():
    """Test design pattern implementations."""
    print("\nTesting design patterns...")
    
    try:
        # Test Factory Pattern
        from patterns.factory import StudentFactory, CourseFactory
        student_factory = StudentFactory()
        student_data = {
            'user_id': 'S001',
            'name': 'John Doe',
            'email': 'john@university.edu',
            'major': 'Computer Science'
        }
        student = student_factory.create_user(student_data)
        print("[OK] Factory pattern working")
        
        # Test Strategy Pattern
        from patterns.strategy import PrerequisiteValidationStrategy, CapacityValidationStrategy
        prereq_validator = PrerequisiteValidationStrategy()
        capacity_validator = CapacityValidationStrategy()
        print("[OK] Strategy pattern working")
        
        # Test Observer Pattern
        from patterns.observer import EmailNotificationObserver, EmailService
        email_service = EmailService()
        observer = EmailNotificationObserver(email_service)
        print("[OK] Observer pattern working")
        
        # Test Command Pattern
        from patterns.command import EnrollStudentCommand, CommandInvoker
        command_invoker = CommandInvoker()
        print("[OK] Command pattern working")
        
        return True
    except Exception as e:
        print(f"[ERROR] Design pattern error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nChecking file structure...")
    
    required_files = [
        "main.py", "demo.py", "README.md", "requirements.txt",
        "models/user.py", "models/course.py",
        "patterns/observer.py", "patterns/factory.py", 
        "patterns/strategy.py", "patterns/command.py",
        "services/enrollment_service.py", "services/grade_service.py", "services/user_service.py",
        "tests/test_enrollment.py",
        "docs/architecture_analysis.md", "docs/design_patterns_analysis.md", "docs/uml_diagrams.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"[OK] {file_path}")
    
    if missing_files:
        print(f"[ERROR] Missing files: {missing_files}")
        return False
    
    return True

def run_demo():
    """Run the demo script."""
    print("\nRunning demo...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("[OK] Demo ran successfully")
            print("Demo output:")
            print(result.stdout)
            return True
        else:
            print(f"[ERROR] Demo failed with exit code: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Demo error: {e}")
        return False

def main():
    """Main test function."""
    print("Testing NexusEnroll Assignment")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Design Patterns", test_design_patterns),
        ("Demo Execution", run_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"[ERROR] {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED! Assignment is ready for submission.")
        return 0
    else:
        print(f"[WARNING] {total - passed} tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
