"""
NexusEnroll - University Course Enrollment System
Main application demonstrating the 3-Tier Architecture and Design Patterns

This is the main entry point for the NexusEnroll system demonstration.
It showcases the implementation of various design patterns and architectural principles.
"""

from datetime import time
from models.user import Student, Faculty, Administrator, UserType
from models.course import Course, Schedule, DayOfWeek, Prerequisite
from services.enrollment_service import EnrollmentService
from services.grade_service import GradeService
from services.user_service import UserService
from patterns.observer import EmailNotificationObserver, AdvisorNotificationObserver, SystemLogObserver, EmailService, AdvisorService, Logger
from patterns.factory import CourseFactory, UserFactoryProducer
from patterns.strategy import ValidationContext, ValidationStrategyFactory
from patterns.command import CommandInvoker, EnrollStudentCommand, DropStudentCommand


def setup_system():
    """Initialize the system with sample data and observers."""
    print("=" * 60)
    print("NEXUSENROLL - University Course Enrollment System")
    print("Software Architecture Assignment - SCS 2303")
    print("=" * 60)
    
    # Initialize services
    enrollment_service = EnrollmentService()
    grade_service = GradeService()
    user_service = UserService()
    
    # Setup observers (Observer Pattern)
    email_service = EmailService()
    advisor_service = AdvisorService()
    logger = Logger()
    
    email_observer = EmailNotificationObserver(email_service)
    advisor_observer = AdvisorNotificationObserver(advisor_service)
    log_observer = SystemLogObserver(logger)
    
    # Attach observers to services
    enrollment_service.attach(email_observer)
    enrollment_service.attach(log_observer)
    grade_service.attach(email_observer)
    grade_service.attach(log_observer)
    user_service.attach(log_observer)
    
    return enrollment_service, grade_service, user_service


def create_sample_data(enrollment_service, grade_service, user_service):
    """Create sample users and courses for demonstration."""
    print("\n1. CREATING SAMPLE DATA")
    print("-" * 30)
    
    # Create sample students using Factory Pattern
    students_data = [
        {
            'user_id': 'STU001',
            'name': 'Alice Johnson',
            'email': 'alice.johnson@university.edu',
            'major': 'Computer Science',
            'advisor_id': 'FAC001'
        },
        {
            'user_id': 'STU002',
            'name': 'Bob Smith',
            'email': 'bob.smith@university.edu',
            'major': 'Mathematics',
            'advisor_id': 'FAC002'
        },
        {
            'user_id': 'STU003',
            'name': 'Carol Davis',
            'email': 'carol.davis@university.edu',
            'major': 'Computer Science',
            'advisor_id': 'FAC001'
        }
    ]
    
    for student_data in students_data:
        success, user, message = user_service.create_user({
            **student_data,
            'user_type': 'student'
        })
        if success:
            enrollment_service.register_student(user)
            print(f"✓ Created student: {user.name} ({user.user_id})")
        else:
            print(f"✗ Failed to create student: {message}")
    
    # Create sample faculty
    faculty_data = [
        {
            'user_id': 'FAC001',
            'name': 'Dr. Sarah Wilson',
            'email': 'sarah.wilson@university.edu',
            'department': 'Computer Science'
        },
        {
            'user_id': 'FAC002',
            'name': 'Dr. Michael Brown',
            'email': 'michael.brown@university.edu',
            'department': 'Mathematics'
        }
    ]
    
    for faculty_data in faculty_data:
        success, user, message = user_service.create_user({
            **faculty_data,
            'user_type': 'faculty'
        })
        if success:
            print(f"✓ Created faculty: {user.name} ({user.user_id})")
        else:
            print(f"✗ Failed to create faculty: {message}")
    
    # Create sample administrator
    admin_data = {
        'user_id': 'ADM001',
        'name': 'Dr. Jennifer Lee',
        'email': 'jennifer.lee@university.edu',
        'department': 'Administration',
        'admin_level': 'senior'
    }
    
    success, user, message = user_service.create_user({
        **admin_data,
        'user_type': 'administrator'
    })
    if success:
        print(f"✓ Created administrator: {user.name} ({user.user_id})")
    else:
        print(f"✗ Failed to create administrator: {message}")
    
    # Create sample courses using Factory Pattern
    courses_data = [
        {
            'course_id': 'CS101',
            'name': 'Introduction to Programming',
            'description': 'Basic programming concepts and problem solving',
            'department': 'Computer Science',
            'credits': 3,
            'instructor_id': 'FAC001',
            'capacity': 30,
            'schedule': {
                'days': ['Monday', 'Wednesday', 'Friday'],
                'start_time': '10:00',
                'end_time': '10:50',
                'location': 'Lecture Hall A'
            },
            'prerequisites': []
        },
        {
            'course_id': 'CS201',
            'name': 'Data Structures',
            'description': 'Fundamental data structures and algorithms',
            'department': 'Computer Science',
            'credits': 3,
            'instructor_id': 'FAC001',
            'capacity': 25,
            'schedule': {
                'days': ['Tuesday', 'Thursday'],
                'start_time': '14:00',
                'end_time': '15:30',
                'location': 'Lecture Hall B'
            },
            'prerequisites': [
                {'course_id': 'CS101', 'min_grade': 'C'}
            ]
        },
        {
            'course_id': 'MATH101',
            'name': 'Calculus I',
            'description': 'Differential and integral calculus',
            'department': 'Mathematics',
            'credits': 4,
            'instructor_id': 'FAC002',
            'capacity': 35,
            'schedule': {
                'days': ['Monday', 'Wednesday', 'Friday'],
                'start_time': '09:00',
                'end_time': '09:50',
                'location': 'Math Building Room 101'
            },
            'prerequisites': []
        }
    ]
    
    for course_data in courses_data:
        try:
            course = CourseFactory.create_course(course_data)
            enrollment_service.register_course(course)
            print(f"✓ Created course: {course.name} ({course.course_id})")
        except Exception as e:
            print(f"✗ Failed to create course: {str(e)}")


