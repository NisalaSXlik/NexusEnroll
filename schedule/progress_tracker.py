class ProgressTracker:
    def __init__(self):
        self._completed_courses = {}  # course_id -> grade

    def add_completed(self, course, grade):
        self._completed_courses[course.id] = grade

    def remaining_courses(self, program):
        # Assume program.required_courses is a list of course ids
        completed = set(self._completed_courses.keys())
        required = set(getattr(program, "required_courses", []))
        return list(required - completed)

    def get_completed_courses(self):
        # Returns a dict of course_id -> grade
        return dict(self._completed_courses)
