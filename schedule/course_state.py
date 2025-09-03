from abc import ABC, abstractmethod

class CourseState(ABC):
    @abstractmethod
    def start(self, context):
        pass

    @abstractmethod
    def complete(self, context):
        pass

    @abstractmethod
    def archive(self, context):
        pass

class PlannedState(CourseState):
    def start(self, context):
        print("Course started.")
        context.state = OngoingState()
    def complete(self, context):
        print("Cannot complete. Course not started.")
    def archive(self, context):
        print("Cannot archive. Course not started.")

class OngoingState(CourseState):
    def start(self, context):
        print("Course already started.")
    def complete(self, context):
        print("Course completed.")
        context.state = CompletedState()
    def archive(self, context):
        print("Cannot archive. Course not completed.")

class CompletedState(CourseState):
    def start(self, context):
        print("Cannot start. Course already completed.")
    def complete(self, context):
        print("Course already completed.")
    def archive(self, context):
        print("Course archived.")
        context.state = ArchivedState()

class ArchivedState(CourseState):
    def start(self, context):
        print("Cannot start. Course is archived.")
    def complete(self, context):
        print("Cannot complete. Course is archived.")
    def archive(self, context):
        print("Course already archived.")

class CourseContext:
    def __init__(self):
        self.state = PlannedState()

    def start(self):
        self.state.start(self)

    def complete(self):
        self.state.complete(self)

    def archive(self):
        self.state.archive(self)

    def get_state_name(self):
        return self.state.__class__.__name__
