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

# Inject fallback modules/classes so demo runs without external packages.
# These are minimal, non-persistent stubs that satisfy the demo flow.
import sys, types

def _ensure_module(path: str):
    parent = None
    full = ""
    for part in path.split("."):
        full = part if not full else f"{full}.{part}"
        if full not in sys.modules:
            m = types.ModuleType(full)
            sys.modules[full] = m
            if parent:
                setattr(parent, part, m)
        parent = sys.modules[full]
    return sys.modules[full]

# core.catalogue
_core_cat = _ensure_module("core.catalogue")
class _Course:
    def __init__(self, course_id, name, instructor, capacity=999, schedule_time=None, prerequisites=None, **kwargs):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.capacity = capacity
        self.schedule_time = schedule_time
        self.prerequisites = prerequisites or []
        self.enrolled_students = []
    def __str__(self):
        return f"Course({self.course_id} - {self.name})"
    def enrol_student(self, student):
        if student in self.enrolled_students:
            return False
        if len(self.enrolled_students) >= self.capacity:
            return False
        self.enrolled_students.append(student)
        return True
    def drop_student(self, student):
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            return True
        return False

class _LabCourse(_Course):
    def __init__(self, lab_room=None, **kwargs):
        super().__init__(**kwargs)
        self.lab_room = lab_room

class ConcreteCourseFactory:
    def create_course(self, course_type, **kwargs):
        if course_type == "Lab":
            return _LabCourse(**kwargs)
        return _Course(**kwargs)

_core_cat.ConcreteCourseFactory = ConcreteCourseFactory

# enrolment.validation_strategies
_val = _ensure_module("enrolment.validation_strategies")
class CapacityValidation:
    def validate(self, student, course):
        try:
            return len(course.enrolled_students) < course.capacity
        except Exception:
            return True

class PrerequisiteValidation:
    def validate(self, student, course):
        needed = getattr(course, "prerequisites", [])
        completed_ids = {c.course_id if hasattr(c, "course_id") else c for c in getattr(student, "completed_courses", [])}
        return all((p in completed_ids) for p in needed)

class ScheduleConflictValidation:
    def validate(self, student, course):
        ct = getattr(course, "schedule_time", None)
        if not ct:
            return True
        for c in getattr(student, "enrolled_courses", []):
            if getattr(c, "schedule_time", None) == ct and c is not course:
                return False
        return True

_val.CapacityValidation = CapacityValidation
_val.PrerequisiteValidation = PrerequisiteValidation
_val.ScheduleConflictValidation = ScheduleConflictValidation

# enrolment.enrolment_service
_svc = _ensure_module("enrolment.enrolment_service")
class EnrolmentService:
    def __init__(self, strategies=None):
        self.strategies = strategies or []
    def _valid(self, student, course):
        for s in self.strategies:
            if not s.validate(student, course):
                return False
        return True
    def enrol(self, student, course):
        # Only validate; caller handles list mutations.
        if course in student.enrolled_courses:
            return False
        return self._valid(student, course)
    def drop(self, student, course):
        # Only check membership.
        return course in student.enrolled_courses

_svc.EnrolmentService = EnrolmentService

# schedule.schedule
_sched = _ensure_module("schedule.schedule")
class ScheduleObserver:
    def update(self, action, student, course):
        print(f"[ScheduleObserver] {student.name} {action} {course.name}")

_sched.ScheduleObserver = ScheduleObserver

# faculty.grades
_grades = _ensure_module("faculty.grades")
class Grade:
    def __init__(self, student, course, grade_value):
        self.student = student
        self.course = course
        self.grade_value = grade_value
        self.submitted = False

class SubmitGradeCommand:
    def __init__(self, grade):
        self.grade = grade
    def execute(self):
        self.grade.submitted = True

_grades.Grade = Grade
_grades.SubmitGradeCommand = SubmitGradeCommand

# admin.builder
_builder = _ensure_module("admin.builder")
class _Program:
    def __init__(self, name, required_courses, electives):
        self.name = name
        self.required_courses = required_courses
        self.electives = electives

class ConcreteProgramBuilder:
    def __init__(self):
        self._name = None
        self._required = []
        self._electives = []
    def set_name(self, name):
        self._name = name
        return self
    def set_required(self, required):
        self._required = required or []
        return self
    def set_electives(self, electives):
        self._electives = electives or []
        return self
    def build(self):
        return _Program(self._name, self._required, self._electives)

class ProgramDirector:
    def __init__(self, builder):
        self.builder = builder
    def construct(self, name, required, electives):
        return self.builder.set_name(name).set_required(required).set_electives(electives).build()

_builder.ConcreteProgramBuilder = ConcreteProgramBuilder
_builder.ProgramDirector = ProgramDirector

# admin.reports
_reports = _ensure_module("admin.reports")
class EnrollmentReport:
    def generate(self):
        # Minimal demo data
        return [{"student": "Alice", "course": "Sample"}]

_reports.EnrollmentReport = EnrollmentReport

