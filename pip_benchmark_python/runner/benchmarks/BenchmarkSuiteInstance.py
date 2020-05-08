# -*- coding: utf-8 -*-

import threading

from ...BenchmarkSuite import BenchmarkSuite
from ...IExecutionContext import IExecuteContext
from ...Parameter import Parameter
from .BenchmarkInstance import BenchmarkInstance


class BenchmarkSuiteInstance:

    def __init__(self, suite):

        self.__suite = suite
        self.__benchmarks = list(map(lambda benchmark: BenchmarkInstance(self, benchmark), suite.benchmarks))

    @property
    def suite(self):
        return self.__suite

    @property
    def name(self):
        return self.__suite.name

    @property
    def description(self):
        return self.__suite.description

    @property
    def parameters(self):
        result = []
        parameters = self.__suite.parameters
        for prop in parameters.keys():
            if prop in parameters.keys():
                parameter = parameters[prop]
                if isinstance(parameter, Parameter):
                    result.append(parameter)

        return result

    @property
    def benchmarks(self):
        return self.__benchmarks

    @property
    def is_selected(self):
        return list(filter(lambda benchmark: benchmark.is_selected, self.__benchmarks))

    def select_all(self):
        for benchmark in self.__benchmarks:
            benchmark.is_selected = True

    def select_by_name(self, benchmark_name):
        for benchmark in self.__benchmarks:
            if benchmark.name == benchmark_name:
                benchmark.is_selected = True

    def unselect_all(self):
        for benchmark in self.__benchmarks:
            benchmark.is_selected = False

    def unselect_by_name(self, benchmark_name):
        for benchmark in self.__benchmarks:
            if benchmark.name == benchmark_name:
                benchmark.is_selected = False

    def set_up(self, context, callback):
        self.__suite.context = context

        def inner(err):
            if err:
                callback(err)
                return
            try:
                for benchmark in self.__benchmarks:
                    if benchmark.is_selected:
                        benchmark.set_up(context, callback)
                    else:
                        callback()
            except Exception as err:
                callback(err)

        threading.Thread(
            target=self.__suite.set_up, args=(inner,)
        ).start()

    def tear_down(self, callback):

        def inner(err):
            if err:
                callback(err)
                return
            try:
                for benchmark in self.__benchmarks:
                    if benchmark.is_selected:
                        benchmark.tear_down(callback)
                    else:
                        callback()
            except Exception as err:
                callback(err)

        threading.Thread(
            target=self.__suite.tear_down, args=(inner,)
        ).start()
