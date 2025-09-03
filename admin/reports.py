from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    def generate(self):
        data = self.fetch_data()
        processed = self.process_data(data)
        return self.format_data(processed)

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def format_data(self, data):
        pass

class HighCapacityBusinessCoursesReport(ReportGenerator):
    def __init__(self, catalogue):
        self.catalogue = catalogue

    def fetch_data(self):
        # Get all courses in Business school
        return [c for c in self.catalogue.list_courses() if getattr(c, 'department', None) == 'Business']

    def process_data(self, data):
        # Filter courses >90% capacity
        return [c for c in data if c.capacity > 0 and len(c.enrolled_students) / c.capacity >= 0.9]

    def format_data(self, data):
        if not data:
            return "No Business courses over 90% capacity."
        lines = [f"{c.name} ({c.id}): {len(c.enrolled_students)}/{c.capacity} enrolled" for c in data]
        return "High Capacity Business Courses:\n" + "\n".join(lines)

class EnrollmentReport(ReportGenerator):
    def fetch_data(self):
        # Placeholder: fetch enrollment data
        return ["student1", "student2"]

    def process_data(self, data):
        return [d.upper() for d in data]

    def format_data(self, data):
        return f"Enrollment Report: {', '.join(data)}"

class WorkloadReport(ReportGenerator):
    def fetch_data(self):
        return ["faculty1", "faculty2"]

    def process_data(self, data):
        return [d.lower() for d in data]

    def format_data(self, data):
        return f"Workload Report: {', '.join(data)}"

class TrendReport(ReportGenerator):
    def fetch_data(self):
        return [1, 2, 3]

    def process_data(self, data):
        return [x * 10 for x in data]

    def format_data(self, data):
        return f"Trend Report: {', '.join(map(str, data))}"
