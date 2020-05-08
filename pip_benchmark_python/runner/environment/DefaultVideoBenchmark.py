# -*- coding: utf-8 -*-

from ...PassiveBenchmark import PassiveBenchmark


class DefaultVideoBenchmark(PassiveBenchmark):
    def __init__(self):
        super().__init__('Video', 'Measures performance of video card')
