from app.estimators import BaseOverloadHourEstimator


class NaiveOverloadHourEstimator(BaseOverloadHourEstimator):
    def _get_estimator_instance(self) -> object:
        """
        create naive (in-memory) unique values container to estimate cardinality
        :return:
        """
        return set()

    def _calculate_cardinality(self, hour: str) -> float:
        """
        :param hour:
        :return:
        """
        return len(self._estimators[hour])

    def _add_record(self, hour: str, record: str):
        """
        :param hour:
        :param record:
        :return:
        """
        self._estimators[hour].add(record)
