# -*- coding: utf-8 -*-

import random
from threading import Timer

from ..BenchmarkSuite import BenchmarkSuite


class UtilityBenchmarkSuite(BenchmarkSuite):
    def __init__(self):
        super(UtilityBenchmarkSuite, self).__init__('Utility', 'Set of utility benchmark tests')
        self.create_benchmark('Empty', 'Does nothing', self.__execute_empty)
        self.create_benchmark('RandomDelay', 'Introduces random delay to measuring thread', self.__execute_random_delay)

    def __execute_empty(self, callback):
        # This is empty benchmark
        if callback:
            callback(None)

    def __execute_random_delay(self, callback):
        Timer(random.random(), callback, None).start()
