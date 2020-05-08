# -*- coding: utf-8 -*-

from ...BenchmarkSuite import BenchmarkSuite
from ...Benchmark import Benchmark
from ...PassiveBenchmark import PassiveBenchmark


class BenchmarkInstance:

    def __init__(self, suite, benchmark):
        self.__suite = suite
        self.__benchmark = benchmark

        self.__selected = False
        self.__proportion = 100
        self.__start_range = None
        self.__end_range = None

    @property
    def suite(self):
        return self.__suite

    @property
    def benchmark(self):
        return self.__benchmark

    @property
    def name(self):
        return self.__benchmark.name

    @property
    def full_name(self):
        return '' + self.__suite.name + '.' + self.name

    @property
    def description(self):
        return self.__benchmark.description

    @property
    def is_selected(self):
        return self.__selected

    @is_selected.setter
    def is_selected(self, value):
        self.__selected = value

    @property
    def is_passive(self):
        return isinstance(self.__benchmark, PassiveBenchmark)

    @property
    def proportion(self):
        return self.__proportion

    @proportion.setter
    def proportion(self, value):
        self.__proportion = max(0, min(10000, value))

    @property
    def start_range(self):
        return self.__start_range

    @start_range.setter
    def start_range(self, value):
        self.__start_range = value

    @property
    def end_range(self):
        return self.__end_range

    @end_range.setter
    def end_range(self, value):
        self.__end_range = value

    def within_range(self, proportion):
        return self.__start_range <= proportion < self.__end_range

    def set_up(self, context, callback):
        self.__benchmark.context = context

        try:
            self.__benchmark.set_up(callback)
        except Exception as err:
            callback(err)

    def execute(self, callback):
        try:
            self.__benchmark.execute(callback)
        except Exception as err:
            callback(err)

    def tear_down(self, callback):
        try:
            self.__benchmark.tear_down(callback)
        except Exception as err:
            callback(err)

        self.__benchmark.context = None
