# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ...utilities.Properties import Properties
from ..config.ConfigurationManager import ConfigurationManager
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from ..benchmarks.BenchmarkInstance import BenchmarkInstance
from .MeasurementTypeParameter import MeasurementTypeParameter
from .NominalRateParameter import NominalRateParameter
from .ExecutionTypeParameter import ExecutionTypeParameter
from .DurationParameter import DurationParameter
from .DurationParameter import DurationParameter
from .BenchmarkSelectedParameter import BenchmarkSelectedParameter
from .BenchmarkProportionParameter import BenchmarkProportionParameter
from .BenchmarkSuiteParameter import BenchmarkSuiteParameter


class ParametersManager:

    def __init__(self, configuration):
        self.__parameters = list()
        self.__configuration = configuration

        self.__parameters.append(MeasurementTypeParameter(configuration))
        self.__parameters.append(NominalRateParameter(configuration))
        self.__parameters.append(ExecutionTypeParameter(configuration))
        self.__parameters.append(DurationParameter(configuration))

    @property
    def user_defined(self):
        parameters = []

        for parameter in self.__parameters:
            if not (parameter.name.endswith('.Selected')) and not (parameter.name.endswith(
                    '.Proportion')) and not (parameter.name.startswith('General.')):
                parameters.append(parameter)

        return parameters

    @property
    def all(self):
        return self.__parameters

    def load_from_file(self, path):
        properties = Properties()
        properties.load_from_file(path)

        for parameter in self.__parameters:
            if hasattr(properties, parameter.name):
                parameter.value = getattr(properties, parameter.name)

        self.__configuration.notify_changed()

    def add_suite(self, suite):
        for benchmark in suite.benchmarks:
            benchmark_selected_parameter = BenchmarkSelectedParameter(benchmark)
            self.__parameters.append(benchmark_selected_parameter)

            benchmark_proportion_parameter = BenchmarkProportionParameter(benchmark)
            self.__parameters.append(benchmark_proportion_parameter)

        for parameter in suite.parameters:
            suite_parameter = BenchmarkSuiteParameter(suite, parameter)
            self.__parameters.append(suite_parameter)

        self.__configuration.notify_changed()

    def remove_suite(self, suite):
        parameter_name_prefix = suite.name + '.'
        self.__parameters = \
            list(filter(lambda parameter: parameter.name.startswith(parameter_name_prefix),
                        self.__parameters))

        self.__configuration.notify_changed()

    def set(self, parameters):
        for parameter in self.__parameters:
            if parameter.name in parameters.keys():
                parameter.value = parameters[parameter.name]

        self.__configuration.notify_changed()
