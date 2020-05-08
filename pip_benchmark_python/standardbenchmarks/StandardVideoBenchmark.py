# -*- coding: utf-8 -*-

from ..PassiveBenchmark import PassiveBenchmark


class StandardVideoBenchmark(PassiveBenchmark):
    def __init__(self):
        super().__init__('Video', 'Measures speed of drawing graphical primitives')
