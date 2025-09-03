# UML Diagrams for NexusEnroll System

## 1. Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                USER CLASSES                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    User                                        │
│  - user_id: String                                                             │
│  - name: String                                                                │
│  - email: String                                                               │
│  - user_type: UserType                                                         │
│  - created_at: DateTime                                                        │
│  - is_active: Boolean                                                          │
│  + get_permissions(): List<String>                                             │
│  + deactivate(): void                                                          │
│  + activate(): void                                                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ▲
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
┌───────────────────▼──────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│        Student           │  │     Faculty     │  │ Administrator   │
│  - major: String         │  │ - department:   │  │ - department:   │
│  - advisor_id: String    │  │   String        │  │   String        │
│  - enrolled_courses:     │  │ - teaching_     │  │ - admin_level:  │
│    List<String>          │  │   courses:      │  │   String        │
│  - completed_courses:    │  │   List<String>  │  │                 │
│    List<Dict>            │  │                 │  │                 │
│  - gpa: Float            │  │                 │  │                 │
│  + enroll_in_course()    │  │ + assign_course()│  │ + set_admin_    │
│  + drop_course()         │  │ + remove_course()│  │   level()       │
│  + complete_course()     │  │                 │  │                 │
└──────────────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               COURSE CLASSES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   Course                                       │
│  - course_id: String                                                           │
│  - name: String                                                                │
│  - description: String                                                         │
│  - department: String                                                          │
│  - credits: Integer                                                            │
│  - instructor_id: String                                                       │
│  - capacity: Integer                                                           │
│  - schedule: Schedule                                                          │
│  - prerequisites: List<Prerequisite>                                           │
│  - enrolled_students: List<String>                                             │
│  - waitlist: List<String>                                                      │
│  - status: CourseStatus                                                        │
│  + enroll_student(): Boolean                                                   │
│  + drop_student(): Boolean                                                     │
│  + add_prerequisite(): void                                                    │
│  + get_enrollment_info(): Dict                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
┌───────────────────▼──────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│      Schedule            │  │  Prerequisite   │  │  DegreeProgram  │
│  - days: List<DayOfWeek> │  │ - course_id:    │  │ - program_id:   │
│  - start_time: Time      │  │   String        │  │   String        │
│  - end_time: Time        │  │ - min_grade:    │  │ - name: String  │
│  - location: String      │  │   String        │  │ - department:   │
│  + conflicts_with():     │  │                 │  │   String        │
│    Boolean               │  │                 │  │ - total_credits:│
└──────────────────────────┘  └─────────────────┘  │   Integer       │
                                                    │ - required_     │
                                                    │   courses:      │
                                                    │   List<String>  │
                                                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE CLASSES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            EnrollmentService                                   │
│  - students: Dict<String, Student>                                             │
│  - courses: Dict<String, Course>                                               │
│  - enrollments: Dict<String, List<String>>                                     │
│  - validation_context: ValidationContext                                       │
│  - command_invoker: CommandInvoker                                             │
│  + register_student(): void                                                    │
│  + register_course(): void                                                     │
│  + enroll_student(): Boolean                                                   │
│  + drop_student(): Boolean                                                     │
│  + get_student_schedule(): List<Dict>                                          │
│  + get_course_roster(): List<Dict>                                             │
│  + get_enrollment_statistics(): Dict                                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              GradeService                                      │
│  - grades: Dict<String, Dict<String, String>>                                  │
│  - grade_history: Dict<String, List<Dict>>                                     │
│  - pending_grades: Dict<String, List<Dict>>                                    │
│  - command_invoker: CommandInvoker                                             │
│  + submit_grades(): Boolean                                                    │
│  + get_student_grade(): String                                                 │
│  + calculate_student_gpa(): Float                                              │
│  + get_grade_statistics(): Dict                                                │
│  + approve_grades(): Boolean                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              UserService                                       │
│  - users: Dict<String, User>                                                   │
│  - user_sessions: Dict<String, Dict>                                           │
│  - login_attempts: Dict<String, List<DateTime>>                                │
│  + create_user(): Tuple<Boolean, User, String>                                 │
│  + authenticate_user(): Tuple<Boolean, User, String>                           │
│  + get_user_by_id(): User                                                      │
│  + update_user_profile(): Tuple<Boolean, String>                               │
│  + get_user_statistics(): Dict                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Sequence Diagram - Student Enrollment Process

```
Student    WebUI    EnrollmentService    ValidationContext    Course    Observer
   │         │            │                    │               │          │
   │         │            │                    │               │          │
   │   1. Request         │                    │               │          │
   │   enrollment         │                    │               │          │
   │◄─────────────────────┤                    │               │          │
   │         │            │                    │               │          │
   │         │ 2. Enroll  │                    │               │          │
   │         │ Student    │                    │               │          │
   │         ├────────────►                    │               │          │
   │         │            │                    │               │          │
   │         │            │ 3. Validate        │               │          │
   │         │            ├────────────────────►               │          │
   │         │            │                    │               │          │
   │         │            │ 4. Validation      │               │          │
   │         │            │    Results         │               │          │
   │         │            ◄────────────────────┤               │          │
   │         │            │                    │               │          │
   │         │            │ 5. Enroll Student  │               │          │
   │         │            ├────────────────────────────────────►          │
   │         │            │                    │               │          │
   │         │            │ 6. Enrollment      │               │          │
   │         │            │    Result          │               │          │
   │         │            ◄────────────────────────────────────┤          │
   │         │            │                    │               │          │
   │         │            │ 7. Notify          │               │          │
   │         │            ├─────────────────────────────────────────────────►
   │         │            │                    │               │          │
   │         │ 8. Success │                    │               │          │
   │         │ Response   │                    │               │          │
   │         ◄────────────┤                    │               │          │
   │         │            │                    │               │          │
   │ 9. Display           │                    │               │          │
   │    Result            │                    │               │          │
   │◄─────────────────────┤                    │               │          │
```

