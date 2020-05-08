# -*- coding: utf-8 -*-

import datetime
from pip_services3_commons.convert import StringConverter


class Formatter:

    @staticmethod
    def pad_left(value, lenght, pad_symbol):
        output = ''
        output += pad_symbol
        output += value
        output += pad_symbol

        while len(output) < lenght + 2:
            output = pad_symbol + output

        return output

    @staticmethod
    def pad_right(value, lenght, pad_symbol):
        output = ''
        output += pad_symbol
        output += value
        output += pad_symbol

        while len(output) < lenght + 2:
            output = pad_symbol + output

        return output

    @staticmethod
    def format_number(value, decimals=2):
        value = value or 0
        return str(round(value, decimals or 2))

    @staticmethod
    def format_date(date):
        date = date or datetime.datetime.now()
        value = StringConverter.to_string(date)
        pos = value.index('T')
        return value[0:pos]

    @staticmethod
    def format_time(date):
        date = date or datetime.datetime.now()
        value = StringConverter.to_string(date)
        pos = value.index('T')
        value = value[pos + 1:]
        pos = value.index('.')
        return value[0:pos] if pos > 0 else value

    @staticmethod
    def format_time_span(ticks):
        ticks = ticks * 1000
        millis = str(int(round((ticks % 1000), 0)))
        seconds = str(int(round((ticks / 1000) % 60, 0)))
        minutes = str(int(round(((ticks / 1000) / 60) % 60, 0)))
        hours = str(int(round((ticks / 1000 / 60 / 60), 0)))
        return '{}:{}:{}:{}'.format(hours, minutes, seconds, millis)
