# -*- coding: utf-8 -*-

from .config.ConfigurationManager import ConfigurationManager
from .results.ResultsManager import ResultsManager
from .benchmarks.BenchmarksManager import BenchmarksManager
from .parameters.ParametersManager import ParametersManager
from .execution.ExecutionManager import ExecutionManager
from .reports.ReportGenerator import ReportGenerator
from .environment.EnvironmentManager import EnvironmentManager


class BenchmarkRunner:

    def __init__(self):
        self.__configuration = None
        self.__results = None
        self.__parameters = None
        self.__benchmarks = None
        self.__execution = None
        self.__report = None
        self.__environment = None

        self.__configuration = ConfigurationManager()
        self.__results = ResultsManager()
        self.__parameters = ParametersManager(self.__configuration)
        self.__benchmarks = BenchmarksManager(self.__parameters)
        self.__execution = ExecutionManager(self.__configuration, self.__results)
        self.__environment = EnvironmentManager()
        self.__report = ReportGenerator(self.__configuration, self.__results,
                                        self.__parameters, self.__benchmarks,
                                        self.__environment)

    @property
    def configuration(self):
        return self.__configuration

    @property
    def results(self):
        return self.__results

    @property
    def parameters(self):
        return self.__parameters

    @property
    def execution(self):
        return self.__execution

    @property
    def benchmarks(self):
        return self.__benchmarks

    @property
    def report(self):
        return self.__report

    @property
    def environment(self):
        return self.__environment

    @property
    def is_running(self):
        return self.__execution.is_running

    def start(self):
        self.__execution.start(self.__benchmarks.is_selected)

    def stop(self):
        self.__execution.stop()

    def run(self, callback):
        self.__execution.run(self.__benchmarks.is_selected, callback)
