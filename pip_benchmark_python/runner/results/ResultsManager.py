# -*- coding: utf-8 -*-

from .BenchmarkResult import BenchmarkResult


class ResultsManager:

    def __init__(self):
        self.__results = []
        self.__update_listeners = []
        self.__message_listeners = []
        self.__error_listeners = []

    @property
    def all(self):
        return self.__results

    def add(self, result):
        self.__results.append(result)

    def clear(self):
        self.__results = []

    def add_updated_listener(self, listener):
        self.__update_listeners.append(listener)

    def remove_updated_listener(self, listener):
        index = len(self.__update_listeners) - 1
        while index >= 0:
            if self.__update_listeners[index] == listener:
                del self.__update_listeners[index]
            index -= 1

    def notify_updated(self, result):
        for index in range(len(self.__update_listeners)):
            try:
                listener = self.__update_listeners[index]
                listener(result)
            except Exception as err:
                # Ignore and send a message to the next listener.
                pass

    def add_message_listener(self, listener):
        self.__message_listeners.append(listener)

    def remove_message_listener(self, listener):
        index = len(self.__message_listeners) - 1
        while index >= 0:
            if self.__message_listeners[index] == listener:
                del self.__message_listeners[index]
            index -= 1

    def notify_message(self, message):
        for index in range(len(self.__message_listeners)):
            try:
                listener = self.__message_listeners[index]
                listener(message)
            except Exception as err:
                # Ignore and send a message to the next listener.
                pass

    def add_error_listener(self, listener):
        self.__error_listeners.append(listener)

    def remove_error_listener(self, listener):
        index = len(self.__error_listeners) - 1
        while index >= 0:
            if self.__error_listeners[index] == listener:
                del self.__error_listeners[index]
            index -= 1

    def notify_error(self, error):
        for index in range(len(self.__error_listeners)):
            try:
                listener = self.__error_listeners[index]
                listener(error)
            except Exception as err:
                # Ignore and send an error to the next listener.
                pass
