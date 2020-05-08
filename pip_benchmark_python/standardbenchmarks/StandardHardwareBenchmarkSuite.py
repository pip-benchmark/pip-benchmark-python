# -*- coding: utf-8 -*-

from ..BenchmarkSuite import BenchmarkSuite
from .StandardCpuBenchmark import StandardCpuBenchmark
from .StandardDiskBenchmark import StandardDiskBenchmark
from .StandardVideoBenchmark import StandardVideoBenchmark


class StandardHardwareBenchmarkSuite(BenchmarkSuite):

    def __init__(self):
        super().__init__("StandardBenchmark", "Standard hardware benchmark")

        self.__cpu_benchmark_test = None
        self.__disk_benchmark_test = None
        self.__video_benchmark_test = None

        self.__cpu_benchmark_test = StandardCpuBenchmark()
        self.add_benchmarks(self.__cpu_benchmark_test)

        self.__disk_benchmark_test = StandardDiskBenchmark()
        self.add_benchmarks(self.__disk_benchmark_test)

        self.__video_benchmark_test = StandardVideoBenchmark()
        self.add_benchmarks(self.__video_benchmark_test)

    @property
    def cpu_benchmark_test(self):
        return self.__cpu_benchmark_test

    @property
    def disk_benchmark_test(self):
        return self.__disk_benchmark_test

    @property
    def video_benchmark_test(self):
        return self.__video_benchmark_test
