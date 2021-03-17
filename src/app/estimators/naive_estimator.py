from app.estimators import BaseOverloadHourEstimator


class NaiveOverloadHourEstimator(BaseOverloadHourEstimator):
    def _get_estimator_instance(self) -> object:
        return set()

    def _calculate_cardinality(self, hour: str) -> float:
        return len(self._estimators[hour])

    def _add_record(self, hour: str, record: str):
        self._estimators[hour].add(record)
