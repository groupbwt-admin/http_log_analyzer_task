import json
import datetime
import ipaddress


class HTTPLogRecord:
    record_key_mapping = {
        "datetime_stamp": "time",
        "ip": "ip",
        "status_code": "status_code"
    }
    datetime_stamp_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, record: str):
        payload: dict = json.loads(record)
        if any([k not in payload for k in self.record_key_mapping.values()]):
            raise ValueError("Failed to validate record keys")
        self.datetime_stamp: datetime.datetime = payload.get(self.record_key_mapping.get("datetime_stamp"))
        self.ip: str = payload.get(self.record_key_mapping.get("ip"), "127.0.0.1")
        self.status_code: int = payload.get(self.record_key_mapping.get("status_code"))

    @property
    def datetime_stamp(self) -> datetime.datetime:
        return self._datetime_stamp

    @datetime_stamp.setter
    def datetime_stamp(self, datetime_str: str):
        self._datetime_stamp = datetime.datetime.strptime(datetime_str, self.datetime_stamp_format)

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str):
        ipaddress.ip_address(ip)
        self._ip = ip

    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int):
        if not (100 <= status_code < 1000):
            raise ValueError("HTTP status_code must be 3 digits number")
        self._status_code = status_code
