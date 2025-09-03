from abc import ABC, abstractmethod

class ReportAdapter(ABC):
    @abstractmethod
    def convert(self, report):
        pass

class CSVAdapter(ReportAdapter):
    def convert(self, report):
        # Assume report is a string or list
        if isinstance(report, list):
            return ",".join(map(str, report))
        return str(report)

class JSONAdapter(ReportAdapter):
    def convert(self, report):
        import json
        return json.dumps(report)

class PDFAdapter(ReportAdapter):
    def convert(self, report):
        # Placeholder for PDF conversion
        return f"PDF({str(report)})"