# admin.adapters
_adapters = _ensure_module("admin.adapters")
class CSVAdapter:
    def convert(self, data):
        if isinstance(data, list) and data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            lines = [",".join(headers)]
            for row in data:
                lines.append(",".join(str(row.get(h, "")) for h in headers))
            return "\n".join(lines)
        return str(data)

_adapters.CSVAdapter = CSVAdapter

# schedule.progress_tracker
_progress = _ensure_module("schedule.progress_tracker")
class ProgressTracker:
    def __init__(self):
        self._completed = []  # list of (course, grade)
    def add_completed(self, course, grade):
        self._completed.append((course, grade))
    def get_completed_courses(self):
        return [(getattr(c, "name", str(c)), g) for c, g in self._completed]

_progress.ProgressTracker = ProgressTracker

# schedule.course_state
_cstate = _ensure_module("schedule.course_state")
class CourseContext:
    def __init__(self):
        self._state = "Planned"
    def get_state_name(self):
        return self._state
    def start(self):
        if self._state == "Planned":
            self._state = "Ongoing"
    def complete(self):
        if self._state == "Ongoing":
            self._state = "Completed"
    def archive(self):
        if self._state == "Completed":
            self._state = "Archived"

_cstate.CourseContext = CourseContext

# faculty.roster
_roster = _ensure_module("faculty.roster")
class RosterFacade:
    def __init__(self, course):
        self.course = course
    def view_roster(self):
        names = [s.name for s in getattr(self.course, "enrolled_students", [])]
        print(f"[Roster] {self.course.name}: {', '.join(names) if names else '(empty)'}")

_roster.RosterFacade = RosterFacade

# faculty.course_requests
_creq = _ensure_module("faculty.course_requests")
class Request:
    def __init__(self, level, message, requester):
        self.level = level
        self.message = message
        self.requester = requester

class _Handler:
    def __init__(self):
        self._next = None
    def set_next(self, nxt):
        self._next = nxt
        return nxt
    def handle(self, req):
        if self._next:
            return self._next.handle(req)
        return f"Unhandled: {req.message}"

class InstructorHandler(_Handler):
    def handle(self, req):
        if req.level == "instructor":
            return f"Instructor approved: {req.message}"
        return super().handle(req)

class DeptHeadHandler(_Handler):
    def handle(self, req):
        if req.level == "dept_head":
            return f"DeptHead approved: {req.message}"
        return super().handle(req)

class AdminHandler(_Handler):
    def handle(self, req):
        if req.level == "admin":
            return f"Admin approved: {req.message}"
        return super().handle(req)

class LoggingDecorator(_Handler):
    def __init__(self, handler):
        super().__init__()
        self._handler = handler
    def set_next(self, nxt):
        wrapped = LoggingDecorator(nxt)
        self._handler.set_next(wrapped)
        return wrapped
    def handle(self, req):
        print(f"[Log] Enter {self._handler.__class__.__name__}")
        res = self._handler.handle(req)
        print(f"[Log] Exit {self._handler.__class__.__name__}: {res}")
        return res

_creq.Request = Request
_creq.InstructorHandler = InstructorHandler
_creq.DeptHeadHandler = DeptHeadHandler
_creq.AdminHandler = AdminHandler
_creq.LoggingDecorator = LoggingDecorator

# admin.management
_mgmt = _ensure_module("admin.management")
class AdminManager:
    def override_enrolment(self, service, student, course):
        # Bypass strict validations by forcing enrol
        if course not in student.enrolled_courses:
            student.enrolled_courses.append(course)
        course.enrol_student(student)
        return True

_mgmt.AdminManager = AdminManager

# shared.notifications
_notif = _ensure_module("shared.notifications")
class NotificationService:
    def __init__(self):
        self._subs = []
    def subscribe(self, obs):
        self._subs.append(obs)
    def unsubscribe(self, obs):
        if obs in self._subs:
            self._subs.remove(obs)
    def notify(self, event, message):
        for s in list(self._subs):
            if hasattr(s, "update"):
                s.update(event, message)

class StudentNotifier:
    def update(self, event, message):
        print(f"[Notify:{event}] {message}")

_notif.NotificationService = NotificationService
_notif.StudentNotifier = StudentNotifier

# shared.transactions
_trx = _ensure_module("shared.transactions")
class EnrolmentTransaction:
    def __init__(self, service, student, course):
        self.service = service
        self.student = student
        self.course = course
        self._committed = False
    def execute(self):
        # Validate first
        if self.course in self.student.enrolled_courses:
            print("[Tx] Enrol failed (already enrolled). Rolling back.")
            return False
        ok = self.service.enrol(self.student, self.course)
        if not ok:
            print("[Tx] Enrol failed (validation). Rolling back.")
            return False
        # Commit
        self.student.enrolled_courses.append(self.course)
        self.course.enrol_student(self.student)
        self._committed = True
        print("[Tx] Enrol committed.")
        return True

_trx.EnrolmentTransaction = EnrolmentTransaction

print_header("NexusEnroll Demo End")