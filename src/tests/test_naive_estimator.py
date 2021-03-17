import unittest
from app.estimators import NaiveOverloadHourEstimator
from app.models import HTTPServerErrorLogRecord


class TestNaiveOverloadHourEstimator(unittest.TestCase):
    def test_instance_create(self):
        estimator = NaiveOverloadHourEstimator()
        self.assertIsInstance(estimator, NaiveOverloadHourEstimator)

    def test_estimate(self):
        record_fixture = '{"time":"2021-03-17 17:24:53","ip":"10.0.186.98","status_code":503}'
        http_log_record = HTTPServerErrorLogRecord(record_fixture)
        estimator = NaiveOverloadHourEstimator()
        se_hour = str(http_log_record.datetime_stamp.hour).zfill(2)
        estimator.estimate(se_hour, http_log_record.ip)
        self.assertEqual(estimator.max_overload_hour, "17")

    def test___add_record(self):
        fixture_ip = "127.0.0.1"
        fixture_hour = "04"
        estimator = NaiveOverloadHourEstimator()
        estimator._add_record(fixture_hour, fixture_ip)
        self.assertIn(fixture_ip, estimator._estimators[fixture_hour])

    def test___calculate_cardinality(self):
        fixture_ip = "127.0.0.1"
        fixture_hour = "04"
        estimator = NaiveOverloadHourEstimator()
        estimator._add_record(fixture_hour, fixture_ip)
        self.assertEqual(estimator._calculate_cardinality(fixture_hour), 1)

    def test_incorrect_hour_to_estimate(self):
        record_fixture = '{"time":"2021-03-17 17:24:53","ip":"10.0.186.98","status_code":503}'
        http_log_record = HTTPServerErrorLogRecord(record_fixture)
        estimator = NaiveOverloadHourEstimator()
        estimator.estimate("25", http_log_record.ip)
        self.assertEqual(estimator.max_overload_hour, "00")

    def test__str__repr__(self):
        estimator = NaiveOverloadHourEstimator()
        self.assertIn("Current max overload hour is", str(estimator))
        self.assertIn("Current max overload hour is", repr(estimator))


if __name__ == "__main__":
    unittest.main()
