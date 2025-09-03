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
