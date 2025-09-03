# Architecture — NexusEnroll (accurate)

Purpose: provide a concise, repository-accurate description that maps implemented files to the assignment brief. This document only documents code that exists in the repo and its implemented/scaffolded status.

## High-level structure (actual)
- `main.py` — demo script (business-tier proof-of-concept)
- `core/` — course domain and catalogue (`course.py`, `catalogue.py`)
- `enrolment/` — enrolment service and validation strategies (`enrolment_service.py`, `validation_strategies.py`)
- `faculty/` — roster, grades, course requests (`roster.py`, `grades.py`, `course_requests.py`)
- `admin/` — management, builder, reports, adapters (`management.py`, `builder.py`, `reports.py`, `adapters.py`)
- `schedule/` — schedule observer, progress tracker, course state (`schedule.py`, `progress_tracker.py`, `course_state.py`)
- `shared/` — notifications, transactions (`notifications.py`, `transactions.py`)

> Note: there is no web/mobile UI or external DB implementation in this repository — `main.py` is the demonstration entrypoint that exercises the business logic.

## Feature → file mapping (status)
Status legend: Implemented = working code; Partial/Scaffold = methods present but some placeholders; Stub = minimal placeholder.

### Student
- Browse catalogue: `core/catalogue.py` — Implemented (LectureCourse, LabCourse, ConcreteCourseFactory, CourseCatalogue with add/get/search/list)
- Enrol / drop: `enrolment/enrolment_service.py`, `enrolment/validation_strategies.py` — Implemented (validation strategies: Prerequisite/Capacity/ScheduleConflict; EnrolmentService and command classes present and used by demo)
- View schedule: `schedule/schedule.py` — Implemented (Schedule, ScheduleObserver, add/remove/notify)
- Track progress: `schedule/progress_tracker.py` — Implemented (ProgressTracker: add_completed, remaining_courses)

### Faculty
- View roster: `faculty/roster.py` — Implemented (RosterIterator, RosterFacade.view_roster)
- Submit grades: `faculty/grades.py` — Implemented (Grade state machine, SubmitGradeCommand, batch_submit)
- Course requests workflow: `faculty/course_requests.py` — Implemented (InstructorHandler, DeptHeadHandler, AdminHandler, LoggingDecorator)

### Admin
- Course/program management: `admin/management.py`, `admin/builder.py` — Implemented (AdminManager singleton, ConcreteProgramBuilder, ProgramDirector)
- Override enrolments: `admin/management.py::override_enrolment` — Implemented
- Reporting: `admin/reports.py`, `admin/adapters.py` — Implemented (ReportGenerator template + Enrollment/Workload/Trend; CSV/JSON/PDF adapters)

### System-wide
- Notifications: `shared/notifications.py` — Implemented (NotificationService and concrete notifiers)
- Transactions / rollback: `shared/transactions.py` — Implemented (Transaction base class; EnrolmentTransaction and GradeTransaction with rollback)

## Design patterns present (file references)
- Factory Method: `core/catalogue.py` (ConcreteCourseFactory, LectureCourse, LabCourse)
- Strategy: `enrolment/validation_strategies.py` (PrerequisiteValidation, CapacityValidation, ScheduleConflictValidation)
- Command: `enrolment/enrolment_service.py` (EnrolCommand, DropCommand) and `faculty/grades.py` (SubmitGradeCommand)
- Observer: `schedule/schedule.py` (ScheduleObserver) and `shared/notifications.py` (NotificationService + notifiers)
- Singleton: `admin/management.py` (AdminManager)
- Builder: `admin/builder.py` (ConcreteProgramBuilder, ProgramDirector)
- Adapter: `admin/adapters.py` (CSVAdapter, JSONAdapter, PDFAdapter, DefaultAdapter)
- Facade / Iterator: `faculty/roster.py` (RosterFacade, RosterIterator)
- State: `faculty/grades.py` (GradeState variants) and `schedule/course_state.py` (CourseState variants)
- Template Method: `admin/reports.py` (ReportGenerator base with concrete report subclasses)
- Transaction: `shared/transactions.py` (Transaction base, EnrolmentTransaction, GradeTransaction)
- Chain of Responsibility + Decorator: `faculty/course_requests.py` (handlers + LoggingDecorator)

## Implementation notes
- Adapters and report outputs are intentionally lightweight (string/JSON/PDF placeholder) to show the Adapter and Template Method patterns without external dependencies.
- `main.py` contains a runnable demo sequence that exercises the catalogue, enrolment, schedule, grades, builder, reports, notifications and transactions; run it to validate integration.

## Quick verification (recommended)
Run this from project root (PowerShell):

```powershell
python -c "import importlib; mods=['core.catalogue','enrolment.validation_strategies','enrolment.enrolment_service','schedule.schedule','faculty.grades','admin.builder','admin.reports','admin.adapters','schedule.progress_tracker','schedule.course_state','faculty.roster','faculty.course_requests','admin.management','shared.notifications','shared.transactions'];
for m in mods:
 try:
  importlib.import_module(m); print(f'[OK] {m}')
 except Exception as e:
  print(f'[ERR] {m}: {e}')
"
```

## Related assignment documentation
To keep the assignment brief and implementation documentation separate and easy to navigate, the full assignment specification and requirement breakdown have been split into companion documents in this folder:

- `assignment_spec.md` — Introduction, duration, team composition, and submission guidelines.
- `assignment_tasks.md` — The assignment outline (Part A and Part B), assessment criteria and task breakdown.
- `requirements_summary.md` — Business scenario and detailed functional requirements (student, faculty, admin, system-wide).

Refer to those files for the canonical assignment text used to guide the implementation and documentation.

## Recommended next steps (I can do these now)
1. Update `docs/REQUIREMENTS_VALIDATION.md` to mirror this mapping (file → requirement status). (recommended)
2. Update `docs/design_patterns_analysis.md` to list patterns and file refs with brief notes.
3. Run a repo-wide scan for TODOs/placeholders and produce a short remediation list.

Tell me which of the recommended edits you want me to apply next and I'll update them accordingly.