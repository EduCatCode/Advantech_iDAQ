#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TOsChannel, BioFailed
from Automation.BDaq import ErrorCode, SignalPolarity, OutSignalType
from Automation.BDaq import Utils, SignalDrop


class OsChannel(object):
    def __init__(self, nativeOsObj):
        self._nativeOsObj = nativeOsObj

    @property
    def channel(self):
        return TOsChannel.getChannel(self._nativeOsObj)

    @property
    def noiseFiltered(self):
        value = TOsChannel.getNoiseFiltered(self._nativeOsObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret = ErrorCode.lookup(TOsChannel.setNoiseFiltered(self._nativeOsObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def delayCount(self):
        return TOsChannel.getDelayCount(self._nativeOsObj)

    @delayCount.setter
    def delayCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TOsChannel.setDelayCount(self._nativeOsObj, value))
        if BioFailed(ret):
            raise ValueError('set delayCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def clockSource(self):
        return Utils.toSignalDrop(TOsChannel.getClockSource(self._nativeOsObj))

    @clockSource.setter
    def clockSource(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError('a SignalDrop is required')
        ret = ErrorCode.lookup(TOsChannel.setClockSource(self._nativeOsObj, value.value))
        if BioFailed(ret):
            raise ValueError('set clockSource is failed, the error code is 0x%X' % (ret.value))

    @property
    def clockPolarity(self):
        value = TOsChannel.getClockPolarity(self._nativeOsObj)
        return Utils.toSignalPolarity(value)

    @clockPolarity.setter
    def clockPolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError('a SignalPolarity is required')
        ret = ErrorCode.lookup(TOsChannel.setClockPolarity(self._nativeOsObj, value.value))
        if BioFailed(ret):
            raise ValueError('set clockPolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def gateSource(self):
        return Utils.toSignalDrop(TOsChannel.getGateSource(self._nativeOsObj))

    @gateSource.setter
    def gateSource(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError('a SignalDrop is required')
        ret = ErrorCode.lookup(TOsChannel.setGateSource(self._nativeOsObj, value.value))
        if BioFailed(ret):
            raise ValueError('set gateSource is failed, the error code is 0x%X' % (ret.value))

    @property
    def gatePolarity(self):
        value = TOsChannel.getGatePolarity(self._nativeOsObj)
        return Utils.toSignalPolarity(value)

    @gatePolarity.setter
    def gatePolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError('a SignalPolarity is required')
        ret = ErrorCode.lookup(TOsChannel.setGatePolarity(self._nativeOsObj, value.value))
        if BioFailed(ret):
            raise ValueError('set gatePolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def outSignal(self):
        value = TOsChannel.getOutSignal(self._nativeOsObj)
        return Utils.toOutSignaleType(value)

    @outSignal.setter
    def outSignal(self, value):
        if not isinstance(value, OutSignalType):
            raise TypeError("a OutSignalType is required")
        ret = ErrorCode.lookup(TOsChannel.setOutSignal(self._nativeOsObj, value.value))
        if BioFailed(ret):
            raise ValueError('set outSignal is failed, the error code is 0x%X' % (ret.value))
