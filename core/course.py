
class Course:
    def __init__(self, course_id, name, instructor, capacity, prerequisites=None, schedule=None, department=None, description=None):
        self._id = course_id
        self._name = name
        self._instructor = instructor
        self._capacity = capacity
        self._prerequisites = prerequisites if prerequisites else []
        self._schedule = schedule
        self._enrolled_students = []
        self._waitlist = []
        self._department = department
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def instructor(self):
        return self._instructor

    @property
    def capacity(self):
        return self._capacity

    @property
    def prerequisites(self):
        return self._prerequisites

    @property
    def schedule(self):
        return self._schedule

    @property
    def department(self):
        return self._department

    @property
    def description(self):
        return self._description

    @property
    def enrolled_students(self):
        return list(self._enrolled_students)

    @property
    def waitlist(self):
        return list(self._waitlist)

    def enrol_student(self, student):
        if student in self._enrolled_students:
            return False  # Already enrolled
        if len(self._enrolled_students) < self._capacity:
            self._enrolled_students.append(student)
            return True
        # Course full, add to waitlist if not already present
        if student not in self._waitlist:
            self._waitlist.append(student)
        return False

    def drop_student(self, student):
        if student in self._enrolled_students:
            self._enrolled_students.remove(student)
            # If waitlist not empty, promote first waitlisted student
            if self._waitlist:
                promoted = self._waitlist.pop(0)
                self._enrolled_students.append(promoted)
                # Notify promoted student if notification service is available
                notif_service = getattr(self, "notification_service", None)
                if notif_service:
                    notif_service.notify("waitlist_promoted", f"{getattr(promoted, 'name', promoted)} promoted from waitlist to {self._name}")
            return True
        # Remove from waitlist if present
        if student in self._waitlist:
            self._waitlist.remove(student)
            return True
        return False

    def __str__(self):
        return f"Course({self._id}, {self._name}, Instructor: {self._instructor})"
