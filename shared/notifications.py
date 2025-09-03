from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, data):
        pass

class NotificationService:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, observer):
        self._subscribers.append(observer)

    def unsubscribe(self, observer):
        self._subscribers.remove(observer)

    def notify(self, event, data):
        for obs in self._subscribers:
            obs.update(event, data)

class StudentNotifier(Observer):
    def update(self, event, data):
        print(f"Student notified: {event} - {data}")

class AdvisorNotifier(Observer):
    def update(self, event, data):
        print(f"Advisor notified: {event} - {data}")

class AdminNotifier(Observer):
    def update(self, event, data):
        print(f"Admin notified: {event} - {data}")
