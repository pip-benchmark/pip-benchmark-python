# -*- coding: utf-8 -*-


class PropertyFileLine:

    def __init__(self, key, value=None, comment=None):
        self.__line = None
        self.__key = None
        self.__value = None
        self.__comment = None

        if value is None and comment is None:
            self.__parse_line(key)
        else:
            self.__key = key
            self.__value = value
            self.__comment = comment
            self.__compose_new_line()

    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.__compose_new_line()

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value
        self.__compose_new_line()

    @property
    def line(self):
        return self.__line

    def __compose_new_line(self):
        self.__line = ''
        if self.__key is not None and len(self.__key) > 0:
            self.__line += self.__encode_value(self.__key)
            self.__line += '='
            self.__line += self.__encode_value(self.__value)

        if self.__comment is not None and len(self.__comment) > 0:
            self.__line += ' ;'
            self.__line += self.__comment

    def __parse_line(self, line):
        self.__line = line

        # Parse comment
        comment_index = self.__index_of_comment(line)
        if comment_index >= 0:
            self.__comment = line[comment_index + 1:]
            line = line[0:comment_index]

        # Parse key and value
        try:
            assignment_index = line.index('=')

            self.__value = line[assignment_index + 1:]
            self.__value = self.__decode_value(self.__value)
            self.__key = line[0:assignment_index]
            self.__key = self.__decode_value(self.__key)
        except ValueError:
            self.__key = self.__decode_value(line)
            self.__value = ''

    def __index_of_comment(self, value):
        part_of_string = False
        string_delimiter = ' '
        for index in range(len(value)):
            chr = value[index]
            if part_of_string is False and chr == ';':
                return index
            elif part_of_string is True and chr == string_delimiter:
                part_of_string = False
            elif part_of_string is False and (chr == '\'' or chr == '\"'):
                part_of_string = True
                string_delimiter = chr

        return -1

    def __decode_value(self, value):
        value = value.strip()
        if len(value) > 0:
            if value[0] == "'" and value[-1] == "'":
                value = value[1:len(value) - 1]
                value = value.replace("''", "'")

            if value[0] == '"' and value[-1] == '"':
                value = value[1:len(value) - 1]
                value = value.replace('""', '"')
        return value

    def __encode_value(self, value):
        if value is None:
            return value

        if value[0] == ' ' or value[-1] == ' ' or value.find(';') >= 0:
            value = value.replace('"', '""')
            value = '"' + value + '"'

        return value

    def to_string(self):
        return self.__line
