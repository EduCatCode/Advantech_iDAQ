#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TDioPort, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import ErrorCode, DioPortDir, DoCircuitType


class DioPort(object):
    def __init__(self, nativePort):
        self._nativePort = nativePort

    @property
    def port(self):
        return TDioPort.getPort(self._nativePort)

    @property
    def direction(self):
        return Utils.toDioPortDir(TDioPort.getDirection(self._nativePort))

    @direction.setter
    def direction(self, value):
        if not isinstance(value, DioPortDir):
            raise TypeError('a DioPortDir is required')
        ret = ErrorCode.lookup(TDioPort.setDirection(self._nativePort, value))
        if BioFailed(ret):
            raise ValueError('set direction is failed, the error code is 0x%X' % (ret.value))

    @property
    def diInversePort(self):
        return TDioPort.getDiInversePort(self._nativePort)

    @diInversePort.setter
    def diInversePort(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TDioPort.setDiInversePort(self._nativePort, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set diInversePort is failed, the error code is 0x%X' % (ret.value))

    @property
    def diOpenState(self):
        return TDioPort.getDiOpenState(self._nativePort)

    @diOpenState.setter
    def diOpenState(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TDioPort.setDiOpenState(self._nativePort, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set diOpenState is failed, the error code is 0x%X' % (ret.value))

    @property
    def doPresetValue(self):
        return TDioPort.getDoPresetValue(self._nativePort)

    @doPresetValue.setter
    def doPresetValue(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TDioPort.setDoPresetValue(self._nativePort, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set doPresetValue is failed, the error code is 0x%X' % (ret.value))

    @property
    def doCircuitType(self):
        return Utils.toDoCircuitType(TDioPort.getDoCircuitType(self._nativePort))

    @doCircuitType.setter
    def doCircuitType(self, value):
        if not isinstance(value, DoCircuitType):
            raise TypeError('a DoCircuitType is required')
        ret = ErrorCode.lookup(TDioPort.setDoCircuitType(self._nativePort, value))
        if BioFailed(ret):
            raise ValueError('set doCircuitType is failed, the error code is 0x%X' % (ret.value))
