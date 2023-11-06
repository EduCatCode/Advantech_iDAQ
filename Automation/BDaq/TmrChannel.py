#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TTmrChannel, BioFailed
from Automation.BDaq import ErrorCode, SignalPolarity, OutSignalType
from Automation.BDaq import Utils


class TmrChannel(object):
    def __init__(self, nativeTmrObj):
        self._nativeTmrObj = nativeTmrObj

    @property
    def channel(self):
        return TTmrChannel.getChannel(self._nativeTmrObj)

    @property
    def noiseFiltered(self):
        value = TTmrChannel.getNoiseFiltered(self._nativeTmrObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret = ErrorCode.lookup(TTmrChannel.setNoiseFiltered(self._nativeTmrObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def frequency(self):
        return TTmrChannel.getFrequency(self._nativeTmrObj)

    @frequency.setter
    def frequency(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TTmrChannel.setFrequency(self._nativeTmrObj, value))
        if BioFailed(ret):
            raise ValueError('set frequency is failed, the error code is 0x%X' % (ret.value))

    @property
    def gatePolarity(self):
        value = TTmrChannel.getGatePolarity(self._nativeTmrObj)
        return Utils.toSignalPolarity(value)

    @gatePolarity.setter
    def gatePolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError('a SignalPolarity is required')
        ret = ErrorCode.lookup(TTmrChannel.setGatePolarity(self._nativeTmrObj, value.value))
        if BioFailed(ret):
            raise ValueError('set gatePolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def gated(self):
        value = TTmrChannel.getGated(self._nativeTmrObj)
        return True if value else False

    @gated.setter
    def gated(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret = ErrorCode.lookup(TTmrChannel.setGated(self._nativeTmrObj, value))
        if BioFailed(ret):
            raise ValueError('set gated is failed, the error code is 0x%X' % (ret.value))

    @property
    def outSignal(self):
        value = TTmrChannel.getOutSignal(self._nativeTmrObj)
        return Utils.toOutSignaleType(value)

    @outSignal.setter
    def outSignal(self, value):
        if not isinstance(value, OutSignalType):
            raise TypeError("a OutSignalType is required")
        ret = ErrorCode.lookup(TTmrChannel.setOutSignal(self._nativeTmrObj, value.value))
        if BioFailed(ret):
            raise ValueError('set outSignal is failed, the error code is 0x%X' % (ret.value))
