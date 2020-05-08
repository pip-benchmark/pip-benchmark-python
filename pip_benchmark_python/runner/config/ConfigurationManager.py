# -*- coding: utf-8 -*-

from .MeasurementType import MeasurementType
from .ExecutionType import ExecutionType
from .IConfigurationListener import IConfigurationListener


class ConfigurationManager:

    def __init__(self):
        self.__measurement_type = MeasurementType.Peak
        self.__nominal_rate = 1
        self.__execution_type = ExecutionType.Proportional
        self.__duration = 60
        self.__force_continue = False
        self.__change_listeners = []

    @property
    def measurement_type(self):
        return self.__measurement_type

    @measurement_type.setter
    def measurement_type(self, value):
        self.__measurement_type = value
        self.notify_changed()

    @property
    def nominal_rate(self):
        return self.__nominal_rate

    @nominal_rate.setter
    def nominal_rate(self, value):
        self.__nominal_rate = value
        self.notify_changed()

    @property
    def execution_type(self):
        return self.__execution_type

    @execution_type.setter
    def execution_type(self, value):
        self.__execution_type = value
        self.notify_changed()

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value
        self.notify_changed()

    @property
    def force_continue(self):
        return self.__force_continue

    @force_continue.setter
    def force_continue(self, value):
        self.__force_continue = value
        self.notify_changed()

    def add_change_listener(self, listener):
        self.__change_listeners.append(listener)

    def remove_change_listener(self, listener):
        index = len(self.__change_listeners) - 1
        while index >= 0:
            if self.__change_listeners[index] == listener:
                self.__change_listeners = self.__change_listeners.pop(index)
            index -= 1

    def notify_changed(self):
        for index in range(len(self.__change_listeners)):
            try:
                listener = self.__change_listeners[index]
                listener()
            except Exception as err:
                # Ignore and send a message to the next listener.
                pass
