class Roster:
    def __init__(self, students):
        self._students = students

    def get_iterator(self):
        return RosterIterator(self._students)

class RosterIterator:
    def __init__(self, students):
        self._students = students
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._students):
            student = self._students[self._index]
            self._index += 1
            return student
        raise StopIteration

class RosterFacade:
    def __init__(self, course):
        self.course = course

    def view_roster(self):
        roster = Roster(getattr(self.course, "enrolled_students", []))
        iterator = roster.get_iterator()
        print(f"Roster for {self.course.name}:")
        for student in iterator:
            print(f"- {getattr(student, 'name', str(student))}")
