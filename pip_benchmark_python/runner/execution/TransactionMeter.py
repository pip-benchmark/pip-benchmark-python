# -*- coding: utf-8 -*-

import datetime

from .BenchmarkMeter import BenchmarkMeter


class TransactionMeter(BenchmarkMeter):
    __transaction_counter = 0

    def __init__(self):
        super().__init__()
        self.__transaction_counter = 0

    def incremental_transaction_counter(self, value):
        self.__transaction_counter += 1

    def set_transaction_counter(self, value):
        self.__transaction_counter = value

    def _perform_measurement(self):
        current_time = datetime.datetime.now().timestamp()
        duration_in_msecs = (current_time - self._last_measured_time) / 1000
        result = 0
        try:
            result = self.__transaction_counter * 1000 / duration_in_msecs
        except ZeroDivisionError:
            self._last_measured_time = current_time
            self.__transaction_counter = 0
        finally:
            return result
