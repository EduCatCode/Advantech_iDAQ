#!/usr/bin/python
# -*- coding:utf-8 -*-


from Automation.BDaq.BDaqApi import TUdChannel, BioFailed
from Automation.BDaq import ErrorCode, PulseWidth, CountingType, SignalPolarity, OutSignalType
from Automation.BDaq import Utils


class UdChannel(object):
    def __init__(self, nativeUdChann):
        self._nativeUdChann = nativeUdChann

    @property
    def channel(self):
        return TUdChannel.getChannel(self._nativeUdChann)

    @property
    def noiseFiltered(self):
        ret = TUdChannel.getNoiseFiltered(self._nativeUdChann)
        return True if ret else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret = ErrorCode.lookup(TUdChannel.setNoiseFiltered(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def countingType(self):
        value = TUdChannel.getCountingType(self._nativeUdChann)
        return Utils.toCountingType(value)

    @countingType.setter
    def countingType(self, value):
        if not isinstance(value, CountingType):
            raise TypeError('a CountingType is required')
        ret = ErrorCode.lookup(TUdChannel.setCountingType(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set countingType is failed, the error code is 0x%X' % (ret.value))

    @property
    def initialValue(self):
        return TUdChannel.getInitialValue(self._nativeUdChann)

    @initialValue.setter
    def initialValue(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TUdChannel.setInitialValue(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set initialValue is failed, the error code is 0x%X' % (ret.value))

    @property
    def resetTimesByIndex(self):
        return TUdChannel.getResetTimesByIndex(self._nativeUdChann)

    @resetTimesByIndex.setter
    def resetTimesByIndex(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TUdChannel.setResetTimesByIndex(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set resetTimesByIndex is failed, the error code is 0x%X' % (ret.value))

    @property
    def pulseWidth(self):
        x = PulseWidth()
        TUdChannel.getPulseWidth(self._nativeUdChann, x)
        return x

    @pulseWidth.setter
    def pulseWidth(self, value):
        if not isinstance(value, PulseWidth):
            raise TypeError('a PulseWidth is required')
        ret = ErrorCode.lookup(TUdChannel.setPulseWidth(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set pulseWidth is failed, the error code is 0x%X' % (ret.value))


    @property
    def gated(self):
        value = TUdChannel.getGated(self._nativeUdChann)
        return True if value else False

    @gated.setter
    def gated(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TUdChannel.setGated(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set gated is failed, the error code is 0x%X' % (ret.value))

    @property
    def gatePolarity(self):
        value = TUdChannel.getGatePolarity(self._nativeUdChann)
        return Utils.toSignalPolarity(value)

    @gatePolarity.setter
    def gatePolarity(self, value):
        if not isinstance(value, SignalPolarity):
            raise TypeError('a SignalPolarity is required')
        ret = ErrorCode.lookup(TUdChannel.setGatePolarity(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set gatePolarity is failed, the error code is 0x%X' % (ret.value))

    @property
    def outSignal(self):
        value = TUdChannel.getOutSignal(self._nativeUdChann)
        return Utils.toOutSignaleType(value)

    @outSignal.setter
    def outSignal(self, value):
        if not isinstance(value, OutSignalType):
            raise TypeError('a OutSignalType is required')
        ret = ErrorCode.lookup(TUdChannel.setOutSignal(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set outSignal is failed, the error code is 0x%X' % (ret.value))

    @property
    def outCount(self):
        return TUdChannel.getOutCount(self._nativeUdChann)

    @outCount.setter
    def outCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TUdChannel.setOutCount(self._nativeUdChann, value))
        if BioFailed(ret):
            raise ValueError('set outCount is failed, the error code is 0x%X' % (ret.value))
