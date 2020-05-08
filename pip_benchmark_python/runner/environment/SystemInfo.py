# -*- coding: utf-8 -*-

import platform
import getpass


class SystemInfo(dict):
    def __init__(self):
        super().__init__()
        self.__put('Machine Name', platform.node())
        self.__put('User Name', getpass.getuser())
        self.__put('Operating System Name', platform.system())
        self.__put('Operating System Version', platform.version())
        self.__put('Operating System Architecture', platform.architecture()[0])
        self.__put('Python Version', platform.python_version())
        self.__put('Python Compiler', platform.python_compiler())
        self.__put('Python Build', platform.python_build()[0])

    def __put(self, parameter, value):
        self[parameter] = value
