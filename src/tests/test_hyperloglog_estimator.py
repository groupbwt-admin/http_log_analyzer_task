import unittest
from app.estimators import HyperLogLogOverloadHourEstimator
from app.models import HTTPServerErrorLogRecord


class TestNaiveOverloadHourEstimator(unittest.TestCase):
    def test_instance_create(self):
        estimator = HyperLogLogOverloadHourEstimator()
        self.assertIsInstance(estimator, HyperLogLogOverloadHourEstimator)

    def test_estimate(self):
        import pathlib
        estimator = HyperLogLogOverloadHourEstimator()
        with open(f"{pathlib.Path(__file__).parent.absolute()}/fixtures/log_streams_errors.log", "r") as f:
            for line in f.readlines():
                http_log_record = HTTPServerErrorLogRecord(line)
                se_hour = str(http_log_record.datetime_stamp.hour).zfill(2)
                unique_to_date_ip_repr = f"{http_log_record.datetime_stamp.strftime('%Y-%m-%d')}_{http_log_record.ip}"
                estimator.estimate(se_hour, unique_to_date_ip_repr)
        self.assertEqual(estimator.max_overload_hour, "17")

    def test___add_record(self):
        fixture_ip = "127.0.0.1"
        fixture_hour = "04"
        estimator = HyperLogLogOverloadHourEstimator()
        estimator._add_record(fixture_hour, fixture_ip)
        estimator._add_record(fixture_hour, fixture_ip)
        self.assertEqual(round(estimator._calculate_cardinality(fixture_hour)), 1)

    def test___calculate_cardinality(self):
        fixture_ip = "127.0.0.1"
        fixture_hour = "04"
        estimator = HyperLogLogOverloadHourEstimator()
        estimator._add_record(fixture_hour, fixture_ip)
        self.assertEqual(round(estimator._calculate_cardinality(fixture_hour)), 1)

    def test_incorrect_hour_to_estimate(self):
        record_fixture = '{"time":"2021-03-17 17:24:53","ip":"10.0.186.98","status_code":503}'
        http_log_record = HTTPServerErrorLogRecord(record_fixture)
        estimator = HyperLogLogOverloadHourEstimator()
        estimator.estimate("25", http_log_record.ip)
        self.assertEqual(estimator.max_overload_hour, "00")


if __name__ == "__main__":
    unittest.main()
