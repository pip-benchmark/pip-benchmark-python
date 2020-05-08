# -*- coding: utf-8 -*-

from .Parameter import Parameter
from .Benchmark import Benchmark
from .DelegatedBenchmark import DelegatedBenchmark
from .IExecutionContext import IExecuteContext


class BenchmarkSuite:

    def __init__(self, name, description):
        self.__name = None
        self.__description = None
        self.__parameters = {}
        self.__benchmarks = list()
        self.__context = None

        self.__name = name
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, value):
        self.__context = value

    @property
    def parameters(self):
        return self.__parameters

    def add_parameter(self, parameter):
        self.__parameters[parameter.name] = parameter
        return parameter

    def create_parameter(self, name, description, default_value=None):
        parameter = Parameter(name, description, default_value)
        self.__parameters[name] = parameter
        return parameter

    @property
    def benchmarks(self):
        return self.__benchmarks

    def add_benchmarks(self, benchmark):
        self.__benchmarks.append(benchmark)
        return benchmark

    def create_benchmark(self, name, description, execute_callback):
        benchmark = DelegatedBenchmark(name, description, execute_callback)
        self.__benchmarks.append(benchmark)
        return benchmark

    def set_up(self, callback):
        if callback:
            callback(None)

    def tear_down(self, callback):
        if callback:
            callback(None)
