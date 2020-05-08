# -*- coding: utf-8 -*-

import psutil

from .BenchmarkMeter import BenchmarkMeter


class MemoryUsageMeter(BenchmarkMeter):

    def __init__(self):
        super().__init__()

    def _perform_measurement(self):
        mem = psutil.virtual_memory()
        return (mem.total - mem.free) / 1024 / 1024
