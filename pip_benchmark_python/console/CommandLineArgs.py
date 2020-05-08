# -*- coding: utf-8 -*-

from ..runner.config.MeasurementType import MeasurementType
from ..runner.config.ExecutionType import ExecutionType
from ..utilities.Converter import Converter


class CommandLineArgs:

    def __init__(self, args):
        self.modules = []
        self.classes = []
        self.benchmarks = []
        self.parameters = {}
        self.configuration_file = str()
        self.report_file = 'BenchmarkReport.txt'
        self.duration = 60
        self.show_help = False
        self.show_benchmarks = False
        self.show_parameters = False
        self.show_report = False
        self.measure_environment = False
        self.measurement_type = MeasurementType.Peak
        self.execution_type = ExecutionType.Proportional
        self.nominal_rate = 1

        self.__process_arguments(args)

    def __process_arguments(self, args):
        index = 1
        while index < len(args):
            arg = args[index]
            more_args = index < len(args)
            if (arg == '-a' or arg == '-j' or arg == '--module') and more_args:
                module = args[index + 1]
                self.modules.append(module)
            elif (arg == '-l' or arg == '--class') and more_args:
                clazz = args[index + 1]
                self.classes.append(clazz)
            elif (arg == '-b' or arg == '--benchmark') and more_args:
                benchmark = args[index + 1]
                self.benchmarks.append(benchmark)
            elif (arg == '-p' or arg == '--param') and more_args:
                param = args[index + 1]
                pos = param.index('=')
                key = param[0:pos - 1] if pos > 0 else param
                value = param[pos - 1] if pos > 0 else None
                self.parameters[key] = value
            elif (arg == '-c' or arg == '--config') and more_args:
                self.configuration_file = args[index + 1]
            elif (arg == '-r' or arg == '--report') and more_args:
                self.report_file = args[index + 1]
            elif (arg == '-d' or arg == '--duration') and more_args:
                self.duration = Converter.string_to_long(args[index + 1], 60)
            elif (arg == '-m' or arg == '--measure') and more_args:
                measure = args[index + 1].lower()
                self.measurement_type = MeasurementType.Nominal if measure.startswith('nom') else MeasurementType.Peak
            elif (arg == '-x' or arg == '--execute') and more_args:
                execution = args[index + 1].lower()
                self.execution_type = ExecutionType.Sequential if execution.startswith(
                    'seq') else ExecutionType.Proportional
            elif (arg == '-n' or arg == '--nominal') and more_args:
                self.nominal_rate = Converter.string_to_double(args[index + 1], 1)
            elif (arg == '-h' or arg == '--help') and more_args:
                self.show_help = True
            elif arg == '-B' or arg == '--show-benchmarks':
                self.show_benchmarks = True
            elif arg == '-P' or arg == '--show-params':
                self.show_parameters = True
            elif arg == '-R' or arg == '--show-report':
                self.show_report = True
            elif arg == '-e' or arg == '--environment':
                self.measure_environment = True

            index += 1
