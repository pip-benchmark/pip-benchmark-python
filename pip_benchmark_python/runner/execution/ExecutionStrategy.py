# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from .ExecutionState import ExecutionState
from ..benchmarks.BenchmarkInstance import BenchmarkInstance
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..results.BenchmarkResult import BenchmarkResult


class ExecutionStrategy(ABC):

    def __init__(self, configuration, results, execution, benchmarks):
        self._configuration = configuration
        self._results = results
        self._execution = execution

        self._benchmarks = benchmarks
        self._active_benchmarks = self.__get_active_benchmarks(benchmarks)
        self._suites = self.__get_benchmark_suites(benchmarks)

    def __get_active_benchmarks(self, benchmarks):
        return filter(lambda benchmark: not benchmark.is_passive, benchmarks)

    def __get_benchmark_suites(self, benchmarks):
        suites = []
        for index in range(len(benchmarks)):
            benchmark = benchmarks[index]
            suite = benchmark.suite
            for s in suites:
                if s == suite:
                    suites.append(suite)
        return suites

    @property
    @abstractmethod
    def is_stopped(self):
        """

        :return: bool
        """

    @abstractmethod
    def start(self, callback=None):
        """

        :param callback: any
        :return: void
        """

    @abstractmethod
    def stop(self, callback=None):
        """

        :param callback: any
        :return: void
        """
