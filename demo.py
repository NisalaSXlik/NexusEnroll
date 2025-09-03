"""
Simple demonstration of the NexusEnroll system.
Shows key features and design patterns in action.
"""

from datetime import time
from models.user import Student, Faculty, Administrator, UserType
from models.course import Course, Schedule, DayOfWeek, Prerequisite
from services.enrollment_service import EnrollmentService
from services.grade_service import GradeService
from services.user_service import UserService
from patterns.observer import EmailNotificationObserver, EmailService
from patterns.factory import CourseFactory, UserFactoryProducer
from patterns.strategy import ValidationStrategyFactory


def main():
    """Run a simple demonstration of the system."""
    print("=" * 60)
    print("NEXUSENROLL SYSTEM - SIMPLE DEMONSTRATION")
    print("=" * 60)
    
    # Initialize services
    enrollment_service = EnrollmentService()
    grade_service = GradeService()
    user_service = UserService()
    
    # Setup observer
    email_service = EmailService()
    email_observer = EmailNotificationObserver(email_service)
    enrollment_service.attach(email_observer)
    
    print("\n1. CREATING USERS (Factory Pattern)")
    print("-" * 40)
    
    # Create a student using Factory pattern
    student_data = {
        'user_id': 'DEMO_STU001',
        'name': 'Demo Student',
        'email': 'demo.student@university.edu',
        'major': 'Computer Science',
        'user_type': 'student'
    }
    
    success, student, message = user_service.create_user(student_data)
    if success:
        enrollment_service.register_student(student)
        print(f"[OK] Created student: {student.name} ({student.user_id})")
        print(f"  Major: {student.major}")
        print(f"  Permissions: {len(student.get_permissions())} permissions")
    
    # Create a faculty member
    faculty_data = {
        'user_id': 'DEMO_FAC001',
        'name': 'Demo Faculty',
        'email': 'demo.faculty@university.edu',
        'department': 'Computer Science',
        'user_type': 'faculty'
    }
    
    success, faculty, message = user_service.create_user(faculty_data)
    if success:
        print(f"[OK] Created faculty: {faculty.name} ({faculty.user_id})")
        print(f"  Department: {faculty.department}")
    
    print("\n2. CREATING COURSES (Factory Pattern)")
    print("-" * 40)
    
    # Create a course using Factory pattern
    course_data = {
        'course_id': 'DEMO_CS101',
        'name': 'Demo Programming Course',
        'description': 'A demonstration course for programming',
        'department': 'Computer Science',
        'credits': 3,
        'instructor_id': 'DEMO_FAC001',
        'capacity': 30,
        'schedule': {
            'days': ['Monday', 'Wednesday', 'Friday'],
            'start_time': '10:00',
            'end_time': '10:50',
            'location': 'Demo Hall A'
        },
        'prerequisites': []
    }
    
    try:
        course = CourseFactory.create_course(course_data)
        enrollment_service.register_course(course)
        print(f"[OK] Created course: {course.name} ({course.course_id})")
        print(f"  Department: {course.department}")
        print(f"  Credits: {course.credits}")
        print(f"  Capacity: {course.capacity}")
        print(f"  Schedule: {course.schedule}")
    except Exception as e:
        print(f"[ERROR] Failed to create course: {str(e)}")
        return
    
    print("\n3. ENROLLMENT OPERATIONS (Strategy + Command Patterns)")
    print("-" * 50)
    
    # Set validation strategy to basic (no GPA requirement)
    enrollment_service.set_validation_strategy("basic")
    
    # Test enrollment
    print(f"Attempting to enroll {student.name} in {course.name}...")
    success = enrollment_service.enroll_student('DEMO_STU001', 'DEMO_CS101')
    print(f"Enrollment result: {'[SUCCESS]' if success else '[FAILED]'}")
    
    if success:
        # Show student schedule
        schedule = enrollment_service.get_student_schedule('DEMO_STU001')
        print(f"\nStudent Schedule ({len(schedule)} courses):")
        for course_info in schedule:
            print(f"  • {course_info['name']} ({course_info['course_id']})")
            print(f"    Schedule: {course_info['schedule']}")
        
        # Show course roster
        roster = enrollment_service.get_course_roster('DEMO_CS101')
        print(f"\nCourse Roster ({len(roster)} students):")
        for student_info in roster:
            print(f"  • {student_info['name']} ({student_info['student_id']})")
    
    print("\n4. COMMAND PATTERN DEMONSTRATION")
    print("-" * 35)
    
    # Execute enrollment command
    print("Executing enrollment command...")
    success = enrollment_service.execute_enrollment_command("enroll", 'DEMO_STU001', 'DEMO_CS101')
    print(f"Command execution: {'[SUCCESS]' if success else '[FAILED]'}")
    
    # Show command history
    history = enrollment_service.get_enrollment_history()
    print(f"\nCommand History ({len(history)} commands):")
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd}")
    
    # Test undo functionality
    if history:
        print(f"\nTesting undo functionality...")
        undo_success = enrollment_service.undo_last_enrollment()
        print(f"Undo operation: {'[SUCCESS]' if undo_success else '[FAILED]'}")
    
    print("\n5. GRADE OPERATIONS (Observer Pattern)")
    print("-" * 40)
    
    # Submit grades
    grade_submissions = [
        {'student_id': 'DEMO_STU001', 'grade': 'A', 'credits': 3}
    ]
    
    print("Submitting grades...")
    success = grade_service.submit_grades('DEMO_CS101', grade_submissions)
    print(f"Grade submission: {'[SUCCESS]' if success else '[FAILED]'}")
    
    if success:
        # Show grade statistics
        stats = grade_service.get_grade_statistics('DEMO_CS101')
        print(f"\nGrade Statistics:")
        print(f"  Total students: {stats.get('total_students', 0)}")
        print(f"  Grade distribution: {stats.get('grade_distribution', {})}")
    
    print("\n6. SYSTEM STATISTICS")
    print("-" * 20)
    
    # Enrollment statistics
    enrollment_stats = enrollment_service.get_enrollment_statistics()
    print(f"Enrollment Statistics:")
    print(f"  Total students: {enrollment_stats['total_students']}")
    print(f"  Total courses: {enrollment_stats['total_courses']}")
    print(f"  Total enrollments: {enrollment_stats['total_enrollments']}")
    
    # User statistics
    user_stats = user_service.get_user_statistics()
    print(f"\nUser Statistics:")
    print(f"  Total users: {user_stats['total_users']}")
    print(f"  Active users: {user_stats['active_users']}")
    print(f"  User types: {user_stats['user_type_distribution']}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nThis demonstration showcased:")
    print("[OK] Factory Method Pattern - User and Course creation")
    print("[OK] Strategy Pattern - Validation strategies")
    print("[OK] Command Pattern - Enrollment operations with undo")
    print("[OK] Observer Pattern - Notification system")
    print("[OK] 3-Tier Architecture - Service layer implementation")
    print("[OK] SOLID Principles - Clean, maintainable code")
    print("[OK] Comprehensive business logic - Real-world functionality")


if __name__ == "__main__":
    main()
