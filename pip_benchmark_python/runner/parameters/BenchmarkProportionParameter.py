# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ...utilities.Converter import Converter
from ..benchmarks.BenchmarkInstance import BenchmarkInstance


class BenchmarkProportionParameter(Parameter):
    __benchmark = None

    def __init__(self, benchmark):
        super().__init__(
            '{}.{}.Proportion'.format(benchmark.suite.name, benchmark.name),
            'Sets execution proportion for benchmark {} in suite {}'.format(benchmark.name, benchmark.suite.name),
            '100'
        )
        self.__benchmark = benchmark

    @property
    def value(self):
        return Converter.integer_to_string(self.__benchmark.proportion)

    @value.setter
    def value(self, value):
        self.__benchmark.proportion = Converter.string_to_integer(value, 100)
