import unittest
from app.services import HTTPOverloadingPeriodAnalyzer
from app.estimators import NaiveOverloadHourEstimator, HyperLogLogOverloadHourEstimator


class TestHTTPOverloadingPeriodAnalyzer(unittest.TestCase):
    def test_instance_create(self):
        server = HTTPOverloadingPeriodAnalyzer("127.0.0.1", 7649)
        self.assertIsInstance(server, HTTPOverloadingPeriodAnalyzer)
        self.assertIsInstance(server.estimator, HyperLogLogOverloadHourEstimator)
        server = HTTPOverloadingPeriodAnalyzer("127.0.0.1", 7649, "naive")
        self.assertIsInstance(server, HTTPOverloadingPeriodAnalyzer)
        self.assertIsInstance(server.estimator, NaiveOverloadHourEstimator)

    def test_process_message__not_server_error(self):
        server = HTTPOverloadingPeriodAnalyzer("127.0.0.1", 7649)
        record_fixture = '{"time":"2021-03-17 17:24:53","ip":"10.0.186.98","status_code":302}'
        hour = server.estimator.max_overload_hour
        server._process_message(record_fixture)
        self.assertEqual(hour, server.estimator.max_overload_hour)

    def test_process_message(self):
        server = HTTPOverloadingPeriodAnalyzer("127.0.0.1", 7649)
        record_fixtures = [
            '{"time":"2021-03-17 17:24:53","ip":"10.0.186.98","status_code":502}',
            '{"time":"2021-03-16 17:24:53","ip":"10.0.186.98","status_code":502}'
        ]
        hour = server.estimator.max_overload_hour
        for f in record_fixtures:
            server._process_message(f)
        self.assertNotEqual(hour, server.estimator.max_overload_hour)


if __name__ == "__main__":
    unittest.main()
