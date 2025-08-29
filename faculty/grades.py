from abc import ABC, abstractmethod

class GradeState(ABC):
    @abstractmethod
    def submit(self, grade):
        pass

    @abstractmethod
    def undo(self, grade):
        pass

class DraftState(GradeState):
    def submit(self, grade):
        print("Grade moved to Pending.")
        grade.state = PendingState()
    def undo(self, grade):
        print("Nothing to undo from Draft.")

class PendingState(GradeState):
    def submit(self, grade):
        print("Grade submitted.")
        grade.state = SubmittedState()
    def undo(self, grade):
        print("Undo: Back to Draft.")
        grade.state = DraftState()

class SubmittedState(GradeState):
    def submit(self, grade):
        print("Already submitted.")
    def undo(self, grade):
        print("Undo: Back to Pending.")
        grade.state = PendingState()

class Grade:
    def __init__(self, student, course, grade_value):
        self.student = student
        self.course = course
        self.grade_value = grade_value
        self.state = DraftState()

    def submit(self):
        self.state.submit(self)

    def undo(self):
        self.state.undo(self)

class SubmitGradeCommand:
    def __init__(self, grade):
        self.grade = grade
        self._executed = False

    def execute(self):
        self.grade.submit()
        self._executed = True

    def undo(self):
        if self._executed:
            self.grade.undo()

def batch_submit(grades):
    commands = [SubmitGradeCommand(g) for g in grades]
    for cmd in commands:
        cmd.execute()
    return commands
