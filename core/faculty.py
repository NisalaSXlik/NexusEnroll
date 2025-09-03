# Formal Faculty entity
class Faculty:
    def __init__(self, faculty_id, name):
        self.id = faculty_id
        self.name = name
        self.courses_taught = []  # list of Course objects
        self.notifications = []   # list of notification messages

    def __str__(self):
        return f"Faculty({self.id}, {self.name})"
