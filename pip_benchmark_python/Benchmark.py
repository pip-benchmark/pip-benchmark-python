# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from .IExecutionContext import IExecuteContext


class Benchmark(ABC):

    def __init__(self, name, description):
        self.__name = None
        self.__description = None
        self.__context = None
        self.__name = name
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, value):
        self.__context = value

    def set_up(self, callback):
        if callback:
            callback(None)

    @abstractmethod
    def execute(self, callback):
        """

        :param callback:
        """

    def tear_down(self, callback):
        callback(None)
