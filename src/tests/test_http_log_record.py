import unittest
from app.models import HTTPLogRecord


class TestHTTPLogRecord(unittest.TestCase):
    def test_valid_http_log_record(self):
        record_fixture = '{"time":"2019-05-06 17:24:53","ip":"10.0.186.98","status_code":202}'
        http_log_record = HTTPLogRecord(record_fixture)
        self.assertEqual(http_log_record.status_code, 202)
        self.assertEqual(http_log_record.ip, "10.0.186.98")
        self.assertEqual(str(http_log_record.datetime_stamp), "2019-05-06 17:24:53")

    def test_non_http_status_code_record(self):
        record_fixture = '{"time":"2019-05-06 17:24:53","ip":"10.0.186.98","status_code":1818}'
        with self.assertRaises(ValueError) as context:
            HTTPLogRecord(record_fixture)
        self.assertTrue("HTTP status_code must" in str(context.exception))

    def test_non_valid_ip_record(self):
        record_fixture = '{"time":"2019-05-06 17:24:53","ip":"10.0.186.a","status_code":200}'
        with self.assertRaises(ValueError) as context:
            HTTPLogRecord(record_fixture)
        self.assertTrue("does not appear to be an IPv4 or IPv6 address" in str(context.exception))

    def test_non_datetime_value_record(self):
        record_fixture = '{"time":"2019-15-21 00:00:00","ip":"10.0.186.0","status_code":200}'
        with self.assertRaises(ValueError) as context:
            HTTPLogRecord(record_fixture)
        self.assertTrue("does not match format" in str(context.exception))

    def test_non_valid_json_keys_record(self):
        record_fixture = '{"time":"2019-15-21 00:00:00","IPv4":"10.0.186.0","status_code":200}'
        with self.assertRaises(ValueError) as context:
            HTTPLogRecord(record_fixture)
        self.assertTrue("Failed to validate record keys" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
