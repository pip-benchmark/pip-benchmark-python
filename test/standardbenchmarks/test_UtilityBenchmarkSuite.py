# -*- coding: utf-8 -*-

import threading

from pip_benchmark_python.standardbenchmarks.UtilityBenchmarkSuite import UtilityBenchmarkSuite


class TestUtilityBenchmarkSuite:
    suite = None

    def setup_method(self):
        self.suite = UtilityBenchmarkSuite()
        self.suite.set_up(None)

    def teardown_method(self):
        self.suite.tear_down(None)

    def test_empty_benchmark(self):
        assert 2 == len(self.suite.benchmarks)
        benchmark = self.suite.benchmarks[0]

        threads = []

        active_threads = threading.active_count()

        for i in range(100):
            threads.append(threading.Thread(target=lambda: benchmark.execute(None), ))
            threads[-1].start()
        for th in threads:  # waiting for all threads
            th.join()

        assert active_threads == threading.active_count()

    def test_random_benchmark(self):
        assert 2 == len(self.suite.benchmarks)
        benchmark = self.suite.benchmarks[1]
        active_threads = threading.active_count()

        th = threading.Thread(target=lambda: benchmark.execute)
        th.start()
        th.join()

        assert active_threads == threading.active_count()
