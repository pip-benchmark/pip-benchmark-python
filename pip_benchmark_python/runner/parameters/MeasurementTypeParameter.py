# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ..config.MeasurementType import MeasurementType
from ..config.ConfigurationManager import ConfigurationManager


class MeasurementTypeParameter(Parameter):

    def __init__(self, configuration):
        super().__init__(
            'General.Benchmarking.MeasurementType',
            'Performance type: peak or nominal',
            'Peak'
        )

        self.__configuration = configuration

    @property
    def value(self):
        if self.__configuration.measurement_type == 'Peak':
            return 'Peak'
        else:
            return 'Nominal'

    @value.setter
    def value(self, value):
        value = value.lower()
        self.__configuration.measurement_type = MeasurementType.Peak if value.startswith('p') else MeasurementType.Nominal
        