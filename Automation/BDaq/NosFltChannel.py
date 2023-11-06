#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.NoiseFilterChannel import NoiseFilterChannel


class NosFltChannel(NoiseFilterChannel):
    def __init__(self, nativeNoiseFilterChannObj):
        super(NosFltChannel, self).__init__(nativeNoiseFilterChannObj)
