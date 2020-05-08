# -*- coding: utf-8 -*-

from pip_benchmark_python.utilities.Converter import Converter


class TestConverter:

    def test_long_to_string(self):
        assert Converter.long_to_string(None) is None
        assert '123' == Converter.long_to_string(123)

    def test_string_to_long(self):
        assert 0 == Converter.string_to_long(None, 0)
        assert 0 == Converter.string_to_long('ABC', 0)
        assert 123 == Converter.string_to_long('123', 0)

    def test_double_to_string(self):
        assert Converter.double_to_string(None) is None
        assert '123.456' == Converter.double_to_string(123.456)

    def test_string_to_double(self):
        assert 0 == Converter.string_to_double(None, 0)
        assert 0 == Converter.string_to_double('ABC', 0)
        assert 123.456 == Converter.string_to_double('123.456', 0)

    def test_boolean_to_string(self):
        assert 'false' == Converter.boolean_to_string(None)
        assert 'true' == Converter.boolean_to_string(True)

    def test_string_to_boolean(self):
        assert False is Converter.string_to_boolean(None, False)
        assert True is Converter.string_to_boolean('True', False)
        assert True is Converter.string_to_boolean('1', False)
        assert True is Converter.string_to_boolean('T', False)
