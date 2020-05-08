# -*- coding: utf-8 -*-

import datetime

from ..results.ResultsManager import ResultsManager
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..results.BenchmarkResult import BenchmarkResult
from .TransactionMeter import TransactionMeter
from .CpuLoadMeter import CpuLoadMeter
from .MemoryUsageMeter import MemoryUsageMeter


class ResultAggregator:
    __MAX_ERROR_COUNT = 1000

    def __init__(self, results, benchmarks):
        self.__results = results
        self.__benchmarks = benchmarks
        self.__transaction_counter = 0
        self.__result = None
        self.__transaction_meter = None
        self.__cpu_load_meter = None
        self.__memory_usage_meter = None

        self.__cpu_load_meter = CpuLoadMeter()
        self.__transaction_meter = TransactionMeter()
        self.__memory_usage_meter = MemoryUsageMeter()

        self.start()

    @property
    def result(self):
        return self.__result

    def start(self):
        self.__result = BenchmarkResult()
        self.__result.benchmarks = self.__benchmarks
        self.__result.start_time = datetime.datetime.now()

        self.__transaction_counter = 0
        self.__transaction_meter.clear()
        self.__cpu_load_meter.clear()
        self.__memory_usage_meter.clear()

    def increment_counter(self, increment, now=None):
        now = now or datetime.datetime.now()
        self.__transaction_counter += increment

        # If it's less then a second then wait
        measure_interval = (now.timestamp() - self.__memory_usage_meter.last_measured_time.timestamp()) * 1000
        if measure_interval >= 1000 and self.__result is not None:
            # Perform measurements
            self.__transaction_meter.set_transaction_counter(self.__transaction_counter)
            self.__transaction_counter = 0
            self.__transaction_meter.measure()
            self.__cpu_load_meter.measure()
            self.__memory_usage_meter.measure()

            # Store measurement results
            self.result.elapsed_time = (now.timestamp() - self.__result.start_time.timestamp()) * 1000
            self.__result.performance_measurement = self.__transaction_meter.measurement
            self.__result.cpu_load_measurement = self.__cpu_load_meter.measurement
            self.__result.memory_usage_measurement = self.__memory_usage_meter.measurement

            self.__results.notify_updated(self.__result)

    def send_message(self, message):
        self.__results.notify_message(message)

    def report_error(self, error):
        if len(self.__result.errors) < ResultAggregator.__MAX_ERROR_COUNT:
            self.__result.errors.append(error)

        self.__results.notify_error(error)

    def stop(self):
        self.__results.add(self.__result)
