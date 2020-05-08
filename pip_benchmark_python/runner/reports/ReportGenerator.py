# -*- coding: utf-8 -*-

import datetime

from ..config.ConfigurationManager import ConfigurationManager
from ..results.ResultsManager import ResultsManager
from ..parameters.ParametersManager import ParametersManager
from ..benchmarks.BenchmarksManager import BenchmarksManager
from ..environment.EnvironmentManager import EnvironmentManager
from ..config.MeasurementType import MeasurementType
from ...utilities.Formatter import Formatter


class ReportGenerator:
    __SEPARATOR_LINE = '***************************************************************\n'
    __NEW_LINE = '\n'

    def __init__(self, configuration, results, parameters,
                 benchmarks, environment):
        self.__configuration = None
        self.__results = None
        self.__parameters = None
        self.__benchmarks = None
        self.__environment = None

        self.__configuration = configuration
        self.__results = results
        self.__parameters = parameters
        self.__benchmarks = benchmarks
        self.__environment = environment

    def generate(self):
        output = ''
        output += self.__generate_header()
        output += str(self.__generate_benchmark_list())

        if len(self.__results.all) > 1:
            output += self.__generate_multiple_results()
        else:
            output += self.__generate_single_result()

        output += self.__generate_system_info()
        output += self.__generate_system_benchmark()
        output += self.__generate_parameters()
        return output

    def save_to_file(self, filename):
        output = self.generate()
        with open(filename, "w", encoding='UTF-8') as file:
            file.write(output)

    def __generate_header(self):
        output = ''
        output += ReportGenerator.__SEPARATOR_LINE
        output += ReportGenerator.__NEW_LINE
        output += '             P E R F O R M A N C E    R E P O R T'
        output += ReportGenerator.__NEW_LINE
        output += ReportGenerator.__NEW_LINE
        output += '                 Generated by Pip.Benchmark'
        output += ReportGenerator.__NEW_LINE
        output += '                   ' \
                  'at {}, {}'.format(Formatter.format_date(datetime.datetime.now()),
                                     Formatter.format_time(datetime.datetime.now()))
        output += ReportGenerator.__NEW_LINE
        output += ReportGenerator.__SEPARATOR_LINE
        output += ReportGenerator.__NEW_LINE
        return output

    def __generate_benchmark_list(self):
        output = ''
        output += 'Executed Benchmarks:'
        output += ReportGenerator.__NEW_LINE
        index = 0
        for benchmark in self.__benchmarks.is_selected:
            index += 1
            output += '  {}. {}.{} [{}%]'.format(
                index, benchmark.suite.name, benchmark.name, 
                benchmark.proportion
            )
            output += ReportGenerator.__NEW_LINE
            return output

    def __generate_multiple_results(self):
        output = ''
        output += 'Benchmarking Results:'
        output += ReportGenerator.__NEW_LINE

        results = self.__results.all
        results_table = [[], []]

        # Fill column headers
        results_table[0][0] = 'Benchmark'
        results_table[0][1] = 'Performance (tps)'
        results_table[0][2] = 'CPU Load (%)'
        results_table[0][3] = 'Memory Usage (Mb)'

        column_sizes = [9, 17, 12, 17]

        for index in range(len(results)):
            results_table[index + 1][0] = results[index].benchmarks[0].full_name
            column_sizes[0] = max(len(results_table[index + 1][0]), column_sizes[0])

            results_table[index + 1][1] = Formatter.format_number(
                results[index].performance_measurement.average_value)
            column_sizes[1] = max(len(results_table[index + 1][1]), column_sizes[1])

            results_table[index + 1][2] = Formatter.format_number(
                results[index].performance_measurement.average_value)
            column_sizes[2] = max(len(results_table[index + 1][2]), column_sizes[2])

            results_table[index + 1][3] = Formatter.format_number(
                results[index].performance_measurement.average_value)
            column_sizes[3] = max(len(results_table[index + 1][3]), column_sizes[3])

        for row_index in range(len(results)):
            # Draw upper line
            if row_index == 0:
                output += '+'
                for column_index in range(4):
                    output += Formatter.pad_right('', column_sizes[column_index], '-')
                    output += '+'
                output += ReportGenerator.__NEW_LINE
            # Draw content
            output += '|'
            output += Formatter.pad_right(results_table[row_index][0], column_sizes[0], ' ')
            output += '|'
            output += Formatter.pad_left(results_table[row_index][1], column_sizes[1], ' ')
            output += '|'
            output += Formatter.pad_left(results_table[row_index][2], column_sizes[2], ' ')
            output += '|'
            output += Formatter.pad_left(results_table[row_index][3], column_sizes[3], ' ')
            output += '|'
            output += ReportGenerator.__NEW_LINE
            # Draw bottom line
            output += '+'
            for column_index in range(4):
                output += Formatter.pad_right('', column_sizes[column_index], '-')
                output += '+'
            output += ReportGenerator.__NEW_LINE
        output += ReportGenerator.__NEW_LINE
        return output

    def __generate_single_result(self):
        output = ''

        if len(self.__results.all) == 0:
            return output

        result = self.__results.all[0]

        output += 'Benchmarking Results:'
        output += ReportGenerator.__NEW_LINE
        if self.__configuration.measurement_type == MeasurementType.Peak:
            output += '  Measurement Type: Peak Performance'
        else:
            output += '  Measurement Type: Nominal Performance at {} tps'.format(self.__configuration.nominal_rate)

        output += ReportGenerator.__NEW_LINE

        start_time = datetime.datetime.fromtimestamp(result.start_time.timestamp())
        output += '  Start Time:   {}'.format(Formatter.format_time(start_time))
        output += ReportGenerator.__NEW_LINE
        end_time = result.start_time.timestamp() * 1000 + result.elapsed_time
        output += '  End Time:     {}'.format(Formatter.format_time_span(end_time))
        output += ReportGenerator.__NEW_LINE
        elapsed_time = result.elapsed_time
        output += '  Elapsed Time: {}'.format(Formatter.format_time_span(elapsed_time))
        output += ReportGenerator.__NEW_LINE
        output += '  Min Performance (tps):     {}'.format(
            Formatter.format_number(result.performance_measurement.min_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Average Performance (tps): {}'.format(
            Formatter.format_number(result.performance_measurement.average_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Max Performance (tps):     {}'.format(
            Formatter.format_number(result.performance_measurement.max_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Min CPU Load (%):          {}'.format(
            Formatter.format_number(result.cpu_load_measurement.min_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Average CPU Load (%):      {}'.format(
            Formatter.format_number(result.cpu_load_measurement.average_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Max CPU Load (%):          {}'.format(
            Formatter.format_number(result.cpu_load_measurement.max_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Min Memory Usage (Mb):     {}'.format(
            Formatter.format_number(result.memory_usage_measurement.min_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Average Memory Usage (Mb): {}'.format(
            Formatter.format_number(result.memory_usage_measurement.average_value))
        output += ReportGenerator.__NEW_LINE
        output += '  Max Memory Usage (Mb):     {}'.format(
            Formatter.format_number(result.memory_usage_measurement.max_value))
        output += ReportGenerator.__NEW_LINE
        output += ReportGenerator.__NEW_LINE

        return output

    def __generate_system_info(self):
        output = ''
        output += 'System Information:'
        output += ReportGenerator.__NEW_LINE
        for prop in self.__environment.system_info.keys():
            value = self.__environment.system_info[prop]
            output += '  {}: {}'.format(prop, value)
            output += ReportGenerator.__NEW_LINE

        output += ReportGenerator.__NEW_LINE
        return output

    def __generate_system_benchmark(self):
        output = ''
        output += 'System Benchmarking:'
        output += ReportGenerator.__NEW_LINE
        output += '  CPU Performance (MFLOP/s): {}'.format(
            Formatter.format_number(self.__environment.cpu_measurement))
        output += ReportGenerator.__NEW_LINE
        output += '  Video Performance (GOP/s): {}'.format(
            Formatter.format_number(self.__environment.video_measurement))
        output += ReportGenerator.__NEW_LINE
        output += '  Disk Performance (MB/s):   {}'.format(
            Formatter.format_number(self.__environment.disk_measurement))
        output += ReportGenerator.__NEW_LINE
        output += ReportGenerator.__NEW_LINE
        return output

    def __generate_parameters(self):
        output = ''
        output += 'Parameters:'
        output += ReportGenerator.__NEW_LINE
        for parameter in self.__parameters.all:
            output += ' {}={}'.format(parameter.name, parameter.value)
            output += ReportGenerator.__NEW_LINE

        output += ReportGenerator.__NEW_LINE
        return output