def demonstrate_enrollment_operations(enrollment_service, grade_service):
    """Demonstrate enrollment operations using various design patterns."""
    print("\n2. ENROLLMENT OPERATIONS DEMONSTRATION")
    print("-" * 40)
    
    # Demonstrate Strategy Pattern - Different validation strategies
    print("\n2.1 Strategy Pattern - Validation Strategies")
    print("-" * 45)
    
    # Test with standard validation
    print("Testing with STANDARD validation strategy:")
    enrollment_service.set_validation_strategy("standard")
    
    # Enroll Alice in CS101 (should succeed - no prerequisites)
    success = enrollment_service.enroll_student('STU001', 'CS101')
    print(f"Alice enrollment in CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Enroll Bob in CS101 (should succeed - no prerequisites)
    success = enrollment_service.enroll_student('STU002', 'CS101')
    print(f"Bob enrollment in CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Try to enroll Alice in CS201 (should fail - no prerequisite completion)
    success = enrollment_service.enroll_student('STU001', 'CS201')
    print(f"Alice enrollment in CS201: {'✓ Success' if success else '✗ Failed'}")
    
    # Demonstrate Command Pattern - Enrollment commands
    print("\n2.2 Command Pattern - Enrollment Commands")
    print("-" * 45)
    
    # Execute enrollment command
    success = enrollment_service.execute_enrollment_command("enroll", 'STU003', 'CS101')
    print(f"Command: Enroll Carol in CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Execute drop command
    success = enrollment_service.execute_enrollment_command("drop", 'STU002', 'CS101')
    print(f"Command: Drop Bob from CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Show command history
    history = enrollment_service.get_enrollment_history()
    print(f"\nCommand History ({len(history)} commands):")
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd}")
    
    # Demonstrate undo functionality
    print("\nUndoing last command...")
    undo_success = enrollment_service.undo_last_enrollment()
    print(f"Undo operation: {'✓ Success' if undo_success else '✗ Failed'}")
    
    # Show updated history
    history = enrollment_service.get_enrollment_history()
    print(f"Updated Command History ({len(history)} commands):")
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd}")


def demonstrate_grade_operations(grade_service):
    """Demonstrate grade submission operations."""
    print("\n3. GRADE OPERMATIONS DEMONSTRATION")
    print("-" * 35)
    
    # Simulate completing CS101 for Alice and Carol
    print("\n3.1 Simulating Course Completion")
    print("-" * 35)
    
    # Get students and update their records
    alice = grade_service.get_student_by_id('STU001') if hasattr(grade_service, 'get_student_by_id') else None
    carol = grade_service.get_student_by_id('STU003') if hasattr(grade_service, 'get_student_by_id') else None
    
    # Submit grades for CS101
    grade_submissions = [
        {'student_id': 'STU001', 'grade': 'A', 'credits': 3},
        {'student_id': 'STU003', 'grade': 'B+', 'credits': 3}
    ]
    
    success = grade_service.submit_grades('CS101', grade_submissions)
    print(f"Grade submission for CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Show grade statistics
    stats = grade_service.get_grade_statistics('CS101')
    print(f"\nGrade Statistics for CS101:")
    print(f"  Total students: {stats.get('total_students', 0)}")
    print(f"  Grade distribution: {stats.get('grade_distribution', {})}")
    
    # Demonstrate Command Pattern for grade submission
    print("\n3.2 Command Pattern - Grade Submission")
    print("-" * 40)
    
    # Execute grade command
    success = grade_service.execute_grade_command('CS101', grade_submissions)
    print(f"Command: Submit grades for CS101: {'✓ Success' if success else '✗ Failed'}")
    
    # Show command history
    history = grade_service.get_grade_submission_history()
    print(f"\nGrade Command History ({len(history)} commands):")
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd}")


def demonstrate_system_features(enrollment_service, grade_service, user_service):
    """Demonstrate various system features and reporting."""
    print("\n4. SYSTEM FEATURES DEMONSTRATION")
    print("-" * 35)
    
    # Show student schedules
    print("\n4.1 Student Schedules")
    print("-" * 20)
    
    for student_id in ['STU001', 'STU002', 'STU003']:
        schedule = enrollment_service.get_student_schedule(student_id)
        student = user_service.get_user_by_id(student_id)
        if student:
            print(f"\n{student.name}'s Schedule:")
            if schedule:
                for course in schedule:
                    print(f"  • {course['name']} ({course['course_id']}) - {course['schedule']}")
            else:
                print("  No courses enrolled")
    
    # Show course rosters
    print("\n4.2 Course Rosters")
    print("-" * 18)
    
    for course_id in ['CS101', 'CS201', 'MATH101']:
        roster = enrollment_service.get_course_roster(course_id)
        course = enrollment_service.get_course_by_id(course_id)
        if course:
            print(f"\n{course.name} ({course_id}) Roster:")
            if roster:
                for student in roster:
                    print(f"  • {student['name']} ({student['student_id']}) - {student['major']}")
            else:
                print("  No students enrolled")
    
    # Show system statistics
    print("\n4.3 System Statistics")
    print("-" * 20)
    
    # Enrollment statistics
    enrollment_stats = enrollment_service.get_enrollment_statistics()
    print(f"Enrollment Statistics:")
    print(f"  Total students: {enrollment_stats['total_students']}")
    print(f"  Total courses: {enrollment_stats['total_courses']}")
    print(f"  Total enrollments: {enrollment_stats['total_enrollments']}")
    print(f"  Average enrollments per student: {enrollment_stats['average_enrollments_per_student']:.2f}")
    
    # User statistics
    user_stats = user_service.get_user_statistics()
    print(f"\nUser Statistics:")
    print(f"  Total users: {user_stats['total_users']}")
    print(f"  Active users: {user_stats['active_users']}")
    print(f"  User type distribution: {user_stats['user_type_distribution']}")
    
    # Course utilization
    print(f"\nCourse Utilization:")
    for course_id, util in enrollment_stats['course_utilization'].items():
        print(f"  {util['name']}: {util['enrolled']}/{util['capacity']} ({util['utilization']:.1%})")


def demonstrate_design_principles():
    """Demonstrate adherence to software design principles."""
    print("\n5. SOFTWARE DESIGN PRINCIPLES DEMONSTRATION")
    print("-" * 50)
    
    print("\n5.1 SOLID Principles")
    print("-" * 20)
    
    print("✓ Single Responsibility Principle:")
    print("  - User class handles only user-related operations")
    print("  - Course class handles only course-related operations")
    print("  - Services handle specific business logic domains")
    
    print("\n✓ Open/Closed Principle:")
    print("  - Validation strategies can be extended without modifying existing code")
    print("  - New user types can be added by extending the User base class")
    print("  - New observers can be added without changing the Subject class")
    
    print("\n✓ Liskov Substitution Principle:")
    print("  - All user types (Student, Faculty, Administrator) can be used interchangeably")
    print("  - All validation strategies can be substituted for each other")
    print("  - All commands can be executed through the same interface")
    
    print("\n✓ Interface Segregation Principle:")
    print("  - Observer interface is minimal and focused")
    print("  - Command interface contains only necessary methods")
    print("  - Validation strategy interface is simple and specific")
    
    print("\n✓ Dependency Inversion Principle:")
    print("  - Services depend on abstractions (Observer, Command, Strategy)")
    print("  - High-level modules don't depend on low-level modules")
    print("  - Dependencies are injected through constructors")
    
    print("\n5.2 Other Design Principles")
    print("-" * 30)
    
    print("✓ DRY (Don't Repeat Yourself):")
    print("  - Common validation logic is centralized in strategies")
    print("  - User creation logic is centralized in factories")
    print("  - Notification logic is centralized in observers")
    
    print("\n✓ KISS (Keep It Simple, Stupid):")
    print("  - Simple, clear class interfaces")
    print("  - Minimal dependencies between components")
    print("  - Straightforward method implementations")
    
    print("\n✓ Composition over Inheritance:")
    print("  - Validation context composes validation strategies")
    print("  - Command invoker composes commands")
    print("  - Services compose multiple observers")


def main():
    """Main function to run the NexusEnroll system demonstration."""
    try:
        # Setup the system
        enrollment_service, grade_service, user_service = setup_system()
        
        # Create sample data
        create_sample_data(enrollment_service, grade_service, user_service)
        
        # Demonstrate enrollment operations
        demonstrate_enrollment_operations(enrollment_service, grade_service)
        
        # Demonstrate grade operations
        demonstrate_grade_operations(grade_service)
        
        # Demonstrate system features
        demonstrate_system_features(enrollment_service, grade_service, user_service)
        
        # Demonstrate design principles
        demonstrate_design_principles()
        
        print("\n" + "=" * 60)
        print("NEXUSENROLL SYSTEM DEMONSTRATION COMPLETED")
        print("=" * 60)
        print("\nThis demonstration showcased:")
        print("• 3-Tier Architecture implementation")
        print("• Observer Pattern for notifications")
        print("• Factory Method Pattern for object creation")
        print("• Strategy Pattern for validation")
        print("• Command Pattern for operations")
        print("• SOLID principles adherence")
        print("• Comprehensive business logic implementation")
        
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
