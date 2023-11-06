#!/usr/bin/python
# -*- coding:utf-8 -*-


from Automation.BDaq import PulseWidth, ErrorCode, SignalPolarity, OutSignalType
from Automation.BDaq.BDaqApi import TPoChannel, BioFailed
from Automation.BDaq import Utils


class PoChannel(object):
    def __init__(self, nativePoChannObj):
        self._nativePoChannObj = nativePoChannObj

    @property
    def channel(self):
        return TPoChannel.getChannel(self._nativePoChannObj)

    @property
    def noiseFiltered(self):
        value = TPoChannel.getNoiseFiltered(self._nativePoChannObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")

        ret = ErrorCode.lookup(TPoChannel.setNoiseFiltered(self._nativePoChannObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def pulseWidth(self):
        value = PulseWidth()
        TPoChannel.getPulseWidth(self._nativePoChannObj, value)
        return value

    @pulseWidth.setter
    def pulseWidth(self, value):
        if not isinstance(value, PulseWidth):
            raise TypeError("a PulseWidth is required")
        ret = ErrorCode.lookup(TPoChannel.setPulseWidth(self._nativePoChannObj, value))
        if BioFailed(ret):
            raise ValueError('set pulseWidth is failed, the error code is 0x%X' % (ret.value))

    @property
    def gatePolarity(self):
        return Utils.toSignalPolarity(TPoChannel.getGatePolarity(self._nativePoChannObj))

    @gatePolarity.setter
    def gatePolarity(self, varValue):
        if not isinstance(varValue, SignalPolarity):
            raise TypeError("a SignalPolarity is required")
        ret = ErrorCode.lookup(TPoChannel.setGatePolarity(self._nativePoChannObj, varValue.value))
        if BioFailed(ret):
            raise ValueError('set gatePolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def gated(self):
        value = TPoChannel.getGated(self._nativePoChannObj)
        return True if value else False

    @gated.setter
    def gated(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret = ErrorCode.lookup(TPoChannel.setGated(self._nativePoChannObj, value))
        if BioFailed(ret):
            raise ValueError('set gated is failed, the error code is 0x%X' % (ret.value))

    @property
    def outSignal(self):
        return Utils.toOutSignaleType(TPoChannel.getOutSignal(self._nativePoChannObj))

    @outSignal.setter
    def outSignal(self, varValue):
        if not isinstance(varValue, OutSignalType):
            raise TypeError('a OutSignalType is required')
        ret = ErrorCode.lookup(TPoChannel.setOutSignal(self._nativePoChannObj, varValue.value))
        if BioFailed(ret):
            raise ValueError('set outSignal is failed, the error code is 0x%X' % (ret.value))

    @property
    def outCount(self):
        return TPoChannel.getOutCount(self._nativePoChannObj)

    @outCount.setter
    def outCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TPoChannel.setOutCount(self._nativePoChannObj, value))
        if BioFailed(ret):
            raise ValueError('set outCount is failed, the error code is 0x%X' % (ret.value))
