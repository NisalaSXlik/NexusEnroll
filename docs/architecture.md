# Architecture — NexusEnroll

## Executive Summary

NexusEnroll implements a Service-Oriented Architecture (SOA) for university course enrollment management. The system demonstrates separation of concerns through distinct service layers (Student, Faculty, Admin) with shared core utilities and comprehensive design pattern implementation.

---

## High-Level Architecture Overview

### System-Wide SOA Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                        NexusEnroll System                       │
├─────────────────────────────────────────────────────────────────┤
│                     Presentation Layer                         │
│                      (main.py - Demo)                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Student       │    Faculty      │        Admin                │
│   Service       │    Service      │        Service              │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • Enrolment     │ • Roster Mgmt   │ • Course Management         │
│ • Schedule      │ • Grade Submit  │ • Program Building          │
│ • Progress      │ • Course Req    │ • Override Authority        │
│   Tracking      │   Workflow      │ • Reporting & Analytics     │
└─────────────────┴─────────────────┴─────────────────────────────┘
        │                │                      │
        └────────────────┼──────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────────┐
│                    Core Domain Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  Course Catalogue  │  Validation Engine  │  Business Rules      │
│  • Course Factory  │  • Strategy Pattern │  • Domain Logic     │
│  • Course Types    │  • Validation Chain │  • Entity Models    │
└─────────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────────┐
│                  Shared Utilities & Patterns                   │
├─────────────────────────────────────────────────────────────────┤
│ Notifications   │ Transactions  │ Design Patterns Infrastructure│
│ • Observer      │ • Rollback    │ • Command/Strategy/State     │
│ • Multi-channel │ • ACID Ops    │ • Factory/Builder/Adapter    │
└─────────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Layer                            │
│              (Future: DB, External APIs, Mobile)               │
└─────────────────────────────────────────────────────────────────┘
```

### Communication Paths

**Service-to-Service Communication:**
- **Admin → Faculty/Student**: Program updates, enrollment overrides
- **Faculty → Student**: Grade notifications, course availability
- **Student → Faculty**: Enrollment requests, progress updates

**Core Domain Access:**
- All services access Course Catalogue for course information
- Validation Engine used by Student service for enrollment checks
- Business Rules enforced across all service operations

**Shared Utilities:**
- Notification system broadcasts events to all interested services
- Transaction system ensures data consistency across service boundaries
- Pattern infrastructure provides reusable components

---

## Architectural Justification

### SOA vs. Microservices vs. 3-Tier Analysis

| Aspect | 3-Tier | SOA (Current) | Microservices |
|--------|--------|---------------|---------------|
| **Deployment** | Monolithic | Service-oriented modules | Independent services |
| **Complexity** | Low | Medium | High |
| **Scalability** | Limited | Good | Excellent |
| **Maintenance** | Simple | Moderate | Complex |
| **Team Size** | Small-Medium | Medium | Large |
| **Network Overhead** | None | Low | High |

**Why SOA for NexusEnroll:**

1. **Right-sized Complexity**: University enrollment systems require structured service separation without microservices overhead
2. **Shared Domain Logic**: Course catalogs, validation rules, and business logic benefit from centralized management
3. **Deployment Simplicity**: Single deployment unit reduces operational complexity for educational institutions
4. **Development Team Scale**: SOA aligns with typical university IT team sizes and skill sets
5. **Data Consistency**: Academic data requires strong consistency, easier to achieve with SOA than distributed microservices

**Trade-offs Considered:**
- **vs 3-Tier**: Sacrificed simplicity for better separation of concerns and pattern demonstration
- **vs Microservices**: Sacrificed independent scaling for reduced complexity and stronger consistency

---

## Maintainability & Scalability

### Maintainability Strengths

**Separation of Concerns:**
- Clear service boundaries (Student/Faculty/Admin)
- Domain logic isolated in core layer
- Shared utilities prevent code duplication

**Design Pattern Implementation:**
- Command pattern enables undo/redo operations
- Strategy pattern allows flexible validation rules
- Observer pattern decouples notifications
- Factory pattern simplifies course creation

**Code Organization:**
```
├── admin/          # Administrative services
├── faculty/        # Faculty-specific operations  
├── core/           # Domain models and business logic
├── enrolment/      # Student enrollment services
├── schedule/       # Schedule and progress tracking
└── shared/         # Cross-cutting concerns
```

### Scalability Considerations

**Horizontal Scaling Potential:**
- Service boundaries enable independent scaling
- Stateless service design supports load distribution
- Observer pattern allows asynchronous processing

**Performance Optimization:**
- Factory pattern reduces object creation overhead
- Strategy pattern enables runtime optimization selection
- Facade pattern simplifies complex subsystem interactions

**Resource Management:**
- Singleton pattern for system-wide resources (AdminManager)
- Iterator pattern for memory-efficient data traversal
- Transaction pattern for resource rollback

---

## Future Integration Possibilities

### Mobile Application Integration

**Architecture Extensions:**
```
Mobile App (iOS/Android)
       ↓
REST API Gateway
       ↓
NexusEnroll SOA Services
```

**Implementation Strategy:**
- Add REST controllers to each service layer
- Implement JWT authentication for mobile sessions
- Extend notification system for push notifications
- Adapt existing validation strategies for mobile workflows

### Financial Aid System Integration

**Integration Patterns:**
```
Financial Aid System ←→ Adapter Layer ←→ Admin Service
                                      ↓
                              Student Enrollment Validation
