# -*- coding: utf-8 -*-

import datetime

from .Measurement import Measurement
from ..benchmarks.BenchmarkInstance import BenchmarkInstance


class BenchmarkResult:

    def __init__(self):
        self.benchmarks = []
        self.start_time = datetime.datetime.now()
        self.elapsed_time = 0
        self.performance_measurement = Measurement(0, 0, 0, 0)
        self.cpu_load_measurement = Measurement(0, 0, 0, 0)
        self.memory_usage_measurement = Measurement(0, 0, 0, 0)
        self.errors = []
