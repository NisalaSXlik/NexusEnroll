from abc import ABC, abstractmethod

class Program:
    def __init__(self):
        self.required_courses = []
        self.electives = []
        self.name = ""

class ProgramBuilder(ABC):
    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def add_required_course(self, course):
        pass

    @abstractmethod
    def add_elective(self, course):
        pass

    @abstractmethod
    def get_program(self):
        pass

class ConcreteProgramBuilder(ProgramBuilder):
    def __init__(self):
        self.program = Program()

    def set_name(self, name):
        self.program.name = name

    def add_required_course(self, course):
        self.program.required_courses.append(course.id)

    def add_elective(self, course):
        self.program.electives.append(course.id)

    def get_program(self):
        return self.program

class ProgramDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, name, required_courses, electives):
        self.builder.set_name(name)
        for course in required_courses:
            self.builder.add_required_course(course)
        for course in electives:
            self.builder.add_elective(course)
        return self.builder.get_program()
