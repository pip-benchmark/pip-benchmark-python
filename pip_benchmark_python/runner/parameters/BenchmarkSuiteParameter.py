# -*- coding: utf-8 -*-


from ...Parameter import Parameter
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance


class BenchmarkSuiteParameter(Parameter):

    def __init__(self, suite, original_parameter):
        super().__init__(
            '{}.{}'.format(suite.name, original_parameter.name),
            original_parameter.description, original_parameter.default_value
        )

        self.__original_parameter = original_parameter

    @property
    def value(self):
        return self.__original_parameter.value

    @value.setter
    def value(self, value):
        self.__original_parameter.value = value
