from abc import ABC, abstractmethod

class Request:
    def __init__(self, type_, description, faculty):
        self.type = type_
        self.description = description
        self.faculty = faculty

class RequestHandler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next:
            return self._next.handle(request)
        return None

class InstructorHandler(RequestHandler):
    def handle(self, request):
        if request.type == "instructor":
            print(f"Instructor handled: {request.description}")
            return True
        return super().handle(request)

class DeptHeadHandler(RequestHandler):
    def handle(self, request):
        if request.type == "dept_head":
            print(f"DeptHead handled: {request.description}")
            return True
        return super().handle(request)

class AdminHandler(RequestHandler):
    def handle(self, request):
        if request.type == "admin":
            print(f"Admin handled: {request.description}")
            return True
        return super().handle(request)

class LoggingDecorator(RequestHandler):
    def __init__(self, handler):
        super().__init__()
        self._handler = handler

    def handle(self, request):
        print(f"[LOG] Handling request: {request.type} - {request.description}")
        # First, delegate to the wrapped handler
        handled = self._handler.handle(request)
        # If not handled, propagate to the next in the chain (CoR)
        if not handled and self._next:
            return self._next.handle(request)
        return handled