```

**Technical Approach:**
- Extend existing Adapter pattern (admin/adapters.py)
- Add financial aid validation strategy
- Integrate with transaction system for payment processing
- Leverage notification system for financial updates

### External System Connectivity

**Planned Integration Points:**
1. **Student Information System (SIS)**: Data synchronization via existing adapters
2. **Learning Management System (LMS)**: Course content delivery through facade pattern
3. **Academic Analytics**: Extend reporting system with data warehouse connectors
4. **Identity Management**: Integrate with university LDAP/SSO systems

---

## Principles & Patterns Analysis

### SOLID Principles Implementation

#### Single Responsibility Principle (SRP)
**Examples in Codebase:**
- `CourseCatalogue` (core/catalogue.py): Only manages course collection and search
- `ValidationStrategy` (enrolment/validation_strategies.py): Each strategy handles one validation concern
- `NotificationService` (shared/notifications.py): Only handles observer management and notification dispatch

**Benefits:**
- Each class has one reason to change
- Easier unit testing and debugging
- Clear ownership and maintenance boundaries

#### Open/Closed Principle (OCP)
**Examples in Codebase:**
- `ValidationStrategy` hierarchy: New validation rules added without modifying existing code
- `ReportGenerator` (admin/reports.py): New report types extend base class without changes
- `CourseFactory`: New course types added via factory extension

**Implementation:**
```python
# New validation strategy - extends without modification
class FinancialAidValidation(ValidationStrategy):
    def validate(self, student, course):
        return student.has_financial_aid_approval()
```

### Additional Design Principles

#### DRY (Don't Repeat Yourself)
**Implementation:**
- Shared utilities in `/shared` prevent code duplication
- Template Method pattern in reports eliminates repeated report structure code
- Base classes for common functionality (Command, ValidationStrategy, Observer)

**Example:**
```python
# Base Command class eliminates repetition
class Command(ABC):
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod  
    def undo(self): pass
```

#### KISS (Keep It Simple, Stupid)
**Implementation:**
- Facade pattern (RosterFacade) simplifies complex roster operations
- Clear service boundaries reduce cognitive load
- Single demonstration entry point (main.py) for system validation

---

## UML Activity Diagram: Course Browse/Search Flow

```
Student Perspective - Course Browse/Search Process

    [Start]
       │
       ▼
┌─────────────────┐
│ Browse Courses  │ ◄─── Student
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Access Course   │ ◄─── CourseCatalogue
│   Catalogue     │
└─────────────────┘
       │
       ▼
    ◇ Apply Filters? ◇
       │         │
    [Yes]      [No]
       │         │
       ▼         ▼
┌─────────────────┐    ┌─────────────────┐
│ Filter Courses  │    │ Display All     │
│ (Dept, Level,   │    │ Available       │
│  Prerequisites) │    │ Courses         │
└─────────────────┘    └─────────────────┘
       │                       │
       ▼                       │
┌─────────────────┐             │
│ Validate Search │ ◄─── Validator
│ Criteria        │             │
└─────────────────┘             │
       │                       │
       ▼                       │
┌─────────────────┐             │
│ Return Filtered │             │
│ Course List     │             │
└─────────────────┘             │
       │                       │
       └───────┬───────────────┘
               ▼
┌─────────────────┐
│ Display Course  │
│ Details         │
│ • Name          │
│ • Schedule      │
│ • Prerequisites │
│ • Capacity      │
└─────────────────┘
       │
       ▼
    ◇ Enroll Now? ◇
       │         │
    [Yes]      [No]
       │         │
       ▼         ▼
┌─────────────────┐    ┌─────────────────┐
│ Trigger         │    │ Continue        │
│ Enrollment      │    │ Browsing        │ ───┐
│ Validation      │    └─────────────────┘    │
└─────────────────┘                           │
       │                                      │
       ▼                                      │
┌─────────────────┐                           │
│ Send            │ ◄─── Notifications       │
│ Notifications   │                          │
│ • Student Alert │                          │
│ • Advisor Notice│                          │
└─────────────────┘                          │
       │                                     │
       ▼                                     │
    [End] ◄─────────────────────────────────┘

Objects Involved:
• Student: Initiates browse/search, makes enrollment decisions
• CourseCatalogue: Provides course data and search functionality  
• Validator: Ensures search criteria and enrollment eligibility
• Notifications: Sends alerts about enrollment actions
```

### Activity Flow Explanation

**Browse Phase:**
1. Student accesses the course catalogue system
2. System presents available courses or search interface
3. Student can apply filters (department, level, prerequisites)

**Filter & Validate Phase:**
4. If filters applied, Validator checks search criteria validity
5. CourseCatalogue returns filtered results based on criteria
6. System displays course details including capacity and requirements

**Display & Action Phase:**
7. Student reviews course information
8. Student decides whether to enroll or continue browsing
9. If enrolling, system triggers validation and notification processes
10. Notifications sent to relevant parties (student, advisor)

**System Objects:**
- **Student**: Primary actor driving the workflow
- **CourseCatalogue**: Core service providing course data and search
- **Validator**: Ensures business rule compliance
- **Notifications**: Handles system-wide communication

---

## Implementation Status & File Mapping

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