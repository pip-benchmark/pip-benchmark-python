# -*- coding: utf-8 -*-

from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from ..config.ExecutionType import ExecutionType
from ..benchmarks.BenchmarkInstance import BenchmarkInstance
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from .ExecutionState import ExecutionState
from .ExecutionStrategy import ExecutionStrategy
from ..results.BenchmarkResult import BenchmarkResult

from .ProportionalExecutionStrategy import ProportionalExecutionStrategy
from .SequencialExecutionStrategy import SequencialExecutionStrategy


class ExecutionManager:

    def __init__(self, configuration, results):
        self._configuration = configuration
        self._results = results

        self.__updated_listeners = []
        self.__running = False
        self.__strategy = None

    @property
    def is_running(self):
        return self.__running

    def start(self, benchmarks):
        self.run(benchmarks, lambda err: err)

    def run(self, benchmarks, callback=None):
        if benchmarks is None or len(benchmarks) == 0:
            callback(Exception('There are no benchmarks to execute'))
            return

        if self.__running:
            self.stop()
        self.__running = True

        self._results.clear()
        self.notify_updated(ExecutionState.Running)

        # Create requested execution strategy
        if self._configuration.execution_type == ExecutionType.Sequential:
            self.__strategy = SequencialExecutionStrategy(self._configuration, self._results, self, benchmarks)
        else:
            self.__strategy = ProportionalExecutionStrategy(self._configuration, self._results, self, benchmarks)

        # Initialize parameters and start
        def inner(err):
            self.stop()
            if callback:
                callback(err)

        self.__strategy.start(inner)

    def stop(self):
        if self.__running:
            self.__running = False

            if self.__strategy is not None:
                self.__strategy.stop()
                self.__strategy = None

            self.notify_updated(ExecutionState.Completed)

    def add_updated_listener(self, listener):
        self.__updated_listeners.append(listener)

    def remove_updated_listener(self, listener):
        index = len(self.__updated_listeners) - 1
        while index >= 0:
            if self.__updated_listeners[index] == listener:
                del self.__updated_listeners[index]
            index -= 1

    def notify_updated(self, state):
        for index in range(len(self.__updated_listeners)):
            try:
                listener = self.__updated_listeners[index]
                listener(state)
            except Exception as err:
                # Ignore and send a message to the next listener.
                pass
