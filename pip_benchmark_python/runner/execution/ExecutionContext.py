# -*- coding: utf-8 -*-

from ...IExecutionContext import IExecuteContext
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from .ExecutionStrategy import ExecutionStrategy
from .ResultAggregator import ResultAggregator


class ExecutionContext(IExecuteContext):

    def __init__(self, suite, aggregator, strategy):
        self.__aggregator = aggregator
        self.__suite = suite
        self.__strategy = strategy

    @property
    def parameters(self):
        return self.__suite.suite.parameters

    def increment_counter(self, increment=None):
        self.__aggregator.increment_counter(increment or 1)

    def send_message(self, message):
        self.__aggregator.send_message(message)

    def report_error(self, error):
        self.__aggregator.report_error(error)

    @property
    def is_stopped(self):
        return self.__strategy.is_stopped

    def stop(self):
        self.__strategy.stop()
