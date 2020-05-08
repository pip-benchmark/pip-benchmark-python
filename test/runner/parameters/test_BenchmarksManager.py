# -*- coding: utf-8 -*-

from pip_benchmark_python.runner.BenchmarkRunner import BenchmarkRunner


class TestBenchmarksManager:
    def test_load_suites(self):
        runner = BenchmarkRunner()
        benchmarks = runner.benchmarks

        assert 0 == len(benchmarks.suites)
        benchmarks.add_suites_from_module('./pip_benchmark_python/standardbenchmarks')
        assert 2 == len(benchmarks.suites)

    def test_add_suite_from_class(self):
        runner = BenchmarkRunner()
        benchmarks = runner.benchmarks

        assert 0 == len(benchmarks.suites)
        benchmarks.add_suite_from_class('../pip_benchmark_python/standardbenchmarks, UtilityBenchmarkSuite')
        assert 1 == len(benchmarks.suites)

    def test_select_all(self):
        runner = BenchmarkRunner()
        benchmarks = runner.benchmarks
        benchmarks.add_suites_from_module('./pip_benchmark_python/standardbenchmarks')
        assert 0 == len(benchmarks.is_selected)
        runner.benchmarks.select_all()
        assert 5 == len(benchmarks.is_selected)

        benchmarks.unselect_all()
        assert 0 == len(benchmarks.is_selected)

    def test_select_benchmark_by_name(self):
        runner = BenchmarkRunner()
        benchmarks = runner.benchmarks

        benchmarks.add_suites_from_module('./pip_benchmark_python/standardbenchmarks')

        assert 0 == len(benchmarks.is_selected)

        benchmarks.select_by_name(['Utility.Empty'])
        assert 1 == len(benchmarks.is_selected)

        benchmarks.unselect_by_name(['Utility.Empty'])
        assert 0 == len(benchmarks.is_selected)
