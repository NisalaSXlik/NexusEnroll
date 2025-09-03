Requirement Summary — NexusEnroll (concise)

Business scenario:
- Modernise "LegacyEnroll" into "NexusEnroll": a flexible, scalable course enrolment platform for a large university.

Core functional requirements:
- Student self-service: browse catalogue, add/drop courses, view schedule, track academic progress.
- Faculty tools: view rosters, submit grades (with approval states), request course changes.
- Administrator controls: create/edit/delete courses and programs, manage accounts, override enrolments, generate reports.
- Scalability: support high concurrent users (peak enrolment periods).
- Accessibility: backend usable by web SPA and future mobile clients.

Detailed features (high level):
1. Student Module
- Search and browse courses (filters: dept, number, keyword, instructor).
- Enrolment with validation (prerequisites, capacity, time conflicts).
- Schedule view and progress tracking.

2. Faculty Module
- Real-time class rosters.
- Grade submission workflow (Draft → Pending → Submitted), batch operations and error recovery.
- Course information change requests with approval workflow.

3. Administrator Module
- Course & program management, user account management, manual overrides.
- Reporting: enrolment stats, faculty workload, popularity trends.

4. System-wide
- Notification system (decoupled observers) for waitlists, advisor alerts, and system errors.
- Transaction management for enrol/withdraw operations ensuring atomicity and rollback.
- API-driven backend compatible with SPA/mobile frontends.

This file maps the assignment's functional requirements to the repository-level components in `docs/architecture.md`.
