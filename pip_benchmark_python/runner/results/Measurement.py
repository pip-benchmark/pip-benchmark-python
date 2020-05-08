# -*- coding: utf-8 -*-


class Measurement:

    def __init__(self, current_value, min_value, average_value, max_value):
        self.current_value = None
        self.min_value = None
        self.average_value = None
        self.max_value = None

        self.current_value = current_value
        self.max_value = min_value
        self.average_value = average_value
        self.min_value = min_value
