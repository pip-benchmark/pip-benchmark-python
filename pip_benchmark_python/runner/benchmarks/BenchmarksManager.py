# -*- coding: utf-8 -*-

import sys
import os
import importlib
import pkgutil
from pathlib import Path

from ...BenchmarkSuite import BenchmarkSuite
from ...Benchmark import Benchmark
from .BenchmarkInstance import BenchmarkInstance
from .BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..parameters.ParametersManager import ParametersManager


class BenchmarksManager:

    def __init__(self, parameters):
        self.__parameters = None
        self.__suites = []
        self.__parameters = parameters

    @property
    def suites(self):
        return self.__suites

    @property
    def is_selected(self):
        benchmarks = []

        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                if benchmark.is_selected:
                    benchmarks.append(benchmark)

        return benchmarks

    def select_all(self):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                benchmark.is_selected = True

    def select_by_name(self, benchmark_names):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                for benchmark_name in benchmark_names:
                    if benchmark_name == benchmark.full_name:
                        benchmark.is_selected = True

    def select(self, benchmarks):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                for another_benchmark in benchmarks:
                    if benchmark == another_benchmark:
                        benchmark.is_selected = True

    def unselect_all(self):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                benchmark.is_selected = False

    def unselect_by_name(self, benchmark_names):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                for benchmark_name in benchmark_names:
                    if benchmark_name == benchmark.full_name:
                        benchmark.is_selected = False

    def unselect(self, benchmarks):
        for suite in self.__suites:
            for benchmark in suite.benchmarks:
                for another_benchmark in benchmarks:
                    if benchmark == another_benchmark:
                        benchmark.is_selected = False

    def add_suite_from_class(self, suite_class_name):
        if suite_class_name is None or len(suite_class_name) == 0:
            return

        suite = None

        module_name = suite_class_name
        suite_class_name = None

        pos = module_name.index(',')
        if pos >= 0:
            module_and_class_name = module_name
            module_name = module_and_class_name[:pos]
            suite_class_name = module_and_class_name[pos + 1:]

        if module_name.startswith('.'):
            sys.path.append(os.path.abspath(module_name.split('/')[1]))
        else:
            sys.path.append(os.path.abspath(module_name))

        path = ''
        for str in module_name.split('/'):
            if str not in module_name.split('/')[0]:
                path += str + '.'

        module_name = path[:-1]

        try:

            if suite_class_name is not None and len(suite_class_name) > 0:
                suite = getattr(importlib.import_module('.' + suite_class_name.strip(), package=module_name),
                                suite_class_name.strip())

        except ModuleNotFoundError as err:
            raise err
        if callable(suite):
            suite = suite()
            self.add_suite(suite)

    def add_suite(self, suite):
        if isinstance(suite, BenchmarkSuite):
            suite = BenchmarkSuiteInstance(suite)
        if not isinstance(suite, BenchmarkSuiteInstance):
            raise Exception('Incorrect suite type')
        self.__suites.append(suite)
        self.__parameters.add_suite(suite)

    def add_suites_from_module(self, module_name):
        if module_name.startswith('.'):
            sys.path.append(os.path.abspath(module_name.split('/')[1]))
        else:
            sys.path.append(os.path.abspath(module_name))
        suites = {}
        module_path = module_name
        path = ''
        for _str in module_name.split('/'):
            if _str not in module_name.split('/')[0]:
                path += _str + '.'

        module_name = path[:-1]

        for (_, name, _) in pkgutil.iter_modules([Path(os.path.abspath(module_path))]):
            suites[name] = getattr(importlib.import_module('.' + name, package=module_name), name)

        if suites is None:
            raise Exception('Module ' + module_name + ' was not found')

        for prop in suites.keys():

            suite = suites[prop]
            if callable(suite) and prop.endswith('Suite'):

                try:
                    suite = suite()
                    if isinstance(suite, BenchmarkSuite):
                        suite = BenchmarkSuiteInstance(suite)
                        self.__suites.append(suite)
                        self.__parameters.add_suite(suite)

                except Exception as err:
                    # Ignore
                    pass

    def remove_suite_by_name(self, suite_name):
        suite = list(filter(lambda sut: sut.suite == suite_name, self.__suites))

        if suite is not None:
            self.__parameters.remove_suite(suite)
            self.__suites = list(filter(lambda sut: sut.suite != suite_name, self.__suites))

    def remove_suite(self, suite):
        if isinstance(suite, BenchmarkSuite):
            suite = list(filter(lambda sut: sut.suite == suite, self.__suites))

        if not isinstance(suite, BenchmarkSuiteInstance):
            raise Exception('Wrong suite type')

        self.__parameters.remove_suite(suite)
        self.__suites = list(filter(lambda s: s.suite != suite, self.__suites))

    def clear(self):
        for index in range(len(self.__suites)):
            suite = self.__suites[index]
            self.__parameters.remove_suite(suite)

        self.__suites = []
