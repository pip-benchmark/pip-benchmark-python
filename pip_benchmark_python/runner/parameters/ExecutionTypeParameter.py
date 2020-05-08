# -*- coding: utf-8 -*-

from ...Parameter import Parameter
from ..config.ExecutionType import ExecutionType
from ..config.ConfigurationManager import ConfigurationManager


class ExecutionTypeParameter(Parameter):

    def __init__(self, configuration):
        super().__init__(
            'General.Benchmarking.ExecutionType',
            'Execution type: proportional or sequencial',
            'Proportional'
        )

        self.__configuration = configuration

    @property
    def value(self):
        self.__configuration.execution_type = 'Proportional' if ExecutionType.Proportional else 'Sequencial'
        return self.__configuration.execution_type

    @value.setter
    def value(self, value):
        value = value.lower()
        self.__configuration.execution_type = \
            ExecutionType.Proportional if value.startswith('p') else ExecutionType.Sequential
