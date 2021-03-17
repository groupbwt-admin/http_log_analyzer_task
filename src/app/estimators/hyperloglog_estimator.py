from datasketch import HyperLogLogPlusPlus
from app.estimators import BaseOverloadHourEstimator


class HyperLogLogOverloadHourEstimator(BaseOverloadHourEstimator):
    hyperloglog_accuracy = 12

    def _get_estimator_instance(self) -> object:
        return HyperLogLogPlusPlus(p=self.hyperloglog_accuracy)

    def _calculate_cardinality(self, hour: str) -> float:
        return self._estimators[hour].count()

    def _add_record(self, hour: str, record: str):
        self._estimators[hour].update(record.encode())
