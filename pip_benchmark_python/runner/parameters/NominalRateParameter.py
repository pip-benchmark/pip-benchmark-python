# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ...utilities.Converter import Converter
from ..config.ConfigurationManager import ConfigurationManager


class NominalRateParameter(Parameter):

    def __init__(self, configuration):
        super().__init__(
            'General.Benchmarking.NominalRate',
            'Rate for nominal benchmarking in TPS',
            '1'
        )

        self.__configuration = configuration

    @property
    def value(self):
        return Converter.double_to_string(self.__configuration.nominal_rate)

    @value.setter
    def value(self, value):
        self.__configuration.nominal_rate = Converter.string_to_double(value, 1)
