# -*- coding: utf-8 -*-

from .Benchmark import Benchmark


class DelegatedBenchmark(Benchmark):


    def __init__(self, name, description, execute_callback):
        super().__init__(name, description)
        self.__execute_callback = None
        if execute_callback is None:
            raise Exception('Execute callback cannot be null')

        self.__execute_callback = execute_callback

    def execute(self, callback):
        self.__execute_callback(callback)
