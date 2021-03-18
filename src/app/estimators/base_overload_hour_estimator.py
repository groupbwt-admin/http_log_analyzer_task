import logging
from abc import ABC, abstractmethod


class BaseOverloadHourEstimator(ABC):
    def __init__(self):
        self._estimators: dict = {str(hour).zfill(2): self._get_estimator_instance() for hour in range(24)}
        self._max_overload_hour: str = "00"
        self._max_overload_cardinality: float = 0
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    @property
    def max_overload_hour(self) -> str:
        return self._max_overload_hour

    @abstractmethod
    def _get_estimator_instance(self) -> object:
        """
        base method to create estimator instance
        :return:
        """
        pass

    @abstractmethod
    def _calculate_cardinality(self, hour: str) -> float:
        """
        base method to execute calculating cardinality of estimator
        :param hour:
        :return:
        """
        pass

    @abstractmethod
    def _add_record(self, hour: str, record: str):
        """
        base method to perform adding record to corresponding estimator
        :param hour:
        :param record:
        :return:
        """
        pass

    def estimate(self, hour: str, record: str) -> str:
        """
        :param hour: - add record for corresponding to hour estimator
        :param record: - exact value of record for calculating count-distinct
        :return: - current hour with max overload as string with leading zero
        """
        if hour not in self._estimators.keys():
            return self.max_overload_hour
        self._add_record(hour, record)
        current_hour_cardinality = self._calculate_cardinality(hour)
        self.logger.debug(f"Hour: {hour} - cardinality: {current_hour_cardinality}")
        if current_hour_cardinality > self._max_overload_cardinality:
            self._max_overload_cardinality = current_hour_cardinality
            self._max_overload_hour = hour
        return self.max_overload_hour

    def __str__(self) -> str:
        return f"Current max overload hour is {self._max_overload_hour} " \
               f"with estimation of {self._max_overload_cardinality} tracked server errors"

    def __repr__(self) -> str:
        return f"Current max overload hour is {self._max_overload_hour} " \
               f"with estimation of {self._max_overload_cardinality} tracked server errors"
