# Centralized event/notification manager for Observer pattern
class EventManager:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, observer):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(observer)

    def unsubscribe(self, event_type, observer):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(observer)

    def notify(self, event_type, data):
        for obs in self._subscribers.get(event_type, []):
            obs.update(event_type, data)

# Example observer classes
class StudentNotifier:
    def update(self, event_type, data):
        print(f"Student notified: {event_type} - {data}")

class FacultyNotifier:
    def update(self, event_type, data):
        print(f"Faculty notified: {event_type} - {data}")

class AdminNotifier:
    def update(self, event_type, data):
        print(f"Admin notified: {event_type} - {data}")
