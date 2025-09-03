class Course:
    def __init__(self, course_id, name, instructor, capacity, prerequisites=None, schedule=None):
        self._id = course_id
        self._name = name
        self._instructor = instructor
        self._capacity = capacity
        self._prerequisites = prerequisites if prerequisites else []
        self._schedule = schedule
        self._enrolled_students = []

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
    def enrolled_students(self):
        return list(self._enrolled_students)

    def enrol_student(self, student):
        if len(self._enrolled_students) >= self._capacity:
            return False  # Course full
        if student in self._enrolled_students:
            return False  # Already enrolled
        self._enrolled_students.append(student)
        return True

    def drop_student(self, student):
        if student in self._enrolled_students:
            self._enrolled_students.remove(student)
            return True
        return False

    def __str__(self):
        return f"Course({self._id}, {self._name}, Instructor: {self._instructor})"
