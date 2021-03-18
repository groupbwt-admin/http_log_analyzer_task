import traceback
from app.services.socket import Server
from app.models import HTTPServerErrorLogRecord
from app.estimators import HyperLogLogOverloadHourEstimator, NaiveOverloadHourEstimator, BaseOverloadHourEstimator


class HTTPOverloadingPeriodAnalyzer(Server):
    def __init__(self, host: str, port: int, estimator="hyperloglog"):
        """
        :param host:
        :param port:
        :param estimator:
        """
        super().__init__(host, port)
        if estimator == "naive":
            self.estimator: BaseOverloadHourEstimator = NaiveOverloadHourEstimator()
        else:
            self.estimator: BaseOverloadHourEstimator = HyperLogLogOverloadHourEstimator()
        self.total_processed_messages = 0

    def _process_message(self, message: str):
        """
        process each retrieved by the server message to validate it as server error (5xx)
        :param message:
        :return:
        """
        self.total_processed_messages += 1
        try:
            server_error = HTTPServerErrorLogRecord(message)
            se_weekday = server_error.datetime_stamp.weekday()
            if se_weekday < 5:  # 5 - Saturday, 6 - Sunday
                se_hour = str(server_error.datetime_stamp.hour).zfill(2)
                unique_to_date_ip_repr = f"{server_error.datetime_stamp.strftime('%Y-%m-%d')}_{server_error.ip}"
                self.estimator.estimate(se_hour, unique_to_date_ip_repr)
            self.logger.debug(str(self.estimator))
            print(f"Total messages: {self.total_processed_messages}"
                  f" - Current hour with max value of server errors experienced for unique users is: "
                  f"{self.estimator.max_overload_hour}")
        except ValueError as ve:
            self.logger.debug(repr(ve))
        except Exception as _e:
            self.logger.error(traceback.format_exc())
