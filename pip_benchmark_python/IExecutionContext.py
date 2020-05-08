# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class IExecuteContext(ABC):

    def __init__(self):
        self.parameters = None

    @abstractmethod
    def increment_counter(self, increment=None):
        """

        :param increment:
        """

    @abstractmethod
    def send_message(self, message):
        """

        :param message:
        """

    @abstractmethod
    def report_error(self, error):
        """

        :param error:
        """

    is_stoped = None

    @abstractmethod
    def stop(self):
        """

        """
