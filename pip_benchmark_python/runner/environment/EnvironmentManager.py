# -*- coding: utf-8 -*-

import threading

from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from ..execution.ExecutionManager import ExecutionManager
from .EnvironmentProperties import EnvironmentProperties
from ..benchmarks.BenchmarkSuiteInstance import BenchmarkSuiteInstance
from .StandardBenchmarkSuite import StandardBenchmarkSuite
from .SystemInfo import SystemInfo


class EnvironmentManager(ExecutionManager):
    __DURATION = 5

    def __init__(self):
        self.__cpu_measurement = None
        self.__video_measurement = None
        self.__disk_measurement = None

        configuration = ConfigurationManager()
        configuration.duration = EnvironmentManager.__DURATION

        results = ResultsManager()

        super().__init__(configuration, results)

        try:
            self.__load()
        except Exception as err:
            # Ignore. it shall never happen here...
            pass

    @property
    def system_info(self):
        return SystemInfo()

    @property
    def cpu_measurement(self):
        return self.__cpu_measurement

    @property
    def video_measurement(self):
        return self.__video_measurement

    @property
    def disk_measurement(self):
        return self.__disk_measurement

    def measure(self, cpu, disk, video):

        def async_start(func):
            _thread = threading.Thread(target=func)
            _thread.start()
            _thread.join()

        try:
            if cpu:
                async_start(self.__measure_cpu)

            if disk:
                async_start(self.__measure_disk)

            if video:
                async_start(self.__measure_video)

            self.__save()
        except Exception as err:
            raise err
        finally:
            self.stop()

    def __load(self):
        properties = EnvironmentProperties()
        properties.load()

        self.__cpu_measurement = properties.get_as_double('CpuMeasurement', 0)
        self.__video_measurement = properties.get_as_double('VideoMeasurement', 0)
        self.__disk_measurement = properties.get_as_double('DiskMeasurement', 0)

    def __save(self):

        properties = EnvironmentProperties()

        properties.set_as_double('CpuMeasurement', self.__cpu_measurement)
        properties.set_as_double('VideoMeasurement', self.video_measurement)
        properties.set_as_double('DiskMeasurement', self.__disk_measurement)

        properties.save()

    def __measure_cpu(self):
        suite = StandardBenchmarkSuite()
        instance = BenchmarkSuiteInstance(suite)

        instance.unselect_all()
        instance.select_by_name(suite.cpu_benchmark.name)
        try:
            self.run(instance.is_selected)
            result = self._results.all[0].performance_measurement.average_value if len(self._results.all) else 0
            self.__cpu_measurement = result
        except Exception as err:
            raise err

    def __measure_disk(self):
        suite = StandardBenchmarkSuite()
        instance = BenchmarkSuiteInstance(suite)

        instance.unselect_all()
        instance.select_by_name(suite.disk_benchmark.name)
        try:
            self.run(instance.is_selected)
            result = self._results.all[0].performance_measurement.average_value if len(self._results.all) else 0
            self.__disk_measurement = result
        except Exception as err:
            raise err

    def __measure_video(self):
        suite = StandardBenchmarkSuite()
        instance = BenchmarkSuiteInstance(suite)

        instance.unselect_all()
        instance.select_by_name(suite.video_benchmark.name)

        try:
            self.run(instance.is_selected)
            result = self._results.all[0].performance_measurement.average_value if len(self._results.all) else 0
            self.__video_measurement = result
        except Exception as err:
            raise err
