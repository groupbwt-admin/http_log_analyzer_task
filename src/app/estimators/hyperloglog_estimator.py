from datasketch import HyperLogLogPlusPlus
from app.estimators import BaseOverloadHourEstimator


class HyperLogLogOverloadHourEstimator(BaseOverloadHourEstimator):
    hyperloglog_accuracy = 12

    def _get_estimator_instance(self) -> object:
        """
        create HyperLogLogPlusPlus cardinality estimator class instance
        :return:
        """
        return HyperLogLogPlusPlus(p=self.hyperloglog_accuracy)

    def _calculate_cardinality(self, hour: str) -> float:
        """
        method to execute calculating cardinality of estimator
        :param hour:
        :return:
        """
        return self._estimators[hour].count()

    def _add_record(self, hour: str, record: str):
        """
        method to perform adding record to corresponding estimator
        :param hour:
        :param record:
        :return:
        """
        self._estimators[hour].update(record.encode())
