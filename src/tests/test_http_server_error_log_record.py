import unittest
from app.models import HTTPServerErrorLogRecord


class TestHTTPServerErrorLogRecord(unittest.TestCase):
    def test_valid_http_log_record(self):
        record_fixture = '{"time":"2019-05-06 17:24:53","ip":"10.0.186.98","status_code":503}'
        http_log_record = HTTPServerErrorLogRecord(record_fixture)
        self.assertEqual(http_log_record.status_code, 503)

    def test_non_server_error_http_status_code_record(self):
        record_fixture = '{"time":"2019-05-06 17:24:53","ip":"10.0.186.98","status_code":1818}'
        with self.assertRaises(ValueError) as context:
            HTTPServerErrorLogRecord(record_fixture)
        self.assertTrue("must starts with 5 digit" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
