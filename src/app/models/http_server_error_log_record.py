from app.models import HTTPLogRecord


class HTTPServerErrorLogRecord(HTTPLogRecord):
    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int):
        if not(500 <= status_code < 600):
            raise ValueError("HTTP Server error status code must starts with 5 digit")
        self._status_code = status_code
