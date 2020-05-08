# -*- coding: utf-8 -*-

import sys
import datetime
from abc import ABC, abstractmethod

from ..results.Measurement import Measurement


class BenchmarkMeter(ABC):

    def __init__(self):
        self._last_measured_time = None
        self.__current_value = None
        self.__min_value = None
        self.__max_value = None
        self.__average_value = None
        self.__sum_of_values = None
        self.__number_of_measurements = None

        self.clear()

    @property
    def measurement(self):
        return Measurement(self.current_value, self.min_value,
                           self.average_value, self.max_value)

    @property
    def last_measured_time(self):
        return self._last_measured_time

    @property
    def current_value(self):
        return self.__current_value

    @current_value.setter
    def current_value(self, value):
        self.__current_value = value

    @property
    def min_value(self):
        return self.__min_value

    @min_value.setter
    def min_value(self, value):
        self.__min_value = value

    @property
    def max_value(self):
        return self.__min_value

    @max_value.setter
    def max_value(self, value):
        self.__max_value = value

    @property
    def average_value(self):
        return self.__average_value

    @average_value.setter
    def average_value(self, value):
        self.__average_value = value

    def clear(self):
        self._last_measured_time = datetime.datetime.now().timestamp()
        self.__current_value = self._perform_measurement()
        self.__min_value = sys.maxsize
        self.__max_value = -sys.maxsize - 1
        self.__average_value = 0
        self.__sum_of_values = 0
        self.__number_of_measurements = 0

    def _calculate_aggregates(self):
        self.__sum_of_values += self.__current_value
        self.__number_of_measurements += 1
        self.__average_value = self.__sum_of_values / self.__number_of_measurements
        self.__max_value = max(self.__min_value, self.__current_value)
        self.__min_value = min(self.__min_value, self.__current_value)

    def measure(self):
        self.__current_value = self._perform_measurement()
        self._last_measured_time = datetime.datetime.now()
        self._calculate_aggregates()
        return self.__current_value

    @abstractmethod
    def _perform_measurement(self):
        """
        
        :return: number
        """
