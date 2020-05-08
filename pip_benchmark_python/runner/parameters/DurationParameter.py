# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ...utilities.Converter import Converter
from ..config.ConfigurationManager import ConfigurationManager


class DurationParameter(Parameter):

    def __init__(self, configuration):
        super().__init__(
            'General.Benchmarking.Duration',
            'Duration of benchmark execution in seconds',
            '60'
        )

        self.__configuration = configuration

    @property
    def value(self):
        return Converter.integer_to_string(self.__configuration.duration)

    @value.setter
    def value(self, value):
        self.__configuration.duration = Converter.string_to_integer(value, 60)
