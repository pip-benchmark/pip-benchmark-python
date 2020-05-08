# -*- coding: utf-8 -*-

import threading

from pip_benchmark_python.standardbenchmarks.StandardCpuBenchmark import StandardCpuBenchmark


class TestStandardCpuBenchmark:
    benchmark = None

    def callback(self, arg=None):
        print('Is Done!')

    def setup_method(self):
        self.benchmark = StandardCpuBenchmark()
        self.benchmark.set_up(None)

    def teardown_method(self):
        self.benchmark.tear_down(self.callback)

    def test_execute(self):
        threads = []

        active_threads = threading.active_count()

        for i in range(100):
            threads.append(threading.Thread(
                target=lambda: self.benchmark.execute(None),
            ))
            threads[-1].start()

        for th in threads:  # waiting for all threads
            th.join()

        assert active_threads == threading.active_count()
