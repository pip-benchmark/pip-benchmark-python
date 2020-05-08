# -*- coding: utf-8 -*-

from pip_benchmark_python.utilities.Properties import Properties


class TestProperties:

    def test_load(self):
        props = Properties()
        props.load_from_file('./data/test.properties')

        assert 4 == len(props.lines)
        print(props.keys())
        assert '' == props['Key1']
        assert 'Value2' == props['Key2']
        assert '"Value 3"' == props['Key3']
