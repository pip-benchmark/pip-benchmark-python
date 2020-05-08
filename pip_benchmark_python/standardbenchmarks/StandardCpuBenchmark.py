# -*- coding: utf-8 -*-

import math

from ..Benchmark import Benchmark


class StandardCpuBenchmark(Benchmark):
    __number_of_attempts = 20000

    def __init__(self):
        super().__init__('CPU', 'Measures CPU speed by running arithmetical operations')

    def execute(self, callback):
        # Count increment, comparison and goto for 1 arithmetic operation
        for value in range(1, StandardCpuBenchmark.__number_of_attempts + 1):
            # 1
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 2
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 3
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 4
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 5
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 6
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 7
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 8
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 9
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

            # 10
            result1 = value + value
            result2 = result1 - value
            result3 = result1 * result2
            result4 = result2 / result3
            math.log(result4)

        if callback:
            callback(None)
