# -*- coding: utf-8 -*-

import datetime
import sys

from pip_services3_commons.convert import StringConverter

from ..runner.BenchmarkRunner import BenchmarkRunner
from ..runner.results.BenchmarkResult import BenchmarkResult
from ..runner.execution.ExecutionState import ExecutionState


class ConsoleEventPrinter:

    @staticmethod
    def attach(runner):
        runner.execution.add_updated_listener(ConsoleEventPrinter.on_state_updated)
        runner.results.add_error_listener(ConsoleEventPrinter.on_error_reported)
        runner.results.add_message_listener(ConsoleEventPrinter.on_message_sent)
        runner.results.add_updated_listener(ConsoleEventPrinter.on_result_updated)

    @staticmethod
    def on_state_updated(state):
        if state == ExecutionState.Running:
            print('Measuring....')
        elif state == ExecutionState.Completed:
            print('Completed measuring.')

    @staticmethod
    def on_result_updated(result):
        if result is not None:
            output = '{} Performance: {} {}>{}>{} CPU Load: {} {}>{}>{} Errors: {}'.format(
                StringConverter.to_string(datetime.datetime.now()),
                str(round(result.performance_measurement.current_value, 2)),
                str(round(result.performance_measurement.min_value, 2)),
                str(round(result.performance_measurement.average_value, 2)),
                str(round(result.performance_measurement.max_value, 2)),
                str(round(result.cpu_load_measurement.current_value, 2)),
                str(round(result.cpu_load_measurement.min_value, 2)),
                str(round(result.cpu_load_measurement.average_value, 2)),
                str(round(result.cpu_load_measurement.max_value, 2)),
                len(result.errors)
            )
            print(output)

    @staticmethod
    def on_message_sent(message):
        print(message)

    @staticmethod
    def on_error_reported(message):
        sys.stderr.write(message)
