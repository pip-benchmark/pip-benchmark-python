# -*- coding: utf-8 -*-

from .utilities.Converter import Converter


class Parameter:

    def __init__(self, name, description, default_value):
        self.__name = None
        self.__description = None
        self.__default_value = None
        self.__value = None

        self.__name = name
        self.__description = description
        self.__default_value = default_value

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def default_value(self):
        return self.__default_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def get_as_string(self):
        return self.value

    def get_as_nullable_string(self):
        return self.value

    def get_as_string_with_default(self, default_value):
        return self.value or default_value

    def set_as_string(self, value):
        self.value = value

    def get_as_boolean(self):
        return Converter.string_to_boolean(self.value, False)

    def get_as_nullable_boolean(self):
        return Converter.string_to_boolean(self.value, None)

    def get_as_boolean_with_default(self, default_value):
        return Converter.string_to_boolean(self.value, default_value)

    def set_as_boolean(self, value):
        self.value = Converter.boolean_to_string(value)

    def get_as_integer(self):
        return Converter.string_to_integer(self.value, 0)

    def get_as_nullable_integer(self):
        return Converter.string_to_integer(self.value, None)

    def get_as_integer_with_default(self, default_value):
        return Converter.string_to_integer(self.value, default_value)

    def set_as_integer(self, value):
        self.value = Converter.integer_to_string(value)

    def get_as_long(self):
        return Converter.string_to_long(self.value, 0)

    def get_as_nullable_long(self):
        return Converter.string_to_long(self.value, None)

    def get_as_long_with_default(self, default_value):
        return Converter.string_to_long(self.value, default_value)

    def set_as_long(self, value):
        self.value = Converter.long_to_string(value)

    def get_as_float(self):
        return Converter.string_to_float(self.value, 0)

    def get_as_nullable_float(self):
        return Converter.string_to_float(self.value, None)

    def get_as_float_with_default(self, default_value):
        return Converter.string_to_float(self.value, default_value)

    def set_as_float(self, value):
        self.value = Converter.float_to_string(self.value, 0)

    def get_as_double(self):
        return Converter.string_to_double(self.value, 0)

    def get_as_nullable_double(self):
        return Converter.string_to_double(self.value, None)

    def get_as_double_with_default(self, default_value):
        return Converter.string_to_double(self.value, default_value)

    def set_as_double(self, value):
        self.value = Converter.double_to_string(value)
