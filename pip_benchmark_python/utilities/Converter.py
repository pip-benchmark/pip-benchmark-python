# -*- coding: utf-8 -*-


class Converter:

    @staticmethod
    def string_to_integer(value, default_value):
        return Converter.string_to_long(value, default_value)

    @staticmethod
    def integer_to_string(value):
        return Converter.long_to_string(value)

    @staticmethod
    def string_to_long(value, default_value):
        if value is None:
            return default_value
        try:
            if value.find('.'):
                value = value.split('.')[0]
            elif value.find(','):
                value = value.split(',')[0]
            return int(value)

        except ValueError:
            return default_value

    @staticmethod
    def long_to_string(value):
        return str(value) if value is not None else None

    @staticmethod
    def string_to_float(value, default_value):
        return Converter.string_to_double(value, default_value)

    @staticmethod
    def float_to_string(value):
        return Converter.double_to_string(value)

    @staticmethod
    def string_to_double(value, default_value):
        if value is None:
            return default_value
        try:
            if value.find(','):
                value = value.split(',')[0]
                return float(value)
        except ValueError:
            return default_value

    @staticmethod
    def double_to_string(value):
        return str(value) if value is not None else None

    @staticmethod
    def string_to_boolean(value, default_value):
        # Process nulls or empty strings
        if value is None or len(value) == 0:
            return default_value

        # Process single characters
        if len(value) == 1:
            if value[0] in ['1', 'T', 'Y', 't', 'y']:
                return True
            if value[0] in ['0', 'F', 'N', 'f', 'n']:
                return False

        # Process strings
        value = value.upper()
        if value == 'TRUE' or value == 'YES':
            return True
        if value == 'FALSE' or value == 'NO':
            return False

        return default_value

    @staticmethod
    def boolean_to_string(value):
        return 'true' if value else 'false'

