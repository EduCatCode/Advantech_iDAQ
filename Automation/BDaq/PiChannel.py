#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TPiChannel, BioFailed
from Automation.BDaq import ErrorCode


class PiChannel(object):
    def __init__(self, nativePiChanObj):
        self._nativePiChanObj = nativePiChanObj

    @property
    def channel(self):
        return TPiChannel.getChannel(self._nativePiChanObj)

    @property
    def noiseFiltered(self):
        value = TPiChannel.getNoiseFiltered(self._nativePiChanObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TPiChannel.setNoiseFiltered(self._nativePiChanObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))
