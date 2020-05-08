# -*- coding: utf-8 -*-

import threading

from pip_benchmark_python.runner.execution.MemoryUsageMeter import MemoryUsageMeter


class TestMemoryUsageMeter:
    def test_measure(self):
        meter = MemoryUsageMeter()
        measure = meter.measure()
        assert measure > 0

        def _test_measure():
            _measure = meter.measure()
            assert _measure > 0

        threading.Timer(100 / 1000, _test_measure)
