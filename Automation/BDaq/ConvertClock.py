#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TConvertClock, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import ErrorCode, SignalDrop


class ConvertClock(object):
    def __init__(self, nativeCnrtClkObj):
        self._nativeCnrtClkObj = nativeCnrtClkObj

    @property
    def source(self):
        ret = TConvertClock.getSource(self._nativeCnrtClkObj)
        return Utils.toSignalDrop(ret)

    @source.setter
    def source(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError('a SignalDrop is required')
        ret = ErrorCode.lookup(TConvertClock.setSource(self._nativeCnrtClkObj, value))
        if BioFailed(ret):
            raise ValueError('set source is failed, the error code is 0x%X' % (ret.value))

    @property
    def rate(self):
        return TConvertClock.getRate(self._nativeCnrtClkObj)

    @rate.setter
    def rate(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TConvertClock.setRate(self._nativeCnrtClkObj, value))
        if BioFailed(ret):
            raise ValueError('set rate is failed, the error code is 0x%X' % (ret.value))
