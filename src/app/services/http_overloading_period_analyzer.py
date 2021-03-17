import traceback
from app.services.socket import Server
from app.models import HTTPServerErrorLogRecord
from app.estimators import HyperLogLogOverloadHourEstimator, NaiveOverloadHourEstimator


class HTTPOverloadingPeriodAnalyzer(Server):
    def __init__(self, host: str, port: int, estimator="hyperloglog"):
        super().__init__(host, port)
        if estimator == "naive":
            self.logger.critical("NAIVE estimator")
            self.estimator = NaiveOverloadHourEstimator()
        else:
            self.logger.critical("HLL estimator")
            self.estimator = HyperLogLogOverloadHourEstimator()

    def _process_message(self, message: str):
        try:
            server_error = HTTPServerErrorLogRecord(message)
            se_weekday = server_error.datetime_stamp.weekday()
            if se_weekday < 5:  # 5 - Saturday, 6 - Sunday
                se_hour = str(server_error.datetime_stamp.hour).zfill(2)
                unique_to_date_ip_repr = f"{server_error.datetime_stamp.strftime('%Y-%m-%d')}_{server_error.ip}"
                self.estimator.estimate(se_hour, unique_to_date_ip_repr)
            self.logger.critical(str(self.estimator))
        except ValueError as ve:
            self.logger.debug(repr(ve))
        except Exception as _e:
            self.logger.error(traceback.format_exc())
