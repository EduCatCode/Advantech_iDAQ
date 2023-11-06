#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TEcChannel, BioFailed
from Automation.BDaq import ErrorCode, SignalPolarity, SignalDrop
from Automation.BDaq import Utils


class EcChannel(object):
    def __init__(self, nativeEcChanObj):
        self._nativeEcChanObj = nativeEcChanObj

    @property
    def channel(self):
        return TEcChannel.getChannel(self._nativeEcChanObj)

    @property
    def noiseFiltered(self):
        value = TEcChannel.getNoiseFiltered(self._nativeEcChanObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TEcChannel.setNoiseFiltered(self._nativeEcChanObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def clockSource(self):
        return Utils.toSignalDrop(TEcChannel.getClockSource(self._nativeEcChanObj))

    @clockSource.setter
    def clockSource(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError('a SignalDrop is required')
        ret = ErrorCode.lookup(TEcChannel.setClockSource(self._nativeEcChanObj, value.value))
        if BioFailed(ret):
            raise ValueError('set clockSource is failed, the error code is 0x%X' % (ret.value))

    @property
    def clockPolarity(self):
        return Utils.toSignalPolarity(TEcChannel.getClockPolarity(self._nativeEcChanObj))

    @clockPolarity.setter
    def clockPolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError("a SignalPolarity is required")
        ret = ErrorCode.lookup(TEcChannel.setClockPolarity(self._nativeEcChanObj, value.value))
        if BioFailed(ret):
            raise ValueError('set clockPolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def gatePolarity(self):
        return Utils.toSignalPolarity(TEcChannel.getGatePolarity(self._nativeEcChanObj))

    @gatePolarity.setter
    def gatePolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError("a SignalePolarity is required")
        ret = ErrorCode.lookup(TEcChannel.setGatePolarity(self._nativeEcChanObj, value.value))
        if BioFailed(ret):
            raise ValueError('set gatePolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def gated(self):
        value = TEcChannel.getGated(self._nativeEcChanObj)
        return True if value else False

    @gated.setter
    def gated(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TEcChannel.setGated(self._nativeEcChanObj, value))
        if BioFailed(ret):
            raise ValueError('set gated is failed, the error code is 0x%X' % (ret.value))
