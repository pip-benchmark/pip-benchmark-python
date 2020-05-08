# -*- coding: utf-8 -*-

import os
import re

from .PropertyFileLine import PropertyFileLine
from .Converter import Converter


class Properties(dict):

    def __init__(self):
        super().__init__()
        self.lines = list()

    def load_from_file(self, file):
        if file:
            with open(file, "r", encoding='UTF-8') as file:
                lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for index in range(len(lines)):
                line = PropertyFileLine(lines[index])
                self.lines.append(line)

            self.__populate_items()

    def __populate_items(self):
        for prop in self.__dict__.keys():
            if prop != 'lines':
                delattr(self, prop)

        for line in self.lines:
            if line.key is not None and len(line.key) > 0:
                self[line.key] = line.value

    def save_to_file(self, file):
        self.__synchronize_items()

        content = ''
        for line in self.lines:
            content += line.line + os.linesep

        with open(file, "w", encoding='UTF-8') as file:
            file.write(content)

    def __find_line(self, key):
        for line in self.lines:
            if key == line.key:
                return line
        return None

    def __synchronize_items(self):
        # Update existing values and create missing lines
        for prop in dir(self):
            if not hasattr(self, prop):
                continue
            if prop == 'lines':
                continue
            line = self.__find_line(prop)
            if line is not None:
                line.value += self.__getattribute__(prop)

            else:
                line = PropertyFileLine(prop, str(self.__getattribute__(prop)), None)
                self.lines.append(line)

        # Remove lines mismatched with listed keys
        index = len(self.lines) - 1
        while index >= 0:
            line = self.lines[index]
            if line.key is not None and not hasattr(self, line.key):
                del self.lines[index]
            index -= 1

    def get_as_string(self, key, value):
        self.__dict__[key] = value

    def get_as_integer(self, key, default_value):
        value = self.__getattribute__(key)
        if value is None:
            return default_value
        return Converter.string_to_integer(value, default_value)

    def set_as_integer(self, key, value):
        self.__dict__[key] = Converter.integer_to_string(value)

    def get_as_long(self, key, default_value):
        value = self.__getattribute__(key)
        if value is None:
            return default_value
        return Converter.string_to_long(value, default_value)

    def set_as_long(self, key, value):
        self.__dict__[key] = Converter.long_to_string(value)

    def get_as_double(self, key, default_value):
        value = self.__getattribute__(key)
        if value is None:
            return default_value
        return Converter.string_to_double(value, default_value)

    def set_as_double(self, key, value):
        self.__dict__[key] = Converter.double_to_string(value)

    def get_as_boolean(self, key, default_value):
        value = self.__getattribute__(key)
        if value is None:
            return default_value
        return Converter.string_to_boolean(value, default_value)

    def set_as_boolean(self, key, value):
        self.__dict__[key] = Converter.boolean_to_string(value)
