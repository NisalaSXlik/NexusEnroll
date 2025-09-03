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
    # Streamlined PoC demo in assignment brief order
    print_header("NexusEnroll Demo Start")

    # 1. Course creation and catalogue browsing
    print_header("Course Creation and Catalogue Browsing")
    from core.catalogue import ConcreteCourseFactory, CourseCatalogue
    factory = ConcreteCourseFactory()
    catalogue = CourseCatalogue()
    cs101 = factory.create_course("Lecture", course_id="CS101", name="Intro to CS", instructor="Prof. Smith", capacity=2, prerequisites=[], schedule="Mon 9am")
    cs102 = factory.create_course("Lab", course_id="CS102", name="Data Structures Lab", instructor="Prof. Lee", capacity=1, prerequisites=["CS101"], schedule="Wed 10am", lab_room="Lab1")
    catalogue.add_course(cs101)
    catalogue.add_course(cs102)
    print("All courses:")
    for c in catalogue.list_courses():
        print(f"- {c}")
    print("Search by instructor='Prof. Smith':")
    for c in catalogue.search_courses(instructor="Prof. Smith"):
        print(f"- {c}")

    # 2. Student registration/enrolment, schedule, progress
    print_header("Student Registration, Enrolment, Schedule, Progress")
    from schedule.schedule import ScheduleObserver, Schedule
    alice = Student("Alice")
    bob = Student("Bob")
    alice.schedule_observer = ScheduleObserver()
    bob.schedule_observer = ScheduleObserver()
    from enrolment.validation_strategies import PrerequisiteValidation, CapacityValidation, ScheduleConflictValidation
    from enrolment.enrolment_service import EnrolmentService
    strategies = [PrerequisiteValidation(), CapacityValidation(), ScheduleConflictValidation()]
    enrol_service = EnrolmentService(strategies)
    result = enrol_service.enrol(alice, cs101)
    if result:
        alice.enrolled_courses.append(cs101)
        Schedule(alice).add_course(cs101)
        print(f"{alice.name} enrolled in {cs101.name}")
    else:
        print(f"{alice.name} could not enrol in {cs101.name}")
    result = enrol_service.enrol(bob, cs101)
    if result:
        bob.enrolled_courses.append(cs101)
        Schedule(bob).add_course(cs101)
        print(f"{bob.name} enrolled in {cs101.name}")
    else:
        print(f"{bob.name} could not enrol in {cs101.name}")
    alice.completed_courses.append("CS101")
    result = enrol_service.enrol(alice, cs102)
    if result:
        alice.enrolled_courses.append(cs102)
        Schedule(alice).add_course(cs102)
        print(f"{alice.name} enrolled in {cs102.name}")
    else:
        print(f"{alice.name} could not enrol in {cs102.name}")
    from schedule.progress_tracker import ProgressTracker
    tracker = ProgressTracker()
    tracker.add_completed(cs101, "A")
    print(f"Completed: {tracker.get_completed_courses()}")

    # 3. Faculty roster viewing, grade submission
    print_header("Faculty Roster Viewing and Grade Submission")
    from faculty.roster import RosterFacade
    RosterFacade(cs101).view_roster()
    from faculty.grades import Grade, SubmitGradeCommand
    grade1 = Grade(alice, cs101, "A")
    grade2 = Grade(bob, cs101, "B")
    cmd1 = SubmitGradeCommand(grade1)
    cmd2 = SubmitGradeCommand(grade2)
    cmd1.execute()
    cmd2.execute()

    # 4. Admin program management, reporting, override
    print_header("Admin Program Management, Reporting, Override")
    from admin.builder import ConcreteProgramBuilder, ProgramDirector
    builder = ConcreteProgramBuilder()
    director = ProgramDirector(builder)
    program = director.construct("BSc CS", [cs101], [cs102])
    print(f"Program: {program.name}, Required: {program.required_courses}, Electives: {program.electives}")
    from admin.reports import EnrollmentReport
    from admin.adapters import CSVAdapter
    report = EnrollmentReport().generate()
    csv = CSVAdapter().convert(report)
    print(f"CSV Report: {csv}")
    from admin.management import AdminManager
    admin_mgr = AdminManager()
    override_result = admin_mgr.override_enrolment(enrol_service, alice, cs102)
    print(f"Admin override enrolment result: {override_result}")
    # Now that a program exists, show remaining courses for tracker
    print(f"Remaining: {tracker.remaining_courses(program)}")

    # 5. System-wide requirements (notifications, transaction)
    print_header("System-wide Notifications and Transaction Management")
    from shared.notifications import NotificationService, StudentNotifier
    notif_service = NotificationService()
    student_notifier = StudentNotifier()
    notif_service.subscribe(student_notifier)
    notif_service.notify("course_dropped", f"{alice.name} dropped {cs101.name}")
    from shared.transactions import EnrolmentTransaction
    tx = EnrolmentTransaction(enrol_service, alice, cs101)
    tx.execute()

    print_header("NexusEnroll Demo End")