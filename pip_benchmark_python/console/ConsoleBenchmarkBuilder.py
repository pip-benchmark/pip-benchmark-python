# -*- coding: utf-8 -*-

from ..runner.BenchmarkBuilder import BenchmarkBuilder
from ..runner.BenchmarkRunner import BenchmarkRunner
from .CommandLineArgs import CommandLineArgs
from .ConsoleEventPrinter import ConsoleEventPrinter


class ConsoleBenchmarkBuilder(BenchmarkBuilder):

    def configured_with_args(self, args):
        _args = None

        if isinstance(args, CommandLineArgs):
            _args = args
        else:
            _args = CommandLineArgs(args)

        # Load modules
        for module in _args.modules:
            self._runner.benchmarks.add_suites_from_module(module)

        # Load test suites classes
        for clazz in _args.classes:
            self._runner.benchmarks.add_suite_from_class(clazz)

        # Load configuration
        if bool(_args.parameters):
            self._runner.parameters.set(_args.parameters)

        # Select benchmarks
        if len(_args.benchmarks) == 0:
            self._runner.benchmarks.select_all()
        else:
            self._runner.benchmarks.select_by_name(_args.benchmarks)

        # Configure benchmarking
        self._runner.configuration.measurement_type = _args.measurement_type
        self._runner.configuration.nominal_rate = _args.nominal_rate
        self._runner.configuration.execution_type = _args.execution_type
        self._runner.configuration.duration = _args.duration

        return self

    def create(self):
        _runner = super().create()
        ConsoleEventPrinter.attach(_runner)
        return _runner
