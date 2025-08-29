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

def print_header(title):
    print("\n" + "="*10 + f" {title} " + "="*10)

class Student:
    def __init__(self, name):
        self.name = name
        self.completed_courses = []
        self.enrolled_courses = []
        self.schedule_observer = None

    def __str__(self):
        return f"Student({self.name})"

if __name__ == "__main__":
    print_header("NexusEnroll Demo Start")

    # 1. Create courses via FactoryMethod
    print_header("Course Creation (Factory Method)")
    from core.catalogue import ConcreteCourseFactory
    course_factory = ConcreteCourseFactory()
    course_math = course_factory.create_course("Lecture", course_id="M101", name="Math 101", instructor="Dr. Euler", capacity=30)
    course_cs = course_factory.create_course("Lab", course_id="CS201", name="CS 201", instructor="Dr. Turing", capacity=20, lab_room="Lab 1")
    print(f"Created: {course_math}, {course_cs}")

    # 2. Student enrols/drops using Command + Strategy
    print_header("Student Enrollment (Command + Strategy)")
    student = Student("Alice")
    from enrolment.validation_strategies import CapacityValidation, PrerequisiteValidation, ScheduleConflictValidation
    from enrolment.enrolment_service import EnrolmentService
    service = EnrolmentService([CapacityValidation(), PrerequisiteValidation(), ScheduleConflictValidation()])
    enrolled = service.enrol(student, course_math)
    if enrolled:
        student.enrolled_courses.append(course_math)
    print(f"{student} enrolled in {course_math}")
    dropped = service.drop(student, course_math)
    if dropped:
        student.enrolled_courses.remove(course_math)
    print(f"{student} dropped {course_math}")

    # 3. Schedule auto-updates (Observer)
    print_header("Schedule Auto-Update (Observer)")
    from schedule.schedule import ScheduleObserver
    student.schedule_observer = ScheduleObserver()
    student.enrolled_courses.append(course_cs)
    student.schedule_observer.update("enrolled", student, course_cs)

    # 4. Faculty submits grades (State + Command)
    print_header("Faculty Grade Submission (State + Command)")
    from faculty.grades import Grade, SubmitGradeCommand
    faculty = "Dr. Smith"
    grade = Grade(student, course_math, "A")
    submit_cmd = SubmitGradeCommand(grade)
    submit_cmd.execute()
    print(f"{faculty} submitted grade '{grade.grade_value}' for {student} in {course_math}")

    # 5. Admin builds a new program (Builder)
    print_header("Admin Program Build (Builder)")
    from admin.builder import ConcreteProgramBuilder, ProgramDirector
    builder = ConcreteProgramBuilder()
    director = ProgramDirector(builder)
    program = director.construct("STEM Program", [course_math], [course_cs])
    print(f"Admin built new program: {program.name}, Required: {program.required_courses}, Electives: {program.electives}")

    # 6. Reports generated (Template + Adapter)
    print_header("Report Generation (Template + Adapter)")
    from admin.reports import EnrollmentReport
    from admin.adapters import CSVAdapter
    report_gen = EnrollmentReport()
    report = report_gen.generate()
    adapter = CSVAdapter()
    formatted_report = adapter.convert(report)
    print(f"Generated report: {formatted_report}")

    # --- core/course.py demo ---
    print_header("Course Entity Demo")
    # Use enrol_student instead of manual append
    enrolled = course_math.enrol_student(student)
    print(f"Enrol_student result for {student} in {course_math}: {enrolled}")
    dropped = course_math.drop_student(student)
    print(f"Drop_student result for {student} in {course_math}: {dropped}")

    # --- schedule/progress_tracker.py demo ---
    print_header("Progress Tracker Demo")
    from schedule.progress_tracker import ProgressTracker
    progress_tracker = ProgressTracker()
    progress_tracker.add_completed(course_math, "A")
    print(f"Completed courses: {progress_tracker.get_completed_courses()}")

    # --- schedule/course_state.py demo ---
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
    print_header("Faculty Roster Iterator + Facade Demo")
    from faculty.roster import RosterFacade
    # Enrol student in course_cs for roster demo
    course_cs.enrol_student(student)
    roster_facade = RosterFacade(course_cs)
    roster_facade.view_roster()

    # --- faculty/course_requests.py demo ---
    print_header("Faculty Course Requests Chain + Decorator Demo")
    from faculty.course_requests import Request, InstructorHandler, DeptHeadHandler, AdminHandler, LoggingDecorator
    req = Request("dept_head", "Change exam date", "Dr. Smith")
    chain = LoggingDecorator(InstructorHandler())
    chain.set_next(LoggingDecorator(DeptHeadHandler())).set_next(LoggingDecorator(AdminHandler()))
    result = chain.handle(req)
    print(f"Course request handled: {result}")

    # --- admin/management.py demo ---
    print_header("AdminManager Singleton Demo")
    from admin.management import AdminManager
    admin_mgr = AdminManager()
    # Show override_enrolment works
    override_result = admin_mgr.override_enrolment(service, student, course_math)
    print(f"Admin override enrolment result: {override_result}")

    # --- shared/notifications.py demo ---
    print_header("System-wide Notification Observer Demo")
    from shared.notifications import NotificationService, StudentNotifier
    notif_service = NotificationService()
    student_notifier = StudentNotifier()
    notif_service.subscribe(student_notifier)
    notif_service.notify("course_dropped", f"{student.name} dropped {course_math.name}")

    # --- shared/transactions.py demo ---
    print_header("Transaction Safety Demo")
    from shared.transactions import EnrolmentTransaction
    # Try enrolling again (should succeed)
    tx = EnrolmentTransaction(service, student, course_math)
    tx.execute()
    # Try enrolling again (should fail and rollback)
    tx_fail = EnrolmentTransaction(service, student, course_math)
    tx_fail.execute()

    print_header("NexusEnroll Demo End")