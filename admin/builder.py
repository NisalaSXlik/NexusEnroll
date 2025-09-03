from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

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
        import logging
        logging.info(f"Constructing program: {name}")
        self.program.name = name

    def add_required_course(self, course):
        import logging
        logging.info(f"Adding required course: {course}")
        self.program.required_courses.append(course.id)

    def add_elective(self, course):
        import logging
        logging.info(f"Adding elective: {course}")
        self.program.electives.append(course.id)

    def get_program(self):
        import logging
        logging.info(f"Program constructed: {self.program.name}")
        return self.program

    def get_program(self):
        return self.program

class ProgramDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, name, required_courses, electives):
        logging.info(f"Constructing program: {name}")
        self.builder.set_name(name)
        for course in required_courses:
            logging.info(f"Adding required course: {course}")
            self.builder.add_required_course(course)
        for course in electives:
            logging.info(f"Adding elective: {course}")
            self.builder.add_elective(course)
        program = self.builder.get_program()
        logging.info(f"Program constructed: {program.name}")
        return program
