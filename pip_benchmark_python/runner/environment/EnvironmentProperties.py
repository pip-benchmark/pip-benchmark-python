# -*- coding: utf-8 -*-

import os

from ...utilities.Properties import Properties


class EnvironmentProperties(Properties):

    def __get_file_path(self):
        return 'BenchmarkEnvironment.properties'

    @property
    def cpu_benchmark(self):
        return super().get_as_double('CpuBenchmark', 0)

    @cpu_benchmark.setter
    def cpu_benchmark(self, value):
        super().set_as_double('CpuBenchmark', value)

    @property
    def disk_benchmark(self):
        return super().get_as_double('DiskBenchmark', 0)

    @disk_benchmark.setter
    def disk_benchmark(self, value):
        super().set_as_double('DiskBenchmark', value)

    @property
    def video_benchmark(self):
        return super().get_as_double('VideoBenchmark', 0)

    @video_benchmark.setter
    def video_benchmark(self, value):
        super().set_as_double('VideoBenchmark', value)

    def load(self):
        if os.path.exists(self.__get_file_path()):
            self.load_from_file(self.__get_file_path())

    def save(self):
        self.save_to_file(self.__get_file_path())

