# -*- coding: utf-8 -*-

from pip_benchmark_python.utilities.PropertyFileLine import PropertyFileLine


class TestPropertyFileLine:

    def test_composite(self):
        line = PropertyFileLine('Key', 'Value', 'Comment')

        assert 'Key' == line.key
        assert 'Value' == line.value
        assert 'Comment' == line.comment
        assert 'Key=Value ;Comment' == line.line

    def test_parse_key(self):
        line = PropertyFileLine('Key')
        assert 'Key' == line.key
        assert '' == line.value
        assert None == line.comment

    def test_parse_key_value(self):
        line = PropertyFileLine('Key=Value')
        assert 'Key' == line.key
        assert 'Value' == line.value
        assert line.comment is None

        line = PropertyFileLine("Key='Value'")
        assert 'Key' == line.key
        assert 'Value' == line.value
        assert line.comment is None

        line = PropertyFileLine('Key="Value"')
        assert 'Key' == line.key
        assert 'Value' == line.value
        assert line.comment is None

    def test_parse_full_line(self):
        line = PropertyFileLine('Key=Value;Comment')
        assert 'Key' == line.key
        assert 'Value' == line.value
        assert 'Comment' == line.comment
