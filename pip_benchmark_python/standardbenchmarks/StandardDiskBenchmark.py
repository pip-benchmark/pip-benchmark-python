# -*- coding: utf-8 -*-

import random
import math
import os

from ..Benchmark import Benchmark


class StandardDiskBenchmark(Benchmark):

    __NAME_TEXT = 'Disk'
    __DESCRIPTION_TEXT = 'Measures disk read and write operations'
    __BUFFER_SIZE = 512
    __CHUNK_SIZE = 1024000
    __FILE_SIZE = 102400000

    def __init__(self):
        super().__init__(StandardDiskBenchmark.__NAME_TEXT, StandardDiskBenchmark.__DESCRIPTION_TEXT)
        self.__file_name = None
        self.__fd = None
        self.__file_size = 0
        self.__buffer = self.__BUFFER_SIZE

    def set_up(self, callback):
        id = math.ceil(1000000 + random.random() * 9000000)
        self.__file_name = './DiskBenchmark-' + str(id) + '.dat'

        try:
            self.__fd = open(self.__file_name, 'w+')
            if callback:
                callback(None)
        except Exception as err:
            if callback:
                callback(err)

    def execute(self, callback):
        if self.__fd is None:
            return

        try:
            if self.__file_size == 0 or random.random() < 0.5:
                position = None
                if self.__file_size < StandardDiskBenchmark.__FILE_SIZE:
                    position = self.__file_size
                else:
                    position = math.ceil(random.random() * (self.__file_size - StandardDiskBenchmark.__CHUNK_SIZE))

                size_to_write = StandardDiskBenchmark.__CHUNK_SIZE
                while size_to_write > 0:
                    lenght = min(StandardDiskBenchmark.__BUFFER_SIZE, size_to_write)
                    with open(self.__fd.name, "w+", encoding='UTF-8') as file:
                        file.seek(position)
                        self.__buffer = file.read(lenght)

                        position += lenght
                        self.__file_size = max(self.__file_size, position)
                        size_to_write -= lenght
                else:
                    position = math.ceil(random.random() * (self.__file_size - StandardDiskBenchmark.__CHUNK_SIZE))

                    size_to_read = StandardDiskBenchmark.__CHUNK_SIZE
                    while size_to_read > 0:
                        lenght = min(StandardDiskBenchmark.__BUFFER_SIZE, size_to_read)
                        with open(self.__fd.name, "w+", encoding='UTF-8') as file:
                            file.seek(position)
                            self.__buffer = file.read(lenght)

                            position += lenght
                            self.__file_size = max(self.__file_size, position)
                            size_to_read -= lenght
            if callback:
                callback(None)
        except Exception as err:
            if callback:
                callback(err)

    def tear_down(self, callback):
        try:
            self.__fd.close()
            self.__fd = None

            if os.path.exists(self.__file_name):
                os.remove(self.__file_name)
        except Exception:
            # ignore...
            pass

        if callback(None):
            callback(None)
