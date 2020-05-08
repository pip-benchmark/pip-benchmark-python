# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ...utilities.Converter import Converter
from ..benchmarks.BenchmarkInstance import BenchmarkInstance


class BenchmarkSelectedParameter(Parameter):

    def __init__(self, benchmark):
        super().__init__(
            '{}.{}.Proportion'.format(benchmark.suite.name, benchmark.name),
            'Sets execution proportion for benchmark {} in suite {}'.format(benchmark.name, benchmark.suite.name),
            'true'
        )

        self.__benchmark = benchmark

    @property
    def value(self):
        return Converter.boolean_to_string(self.__benchmark.is_selected)

    @value.setter
    def value(self, value):
        self.__benchmark.is_selected = Converter.string_to_boolean(value, False)
