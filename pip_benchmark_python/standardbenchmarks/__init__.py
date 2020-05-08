# -*- coding: utf-8 -*-

__all__ = [
    'StandardVideoBenchmark', 'StandardCpuBenchmark', 'StandardDiskBenchmark',
    'StandardHardwareBenchmarkSuite', 'UtilityBenchmarkSuite'
]

from .StandardVideoBenchmark import StandardVideoBenchmark
from .StandardHardwareBenchmarkSuite import StandardHardwareBenchmarkSuite
from .StandardDiskBenchmark import StandardDiskBenchmark
from .StandardCpuBenchmark import StandardCpuBenchmark
from .UtilityBenchmarkSuite import UtilityBenchmarkSuite
