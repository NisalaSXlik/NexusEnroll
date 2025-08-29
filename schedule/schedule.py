class ScheduleObserver:
    def update(self, event, student, course):
        print(f"[ScheduleObserver] Event: {event} for {student.name} on {course.name}")
        self.print_schedule(student)

    def print_schedule(self, student):
        enrolled_names = [c.name for c in getattr(student, "enrolled_courses", [])]
        print(f"Schedule for {student.name}: {', '.join(enrolled_names) if enrolled_names else 'No courses enrolled.'}")

class Schedule:
    def __init__(self, student):
        self.student = student
        self.enrolled_courses = []

    def add_course(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            self.notify("enrolled", course)

    def remove_course(self, course):
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            self.notify("dropped", course)

    def notify(self, event, course):
        observer = getattr(self.student, "schedule_observer", None)
        if observer:
            observer.update(event, self.student, course)

    def get_courses(self):
        return list(self.enrolled_courses)