## 3. Activity Diagram - Course Enrollment Flow

```
                    ┌─────────────────┐
                    │   Start         │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Student Login   │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Browse Courses  │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Select Course   │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Check           │
                    │ Prerequisites   │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Prerequisites   │
                    │ Satisfied?      │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Check Course    │
                    │ Capacity        │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Course Full?    │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Check Schedule  │
                    │ Conflicts       │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Schedule        │
                    │ Conflict?       │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Enroll Student  │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ Send            │
                    │ Notification    │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │ End             │
                    └─────────────────┘
```

## 4. State Diagram - Course Enrollment States

```
                    ┌─────────────────┐
                    │   Available     │
                    │   (Open for     │
                    │   Enrollment)   │
                    └─────────┬───────┘
                              │
                              │ Student Enrolls
                              │
                    ┌─────────▼───────┐
                    │   Enrolled      │
                    │   (Student      │
                    │   Successfully  │
                    │   Enrolled)     │
                    └─────────┬───────┘
                              │
                              │ Student Drops
                              │
                    ┌─────────▼───────┐
                    │   Available     │
                    │   (Open for     │
                    │   Enrollment)   │
                    └─────────┬───────┘
                              │
                              │ Course Reaches
                              │ Capacity
                              │
                    ┌─────────▼───────┐
                    │   Full          │
                    │   (No More      │
                    │   Seats)        │
                    └─────────┬───────┘
                              │
                              │ Student Drops
                              │ (Waitlist
                              │  Promotion)
                              │
                    ┌─────────▼───────┐
                    │   Available     │
                    │   (Open for     │
                    │   Enrollment)   │
                    └─────────────────┘
```

## 5. Component Diagram - System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION TIER                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Mobile App     │    │ Desktop App     │
│                 │    │                 │    │                 │
│  - HTML/CSS/JS  │    │  - React Native │    │  - Electron     │
│  - React/Vue    │    │  - Flutter      │    │  - WPF          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      API Gateway        │
                    │                         │
                    │  - Authentication       │
                    │  - Rate Limiting        │
                    │  - Request Routing      │
                    └────────────┬────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            BUSINESS LOGIC TIER                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Enrollment      │    │ Grade           │    │ User            │
│ Service         │    │ Service         │    │ Service         │
│                 │    │                 │    │                 │
│ - Course        │    │ - Grade         │    │ - Authentication│
│   Management    │    │   Submission    │    │ - Profile       │
│ - Student       │    │ - Academic      │    │   Management   │
│   Enrollment    │    │   Records       │    │ - Authorization │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Cross-Cutting         │
                    │   Concerns              │
                    │                         │
                    │  - Logging              │
                    │  - Caching              │
                    │  - Security             │
                    │  - Monitoring           │
                    └────────────┬────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               DATA TIER                                         │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ User            │    │ Course          │    │ Enrollment      │
│ Database        │    │ Database        │    │ Database        │
│                 │    │                 │    │                 │
│ - User Profiles │    │ - Course Info   │    │ - Enrollment    │
│ - Authentication│    │ - Schedules     │    │   Records       │
│ - Permissions   │    │ - Prerequisites │    │ - Waitlists     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Data Access Layer    │
                    │                         │
                    │  - ORM (SQLAlchemy)    │
                    │  - Repository Pattern  │
                    │  - Connection Pooling  │
                    └─────────────────────────┘
```

## 6. Design Pattern Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              OBSERVER PATTERN                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│    Subject      │                    │    Observer     │
│                 │                    │                 │
│ + attach()      │                    │ + update()      │
│ + detach()      │                    │                 │
│ + notify()      │                    │                 │
└─────────────────┘                    └─────────────────┘
         ▲                                       ▲
         │                                       │
         │                                       │
┌────────▼────────┐                    ┌────────▼────────┐
│ EnrollmentService│                    │EmailNotification│
│                 │                    │   Observer      │
│                 │                    │                 │
│                 │                    │ + update()      │
└─────────────────┘                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FACTORY PATTERN                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│  UserFactory    │                    │      User       │
│                 │                    │                 │
│ + create_user() │                    │                 │
└─────────────────┘                    └─────────────────┘
         ▲                                       ▲
         │                                       │
         │                                       │
┌────────▼────────┐                    ┌────────▼────────┐
│ StudentFactory  │                    │    Student      │
│                 │                    │                 │
│ + create_user() │                    │                 │
└─────────────────┘                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STRATEGY PATTERN                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│ValidationStrategy│                    │ValidationContext│
│                 │                    │                 │
│ + validate()    │                    │ - strategy      │
└─────────────────┘                    │ + set_strategy()│
         ▲                             │ + validate()    │
         │                             └─────────────────┘
         │
┌────────▼────────┐
│PrerequisiteValid│
│   ationStrategy │
│                 │
│ + validate()    │
└─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COMMAND PATTERN                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│    Command      │                    │ CommandInvoker  │
│                 │                    │                 │
│ + execute()     │                    │ + execute_cmd() │
│ + undo()        │                    │ + undo_last()   │
└─────────────────┘                    └─────────────────┘
         ▲                                       │
         │                                       │
         │                                       │
┌────────▼────────┐                    ┌────────▼────────┐
│EnrollStudentCmd │                    │                 │
│                 │                    │                 │
│ + execute()     │                    │                 │
│ + undo()        │                    │                 │
└─────────────────┘                    └─────────────────┘
```

These UML diagrams provide a comprehensive view of the NexusEnroll system architecture, showing the relationships between classes, the flow of operations, and the implementation of design patterns.
