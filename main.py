# Placeholder imports for demo (actual implementations to be added later)
# from course_factory import CourseFactory
# from student import Student
# from faculty import Faculty
# from admin import Admin
# from enrollment_command import EnrollCommand, DropCommand
# from enrollment_strategy import EnrollmentStrategy
# from observer import ScheduleObserver
# from grade_state import GradeSubmissionState
# from program_builder import ProgramBuilder
# from report_template import ReportTemplate
# from report_adapter import ReportAdapter

# --- Assignment alignment notes ---
# Architecture: 3-Tier Architecture (client/demo -> business/domain services -> data/integration stubs)
# This script is a runnable business-tier proof-of-concept (no UI) to satisfy Part B.
# Design patterns covered and where:
# - Factory Method: core.catalogue.ConcreteCourseFactory
# - Strategy: enrolment.validation_strategies.* used by EnrolmentService
# - Command: enrolment operations and faculty grade submission (SubmitGradeCommand)
# - Observer: schedule.ScheduleObserver; shared.notifications.* for system-wide notifications
# - State: schedule.course_state.CourseContext; faculty.grades.Grade state
# - Builder: admin.builder.* for program construction
# - Template Method: admin.reports.EnrollmentReport
# - Adapter: admin.adapters.CSVAdapter
# - Facade + Iterator: faculty.roster.RosterFacade
# - Chain of Responsibility + Decorator: faculty.course_requests pipeline + LoggingDecorator
# - Singleton: admin.management.AdminManager
# - Transaction: shared.transactions.EnrolmentTransaction
# Core features covered:
# - Student: catalogue browse, enrol/drop with validation, schedule, progress
# - Faculty: roster viewing, grade submission with state
# - Admin: program build, override enrolment, reports
# System-wide: notifications, transactional enrolment


# Helper to print section headers
def print_header(title):
    print("\n" + "="*10 + f" {title} " + "="*10)


# Simple Student entity for demo
class Student:
    def __init__(self, name):
        self.name = name
        self.completed_courses = []
        self.enrolled_courses = []
        self.schedule_observer = None

    def __str__(self):
        return f"Student({self.name})"

# --- Lightweight helpers for assignment report/demo ---
def print_assignment_alignment():
    print_header("Assignment Alignment Overview")
    print("- Architecture: 3-Tier Architecture (client/demo -> business/domain -> data/integration).")
    print("- Focus: Business-tier proof-of-concept; UI is optional per brief.")
    print("- Core modules demonstrated: Student, Faculty, Administrator.")
    print("- Patterns showcased:")
    print("  * Factory Method, Strategy, Command, Observer, State, Builder, Template Method, Adapter,")
    print("    Facade, Iterator, Chain of Responsibility, Decorator, Singleton, Transaction.")
    print("- System-wide requirements demonstrated: Notifications, Transaction management.")
    print("- Robustness: Validation strategies, transactional enrolment, and explicit state transitions.")

def verify_required_modules():
    import importlib
    print_header("Assignment Self-Check (Module Readiness)")
    modules = [
        "core.catalogue",
        "enrolment.validation_strategies",
        "enrolment.enrolment_service",
        "schedule.schedule",
        "faculty.grades",
        "admin.builder",
        "admin.reports",
        "admin.adapters",
        "schedule.progress_tracker",
        "schedule.course_state",
        "faculty.roster",
        "faculty.course_requests",
        "admin.management",
        "shared.notifications",
        "shared.transactions",
    ]
    ok = True
    for m in modules:
        try:
            importlib.import_module(m)
            print(f"[OK] {m}")
        except Exception as e:
            ok = False
            print(f"[MISSING] {m} -> {e}")
    if ok:
        print("All referenced modules import successfully. Demo is ready for recording/reporting.")
    else:
        print("One or more modules missing. Complete/adjust imports before submission.")

