# -*- coding: utf-8 -*-

import threading

from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from .ExecutionState import ExecutionState
from ..benchmarks.BenchmarkInstance import BenchmarkInstance
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..results.BenchmarkResult import BenchmarkResult

from .ExecutionContext import ExecutionContext
from .ExecutionStrategy import ExecutionStrategy
from .ProportionalExecutionStrategy import ProportionalExecutionStrategy


class SequencialExecutionStrategy(ExecutionStrategy):

    def __init__(self, configuration, results, execution, benchmarks):
        super().__init__(configuration, results, execution, benchmarks)

        self.__running = False
        self.__current = None
        self.__timeout = None

    @property
    def is_stopped(self):
        return not self.__running

    def start(self, callback=None):
        if self._configuration.duration <= 0:
            raise Exception('Duration was not set')

        if self.__running:
            callback(None)
            return

        self.__running = True
        self.__execute(callback)

    def stop(self, callback=None):
        if self.__timeout is not None:
            self.__timeout.do_run = False
            self.__timeout = None

        if self.__running:
            self.__running = False

            if self._execution:
                self._execution.stop()

            if self.__current is not None:
                self.__current.stop(callback)
            else:
                if callback:
                    callback(None)

        else:
            if callback:
                callback(None)

    def __execute(self, callback=None):
        def inner():
            try:
                for benchmark in self._benchmarks:
                    # Skip if benchmarking was interrupted
                    if not self.__running:
                        callback()
                        return

                    # Start embedded strategy
                    self.__current = ProportionalExecutionStrategy(self._configuration, self._results, None,
                                                                   [benchmark])

                    # Wait for specified duration and stop embedded strategy
                    def _timeout():
                        self.__current.stop(lambda _err: callback(_err))
                        self.__current = None

                    self.__timeout = threading.Timer(self._configuration.duration * 1000, _timeout)
                    self.__timeout.start()
                    self.__timeout.join()
            except Exception as err:
                callback(err)

        threading.Thread(target=inner).start()
