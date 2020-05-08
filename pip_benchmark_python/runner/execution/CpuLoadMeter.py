# -*- coding: utf-8 -*-

import datetime
import psutil

from .BenchmarkMeter import BenchmarkMeter


class CpuLoadMeter(BenchmarkMeter):

    def __init__(self):
        super().__init__()
        self.__last_total_idle = None
        self.__last_total = None

    def clear(self):
        self.__last_total_idle = None
        self.__last_total = None

        super().clear()

    def _perform_measurement(self):
        # Initialize current values
        current_time = datetime.datetime.now().timestamp()
        current_total_idle = 0
        current_total = 0

        # Calculate current values
        cups = psutil.cpu_times(True)
        cpu_count = len(psutil.cpu_times(True))
        for index in range(cpu_count):
            cpu = cups[index]
            for i in range(len(cpu)):
                current_total += cpu[i]
            current_total += cpu.idle
        current_total = current_total / cpu_count
        current_total_idle = current_total_idle / cpu_count

        # Calculate CPU usage
        result = 0
        if self._last_measured_time is not None:
            elapsed = current_time - self._last_measured_time * 1000
            # Calculate only for 100 ms or more
            if elapsed > 100:
                total_difference = current_total - self.__last_total
                idle_difference = current_total_idle - self.__last_total
                result = 100 - (100 * idle_difference / total_difference)
        # Save current values as last values
        self._last_measured_time = current_time
        self.__last_total_idle = current_total_idle
        self.__last_total = current_total

        return result
