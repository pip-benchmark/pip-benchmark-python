# -*- coding: utf-8 -*-

from .Benchmark import Benchmark


class PassiveBenchmark(Benchmark):
    def __init__(self, name, description):
        super().__init__(name, description)

    def execute(self, callback):
        callback(Exception('Active measurement via Execute is not allow for passive benchmarks'))