if __name__ == "__main__":
    print_header("NexusEnroll Demo Start")
    print_assignment_alignment()

    # 1. Create courses via Factory Method
    # Pattern: Factory Method (creational)
    # Used to instantiate different course types (Lecture, Lab) with flexible attributes.
    print_header("Course Creation (Factory Method)")
    from core.catalogue import ConcreteCourseFactory
    course_factory = ConcreteCourseFactory()
    course_math = course_factory.create_course("Lecture", course_id="M101", name="Math 101", instructor="Dr. Euler", capacity=30, department="Mathematics", description="Introductory mathematics.")
    course_cs = course_factory.create_course("Lab", course_id="CS201", name="CS 201", instructor="Dr. Turing", capacity=20, lab_room="Lab 1", department="Computer Science", description="Intro to programming lab.")
    print(f"Created: {course_math}, {course_cs}")

    # Add to catalogue for search demo
    # Demonstrates catalogue search filters (department, instructor, keyword)
    from core.catalogue import CourseCatalogue
    catalogue = CourseCatalogue()
    catalogue.add_course(course_math)
    catalogue.add_course(course_cs)

    print_header("Catalogue Search Filters Demo")
    print("Search by department='Computer Science':")
    for c in catalogue.search_courses(department="Computer Science"):
        print(f"- {c}")
    print("Search by instructor='Dr. Euler':")
    for c in catalogue.search_courses(instructor="Dr. Euler"):
        print(f"- {c}")
    print("Search by keyword='math':")
    for c in catalogue.search_courses(keyword="math"):
        print(f"- {c}")

    # 2. Student enrols/drops using Command + Strategy
    # Patterns: Strategy (validation rules), Command (enrol/drop encapsulation)
    # Strategy: Pluggable validation rules (capacity, prerequisites, schedule conflict)
    # Command: Encapsulates enrol/drop actions for undo/redo and transaction support.
    # Waitlist and notification demo
    # Course maintains a waitlist; notification service alerts students when promoted.
    print_header("Student Enrollment (Command + Strategy)")
    student = Student("Alice")
    student2 = Student("Bob")
    student3 = Student("Carol")
    from enrolment.validation_strategies import CapacityValidation, PrerequisiteValidation, ScheduleConflictValidation
    from enrolment.enrolment_service import EnrolmentService
    service = EnrolmentService([CapacityValidation(), PrerequisiteValidation(), ScheduleConflictValidation()])
    # Set course capacity to 1 for demo
    course_math._capacity = 1
    # Attach notification service to course
    from shared.notifications import NotificationService, StudentNotifier
    notif_service = NotificationService()
    course_math.notification_service = notif_service
    student_notifier = StudentNotifier()
    notif_service.subscribe(student_notifier)
    # Enrol Alice (should succeed)
    enrolled = service.enrol(student, course_math)
    if enrolled:
        student.enrolled_courses.append(course_math)
    print(f"{student} enrolled in {course_math}")
    # Enrol Bob and Carol (should go to waitlist)
    service.enrol(student2, course_math)
    service.enrol(student3, course_math)
    print(f"Waitlist for {course_math.name}: {[s.name for s in course_math.waitlist]}")
    # Drop Alice (should promote Bob and notify)
    dropped = service.drop(student, course_math)
    if dropped:
        student.enrolled_courses.remove(course_math)
    print(f"{student} dropped {course_math}")
    print(f"Enrolled students after drop: {[s.name for s in course_math.enrolled_students]}")
    print(f"Waitlist after promotion: {[s.name for s in course_math.waitlist]}")

    # 3. Schedule auto-updates (Observer)
    # Pattern: Observer
    # Student's schedule observer receives updates on enrol/drop events.
    print_header("Schedule Auto-Update (Observer)")
    from schedule.schedule import ScheduleObserver
    student.schedule_observer = ScheduleObserver()
    student.enrolled_courses.append(course_cs)
    student.schedule_observer.update("enrolled", student, course_cs)

    # 4. Faculty submits grades (State + Command)
    # Patterns: State (grade lifecycle), Command (submit operation)
    # State: Grade transitions (Draft -> Pending -> Submitted)
    # Command: Encapsulates grade submission for undo/redo and transaction.
    print_header("Faculty Grade Submission (State + Command)")
    from faculty.grades import Grade, SubmitGradeCommand
    faculty = "Dr. Smith"
    grade = Grade(student, course_math, "A")
    submit_cmd = SubmitGradeCommand(grade)
    submit_cmd.execute()
    print(f"{faculty} submitted grade '{grade.grade_value}' for {student} in {course_math}")

    # 5. Admin builds a new program (Builder)
    # Pattern: Builder
    # ProgramDirector orchestrates program construction using builder interface.
    print_header("Admin Program Build (Builder)")
    from admin.builder import ConcreteProgramBuilder, ProgramDirector
    builder = ConcreteProgramBuilder()
    director = ProgramDirector(builder)
    program = director.construct("STEM Program", [course_math], [course_cs])
    print(f"Admin built new program: {program.name}, Required: {program.required_courses}, Electives: {program.electives}")


    # 6. Reports generated (Template + Adapter)
    # Patterns: Template Method (report generation), Adapter (CSV formatting)
    # Template Method: ReportGenerator defines skeleton; EnrollmentReport customizes steps.
    # Adapter: Converts report output to CSV format for export.
    # Admin analytics report for Business school
    # Pattern: Template Method (custom report)
    # Shows filtering and formatting for admin analytics use case.
    print_header("Report Generation (Template + Adapter)")
    from admin.reports import EnrollmentReport, HighCapacityBusinessCoursesReport
    from admin.adapters import CSVAdapter
    report_gen = EnrollmentReport()
    report = report_gen.generate()
    adapter = CSVAdapter()
    formatted_report = adapter.convert(report)
    print(f"Generated report: {formatted_report}")

    # Admin analytics report for Business school
    print_header("Admin Analytics Report: Business Courses >90% Capacity")
    # Add a Business course and fill it for demo
    course_bus = course_factory.create_course("Lecture", course_id="B201", name="Business Analytics", instructor="Dr. Porter", capacity=2, department="Business", description="Business analytics intro.")
    catalogue.add_course(course_bus)
    course_bus.enrol_student(student)
    course_bus.enrol_student(student2)
    highcap_report = HighCapacityBusinessCoursesReport(catalogue)
    print(highcap_report.generate())

    # --- core/course.py demo ---
    # Encapsulation: Course entity hides enrol/drop logic and waitlist management.
    print_header("Course Entity Demo")
    # Use enrol_student instead of manual append
    enrolled = course_math.enrol_student(student)
    print(f"Enrol_student result for {student} in {course_math}: {enrolled}")
    dropped = course_math.drop_student(student)
    print(f"Drop_student result for {student} in {course_math}: {dropped}")

    # --- schedule/progress_tracker.py demo ---
    # ProgressTracker aggregates completed courses and grades for student progress view.
    print_header("Progress Tracker Demo")
    from schedule.progress_tracker import ProgressTracker
    progress_tracker = ProgressTracker()
    progress_tracker.add_completed(course_math, "A")
    print(f"Completed courses: {progress_tracker.get_completed_courses()}")

    # --- schedule/course_state.py demo ---
    # Pattern: State
    # CourseContext transitions through lifecycle states (Planned, Ongoing, Completed, Archived).
    print_header("Course Lifecycle State Demo")
    from schedule.course_state import CourseContext
    lifecycle = CourseContext()
    print(f"Initial state: {lifecycle.get_state_name()}")
    lifecycle.start()
    print(f"After start: {lifecycle.get_state_name()}")
    lifecycle.complete()
    print(f"After complete: {lifecycle.get_state_name()}")
    lifecycle.archive()
    print(f"After archive: {lifecycle.get_state_name()}")

    # --- faculty/roster.py demo ---
    # Patterns: Facade + Iterator
    # RosterFacade provides simplified interface; RosterIterator iterates enrolled students.
    print_header("Faculty Roster Iterator + Facade Demo")
    from faculty.roster import RosterFacade
    # Enrol student in course_cs for roster demo
    course_cs.enrol_student(student)
    roster_facade = RosterFacade(course_cs)
    roster_facade.view_roster()

    # --- faculty/course_requests.py demo ---
    # Patterns: Chain of Responsibility + Decorator
    # Request passes through approval chain; LoggingDecorator logs each step.
    print_header("Faculty Course Requests Chain + Decorator Demo")
    from faculty.course_requests import Request, InstructorHandler, DeptHeadHandler, AdminHandler, LoggingDecorator
    req = Request("dept_head", "Change exam date", "Dr. Smith")
    chain = LoggingDecorator(InstructorHandler())
    chain.set_next(LoggingDecorator(DeptHeadHandler())).set_next(LoggingDecorator(AdminHandler()))
    result = chain.handle(req)
    print(f"Course request handled: {result}")

    # --- admin/management.py demo ---
    # Pattern: Singleton
    # AdminManager ensures single instance for admin operations; override enrolment bypasses validation.
    print_header("AdminManager Singleton Demo")
    from admin.management import AdminManager
    admin_mgr = AdminManager()
    # Show override_enrolment works
    override_result = admin_mgr.override_enrolment(service, student, course_math)
    print(f"Admin override enrolment result: {override_result}")

    # --- shared/notifications.py demo ---
    # Pattern: Observer
    # NotificationService broadcasts events to subscribed notifiers (student, advisor, admin).
    print_header("System-wide Notification Observer Demo")
    from shared.notifications import NotificationService, StudentNotifier
    notif_service = NotificationService()
    student_notifier = StudentNotifier()
    notif_service.subscribe(student_notifier)
    notif_service.notify("course_dropped", f"{student.name} dropped {course_math.name}")

    # --- shared/transactions.py demo ---
    # Transaction management: EnrolmentTransaction ensures atomic enrol/drop operations.
    print_header("Transaction Safety Demo")
    from shared.transactions import EnrolmentTransaction
    # Try enrolling again (should succeed)
    tx = EnrolmentTransaction(service, student, course_math)
    tx.execute()
    # Try enrolling again (should fail and rollback)
    tx_fail = EnrolmentTransaction(service, student, course_math)
    tx_fail.execute()

    verify_required_modules()
    print_header("NexusEnroll Demo End")