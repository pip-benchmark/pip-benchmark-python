# -*- coding: utf-8 -*-

import sys
import threading

from ..runner.BenchmarkRunner import BenchmarkRunner
from .CommandLineArgs import CommandLineArgs
from .ConsoleEventPrinter import ConsoleEventPrinter
from ..runner.config.ExecutionType import ExecutionType


class ConsoleRunner:

    def __init__(self):
        self._args = None
        self._runner = None

    def __start(self, args):
        self._args = CommandLineArgs(args)
        self._runner = BenchmarkRunner()

        ConsoleEventPrinter.attach(self._runner)

        self.__execute_batch_mode()

    def stop(self):
        self._runner.stop()

    def __execute_batch_mode(self):
        try:
            if self._args.show_help:
                self.print_help()
                return

            # Load modules
            for module in self._args.modules:
                self._runner.benchmarks.add_suites_from_module(module)

            # Load test suites classes
            for clazz in self._args.classes:
                self._runner.benchmarks.add_suite_from_class(clazz)

            # Load configuration
            if self._args.configuration_file is not None:
                self._runner.parameters.load_from_file(self._args.configuration_file)

            # Set parameters
            if not bool(self._args.parameters):
                self._runner.parameters.set(self._args.parameters)

            # Select benchmarks
            if len(self._args.benchmarks) == 0:
                self._runner.benchmarks.select_all()
            else:
                self._runner.benchmarks.select_by_name(self._args.benchmarks)

            if self._args.show_parameters:
                self.__print_parameters()
                return

            if self._args.show_benchmarks:
                self.__print_benchmarks()
                return

            # TODO err that
            def async_start(func):
                _thread = threading.Thread(target=func)
                _thread.start()
                _thread.join()

            # Benchmark the environment
            async_start(self.__benchmark_environment)

            # Configure benchmarking
            async_start(self.__configure_benchmarking)

        except Exception as err:
            raise err

    def __benchmark_environment(self):

        if self._args.measure_environment:
            print('Measuring Environment (wait up to 2 mins)...')
            self._runner.environment.measure(True, True, False)

        output = 'CPU: {}, Video: {}, Disk: {}'.format(
            str(int(round(self._runner.environment.cpu_measurement or 0))),
            str(int(round(self._runner.environment.video_measurement or 0))),
            str(int(round(self._runner.environment.disk_measurement or 0)))
        )
        print(output)

    def __configure_benchmarking(self):
        def inner(arg=None):
            if len(self._runner.results.all) > 0:
                print(str(int(round(
                    self._runner.results.all[0].performance_measurement.average_value
                ))))

            # Generate report and save to file
            if self._args.report_file:
                self._runner.report.save_to_file(self._args.report_file)

            # Show report in console
            if self._args.show_report:
                print(self._runner.report.generate())

        self._runner.configuration.measurement_type = self._args.measurement_type
        self._runner.configuration.nominal_rate = self._args.nominal_rate
        self._runner.configuration.execution_type = self._args.execution_type
        self._runner.configuration.duration = self._args.duration

        # Perform benchmarking
        self._runner.run(inner)

    def print_help(self):
        print("Pip.Benchmark Console Runner. (c) Conceptual Vision Consulting LLC 2020")
        print()
        print("Command Line Arguments:")
        print("-a <module>    - Module with benchmarks to be loaded. You may include multiple modules")
        print("-p <param>=<value> - Set parameter value. You may include multiple parameters")
        print("-b <benchmark>   - Name of benchmark to be executed. You may include multiple benchmarks")
        print("-c <config file> - File with parameters to be loaded")
        print("-r <report file> - File to save benchmarking report")
        print("-d <seconds>     - Benchmarking duration in seconds")
        print("-h               - Display this help screen")
        print("-B               - Show all available benchmarks")
        print("-P               - Show all available parameters")
        print("-R               - Show report")
        print("-e               - Measure environment")
        print("-x [prop|seq]    - Execution type: Proportional or Sequencial")
        print("-m [peak|nominal] - Measurement type: Peak or Nominal")
        print("-n <rate>        - Nominal rate in transactions per second")

    def __print_benchmarks(self):
        print('Pip.Benchmark Console Runner. (c) Conceptual Vision Consulting LLC 2017')
        print()
        print('Benchmarks:')

        suites = self._runner.benchmarks.suites
        for suite in suites:
            for benchmark in suite.benchmarks:
                print(benchmark.full_name + ' - ' + benchmark.description)

    def __print_parameters(self):
        print('Pip.Benchmark Console Runner. (c) Conceptual Vision Consulting LLC 2017')
        print()
        print('Parameters:')

        parameters = self._runner.parameters.user_defined

        for index in range(len(parameters)):
            parameter = parameters[index]
            default_value = parameter.default_value

            default_value = '' if default_value is None or len(
                default_value) == 0 else ' (Default: ' + default_value + ')'

            print('' + parameter.name + ' - ' + parameter.description + default_value)

    @staticmethod
    def run(args=None):
        runner = ConsoleRunner()

        # Log uncaught exceptions
        try:
            runner.__start(args or sys.argv)

            # Gracefully shutdown
            runner.stop()

        except Exception as err:

            # Process is terminated
            print('Process is terminated')
            raise err
