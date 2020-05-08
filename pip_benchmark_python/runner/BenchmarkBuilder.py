# -*- coding: utf-8 -*-


from .BenchmarkRunner import BenchmarkRunner
from ..BenchmarkSuite import BenchmarkSuite
from .config.MeasurementType import MeasurementType
from .config.ExecutionType import ExecutionType


class BenchmarkBuilder:

    def __init__(self):
        self._runner = BenchmarkRunner()

    def force_continue(self, is_force_continue=False):
        self._runner.configuration.force_continue = is_force_continue
        return self

    def measure_as(self, measurement_type):
        self._runner.configuration.measurement_type = measurement_type
        return self

    def with_nominal_rate(self, nominal_rate):
        self._runner.configuration.nominal_rate = nominal_rate
        return self

    def execute_as(self, execution_type):
        self._runner.configuration.execution_type = execution_type
        return self

    def for_duration(self, duration):
        self._runner.configuration.duration = duration
        return self

    def add_suite(self, suite):
        self._runner.benchmarks.add_suite(suite)
        return self

    def with_parameter(self, name, value):
        parameters = {name: value}
        self._runner.parameters.set(parameters)

    def with_benchmark(self, name):
        self._runner.benchmarks.select_by_name([name])
        return self

    def with_all_benchmarks(self):
        self._runner.benchmarks.select_all()
        return self

    def create(self):
        result = self._runner
        self._runner = BenchmarkRunner()
        return result
