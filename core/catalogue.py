from abc import ABC, abstractmethod
from .course import Course

class CourseFactory(ABC):
    @abstractmethod
    def create_course(self, course_type, **kwargs):
        pass

class LectureCourse(Course):
    def __init__(self, course_id, name, instructor, capacity, prerequisites=None, schedule=None, department=None, description=None):
        super().__init__(course_id, name, instructor, capacity, prerequisites, schedule, department, description)
        self._type = "Lecture"

    def __str__(self):
        return f"LectureCourse({self._id}, {self._name}, Instructor: {self._instructor})"

class LabCourse(Course):
    def __init__(self, course_id, name, instructor, capacity, prerequisites=None, schedule=None, lab_room=None, department=None, description=None):
        super().__init__(course_id, name, instructor, capacity, prerequisites, schedule, department, description)
        self._type = "Lab"
        self._lab_room = lab_room

    @property
    def lab_room(self):
        return self._lab_room

    def __str__(self):
        return f"LabCourse({self._id}, {self._name}, Instructor: {self._instructor}, Lab: {self._lab_room})"

class ConcreteCourseFactory(CourseFactory):
    def create_course(self, course_type, **kwargs):
        if course_type == "Lecture":
            return LectureCourse(**kwargs)
        elif course_type == "Lab":
            return LabCourse(**kwargs)
        else:
            raise ValueError(f"Unknown course type: {course_type}")

class CourseCatalogue:
    def search_courses(self, **filters):
        results = []
        for course in self._courses.values():
            match = True
            for key, value in filters.items():
                attr = getattr(course, key, None)
                if attr != value:
                    match = False
                    break
            if match:
                results.append(course)
        return results
    def __init__(self):
        self._courses = {}

    def add_course(self, course):
        self._courses[course.id] = course

    def remove_course(self, course_id):
        if course_id in self._courses:
            del self._courses[course_id]

    def get_course(self, course_id):
        return self._courses.get(course_id)

    def list_courses(self):
        return list(self._courses.values())
