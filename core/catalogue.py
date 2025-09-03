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
        # Accept department and description for filtering
        if course_type == "Lecture":
            return LectureCourse(**kwargs)
        elif course_type == "Lab":
            return LabCourse(**kwargs)
        else:
            raise ValueError(f"Unknown course type: {course_type}")

class CourseCatalogue:
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

    def search_courses(self, department=None, instructor=None, keyword=None):
        results = self.list_courses()
        if department:
            results = [c for c in results if hasattr(c, 'department') and c.department == department]
        if instructor:
            results = [c for c in results if c.instructor == instructor]
        if keyword:
            results = [c for c in results if keyword.lower() in c.name.lower() or keyword.lower() in getattr(c, 'description', '').lower()]
        return results
