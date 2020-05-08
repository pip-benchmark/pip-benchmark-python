# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class IConfigurationListener:
    @abstractmethod
    def on_configuration_changed(self):
        pass
