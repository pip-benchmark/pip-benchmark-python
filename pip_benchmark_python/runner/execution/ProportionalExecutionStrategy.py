# -*- coding: utf-8 -*-

import random
import datetime
import threading

from ..config.MeasurementType import MeasurementType
from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from .ExecutionContext import ExecutionContext
from ..benchmarks.BenchmarkInstance import BenchmarkInstance
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..results.BenchmarkResult import BenchmarkResult

from .ExecutionContext import ExecutionContext
from .ExecutionStrategy import ExecutionStrategy
from .ResultAggregator import ResultAggregator


class ProportionalExecutionStrategy(ExecutionStrategy):

    def __init__(self, configuration, results,
                 execution, benchmarks):
        super().__init__(configuration, results, execution, benchmarks)

        self.__running = False
        self.__aggregation = None
        self.__ticks_per_transaction = 0
        self.__last_executed_time = None
        self.__stop_time = None
        self.__benchmark_count = None
        self.__only_benchmark = None
        self.__timeout = None

        self.__aggregation = ResultAggregator(results, benchmarks)

    def start(self, callback=None):
        if self.__running:
            callback(None)
            return

        self.__running = True
        self.__aggregation.start()

        self.__calculate_proportional_ranges()

        if self._configuration.measurement_type == MeasurementType.Nominal:
            self.__ticks_per_transaction = 1000.0 / self._configuration.nominal_rate

        # Initialize and start
        def inner(_suite, _callback):
            try:
                _context = ExecutionContext(_suite, self.__aggregation, self)
                self._suites.__sui.set_up(_context, _callback)

                # Execute benchmarks
                self.__execute(_callback)
            except Exception as err:
                # Abort if initialization failed
                self.__aggregation.report_error(err)
                _callback(err)
                return

        for suite in self._suites:
            threading.Thread(
                target=inner, args=(suite, callback)
            ).start()

    @property
    def is_stopped(self):
        return not self.__running

    def stop(self, callback=None):
        # Interrupt any wait
        if self.__timeout is not None:
            self.__timeout.do_run = False
            self.__timeout = None
        if self.__running:
            self.__running = False
            self.__aggregation.stop()

            if self._execution:
                self._execution.stop()

            # Stop and cleanup execution
            def inner(_suite, _callback):
                try:
                    _suite.tear_down(_callback)
                except Exception as err:
                    if _callback:
                        _callback(err)

            for suite in self._suites:
                threading.Thread(
                    target=inner, args=(suite, callback)
                ).start()

        else:
            if callback:
                callback(None)

    def __calculate_proportional_ranges(self):
        total_proportion = 0
        for benchmark in self._active_benchmarks:
            total_proportion += benchmark.proportion

        start_range = 0
        for benchmark in self._active_benchmarks:
            normalized_proportion = benchmark.proportion / total_proportion
            benchmark.start_range = start_range
            benchmark.end_range = start_range + normalized_proportion
            start_range += normalized_proportion

    def __choose_benchmark_proportionally(self):
        proportion = random.random()
        return filter(lambda benchmark: benchmark.with_range(proportion), self._active_benchmarks)

    def __execute_delay(self, delay, callback):
        def inner():
            self.__timeout = None
            self.__last_executed_time = datetime.datetime.now()
            callback(None)

        self.__timeout = threading.Timer(delay, inner)
        self.__timeout.start()

    def __execute_benchmark(self, benchmark, callback):
        try:
            if benchmark is None or benchmark.is_passive:
                # Delay if benchmarks are passive
                self.__execute_delay(500, callback)
            else:
                # Execute active benchmark
                def inner(_err=None):
                    # Process force continue
                    if _err and self._configuration.force_continue:
                        self.__aggregation.report_error(_err)
                        _err = None

                    # Increment counter
                    now = datetime.datetime.now()
                    if _err is None:
                        self.__aggregation.increment_counter(1, now)

                    # Introduce delay to keep nominal rate
                    if _err is None and self._configuration.measurement_type == MeasurementType.Nominal:
                        delay = self.__ticks_per_transaction - (
                                1000 * (now.timestamp() - self.__last_executed_time.timestamp()))
                        self.__last_executed_time = now
                        if delay > 0:
                            self.__execute_delay(delay, callback)
                        else:
                            callback(_err)
                    else:
                        self.__last_executed_time = now
                        callback(_err)

                benchmark.execute(inner)
        except Exception as err:
            # Process force continue
            if self._configuration.force_continue:
                self.__aggregation.report_error(err)
                callback(None)
            else:
                callback(err)

    def __execute(self, callback=None):
        self.__last_executed_time = datetime.datetime.now()
        duration = self._configuration.duration if self._configuration.duration > 0 else 365 * 24 * 36000
        self.__stop_time = datetime.datetime.now().timestamp() * 1000 + duration * 1000
        self.__benchmark_count = len(self._benchmarks)
        self.__only_benchmark = self._benchmarks[0] if self.__benchmark_count == 1 else None

        # Execute benchmarks
        def inner():
            benchmark = self.__only_benchmark if self.__only_benchmark is not None \
                else self.__choose_benchmark_proportionally()
            called = 0
            try:

                def _callback(_err):
                    thread = threading.Thread(target=callback, args=_err)
                    thread.start()
                    thread.join()

                self.__execute_benchmark(benchmark, _callback)

            except Exception as err:
                self.stop(lambda err2: callback(err))

        while self.__running and self.__last_executed_time.timestamp() < self.__stop_time:
            inner()
        self.stop(None)
