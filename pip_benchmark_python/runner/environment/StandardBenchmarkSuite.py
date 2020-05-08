# -*- coding: utf-8 -*-


from ...BenchmarkSuite import BenchmarkSuite
from .DefaultCpuBenchmark import DefaultCpuBenchmark
from .DefaultVideoBenchmark import DefaultVideoBenchmark
from .DefaultDiskBenchmark import DefaultDiskBenchmark


class StandardBenchmarkSuite(BenchmarkSuite):

    def __init__(self):
        super().__init__('StandatrBenchmark', 'Measures overall system performance')

        self.__cpu_benchmark = DefaultCpuBenchmark()
        self.add_benchmarks(self.__cpu_benchmark)

        self.__disk_benchmark = DefaultDiskBenchmark()
        self.add_benchmarks(self.__disk_benchmark)

        self.__video_benchmark = DefaultVideoBenchmark()
        self.add_benchmarks(self.__video_benchmark)

        self.create_parameter('FilePath', 'Path where test file is located on disk', '')
        self.create_parameter('FileSize', 'Size of the test file', '102400000')
        self.create_parameter('ChunkSize', 'Size of a chunk that read or writter from/to test file', '1024000')
        self.create_parameter('OperationTypes', 'Types of test operations: read, write or all', 'all')

    @property
    def cpu_benchmark(self):
        return self.__cpu_benchmark

    @property
    def disk_benchmark(self):
        return self.__disk_benchmark

    @property
    def video_benchmark(self):
        return self.__video_benchmark
