#!/usr/bin/python
# -*- coding:utf-8 -*-

import ctypes

from Automation.BDaq.BDaqApi import TAiChannel, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import *


class AnalogInputChannel(object):
    def __init__(self, ai_channel_obj):
        self._ai_channel_obj = ai_channel_obj

    @property
    def channel(self):
        return TAiChannel.getChannel(self._ai_channel_obj)

    @property
    def logicalNumber(self):
        return TAiChannel.getLogicalNumber(self._ai_channel_obj)

    @property
    def valueRange(self):
        value = TAiChannel.getValueRange(self._ai_channel_obj)
        return Utils.toValueRange(value)

    @valueRange.setter
    def valueRange(self, value):
        if not isinstance(value, ValueRange):
            raise TypeError('a ValueRange is required')
        ret = ErrorCode.lookup(TAiChannel.setValueRange(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set valueRange is failed, the error code is 0x%X' % (ret.value))

    @property
    def signalType(self):
        value = TAiChannel.getSignalType(self._ai_channel_obj)
        return Utils.toAiSignalType(value)

    @signalType.setter
    def signalType(self, value):
        if not isinstance(value, AiSignalType):
            raise TypeError('a AiSignalType is required')
        ret = ErrorCode.lookup(TAiChannel.setSignalType(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set signalType is failed, the error code is 0x%X' % (ret.value))

    @property
    def burnoutRetType(self):
        value = TAiChannel.getBurnoutRetType(self._ai_channel_obj)
        return Utils.toBurnoutRetType(value)

    @burnoutRetType.setter
    def burnoutRetType(self, value):
        if not isinstance(value, BurnoutRetType):
            raise TypeError('a BurnoutRetType is required')
        ret = ErrorCode.lookup(TAiChannel.setBurnoutRetType(self._ai_channel_obj, int(value)))
        if BioFailed(ret):
            raise ValueError('set burnoutRetType is failed, the error code is 0x%X' % (ret.value))

    @property
    def burnoutRetValue(self):
        value = TAiChannel.getBurnoutRetValue(self._ai_channel_obj)
        return value

    @burnoutRetValue.setter
    def burnoutRetValue(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAiChannel.setBurnoutRetValue(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set burnoutRetValue is failed, the error code is 0x%X' % (ret.value))

    @property
    def burnShortRetValue(self):
        return TAiChannel.getBurnShortRetValue(self._ai_channel_obj)

    @burnShortRetValue.setter
    def burnShortRetValue(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(TAiChannel.setBurnShortRetValue(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set burnShortRetValue is failed, the error code is 0x%X' % (ret.value))

    @property
    def filterType(self):
        value = TAiChannel.getFilterType(self._ai_channel_obj)
        return Utils.toFilterType(value)

    @filterType.setter
    def filterType(self, value):
        if not isinstance(value, FilterType):
            raise TypeError('a FilterType is requires')
        ret = ErrorCode.lookup(TAiChannel.setFilterType(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set filterType is failed, the error code is 0x%X' % (ret.value))

    @property
    def filterCutoffFreq(self):
        value = TAiChannel.getFilterCutoffFreq(self._ai_channel_obj)
        return value

    @filterCutoffFreq.setter
    def filterCutoffFreq(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAiChannel.setFilterCutoffFreq(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set filterCutoffFreq is failed, the error code is 0x%X' % (ret.value))

    @property
    def filterCutoffFreq1(self):
        value = TAiChannel.getFilterCutoffFreq1(self._ai_channel_obj)
        return value

    @filterCutoffFreq1.setter
    def filterCutoffFreq1(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAiChannel.setFilterCutoffFreq1(self._ai_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set filterCutoffFreq1 is failed, the error code is 0x%X' % (ret.value))

    @property
    def couplingType(self):
        value = TAiChannel.getCouplingType(self._ai_channel_obj)
        return Utils.toCouplingType(value)

    @couplingType.setter
    def couplingType(self, value):
        if not isinstance(value, CouplingType):
            raise TypeError('a CouplingType is required')
        ret = ErrorCode.lookup(TAiChannel.setCouplingType(self._ai_channel_obj, int(value)))
        if BioFailed(ret):
            raise ValueError('set couplingType is failed, the error code is 0x%X' % (ret.value))

    @property
    def iepeType(self):
        value = TAiChannel.getIepeType(self._ai_channel_obj)
        return Utils.toIepeType(value)

    @iepeType.setter
    def iepeType(self, value):
        if not isinstance(value, IepeType):
            raise TypeError('a IepeType is required')
        ret = ErrorCode.lookup(TAiChannel.setIepeType(self._ai_channel_obj, int(value)))
        if BioFailed(ret):
            raise ValueError('set iepeType is failed, the error code is 0x%X' % (ret.value))

    @property
    def impedanceType(self):
        value = TAiChannel.getImpedanceType(self._ai_channel_obj)
        return Utils.toImpedanceType(value)

    @impedanceType.setter
    def impedanceType(self, value):
        if not isinstance(value, ImpedanceType):
            raise TypeError('a ImpedanceType is required')
        ret = ErrorCode.lookup(TAiChannel.setImpedanceType(self._ai_channel_obj, int(value)))
        if BioFailed(ret):
            raise ValueError('set impedanceType is failed, the error code is 0x%X' % (ret.value))

    @property
    def sensorDescription(self):
        desc = ctypes.create_unicode_buffer(1024)
        pSize = (ctypes.c_int * 1)(1024)
        err = TAiChannel.getSensorDescription(self._ai_channel_obj, pSize, desc)
        if err == int(ErrorCode.ErrorBufferTooSmall.value):
            desc = ctypes.create_unicode_buffer(pSize[0])
            err = TAiChannel.getSensorDescription(self._ai_channel_obj, pSize, desc)

        return ErrorCode.lookup(err), desc.value.encode()

    @sensorDescription.setter
    def sensorDescription(self, value):
        ret = ErrorCode.lookup(TAiChannel.setSensorDescription(self._ai_channel_obj, len(value), value))
        if BioFailed(ret):
            raise ValueError('set sensorDescription is failed, the error code is 0x%X' % (ret.value))

    @property
    def scaleTable(self):
        pSize = (c_int32 * 1)(32)
        buffer = (MapFuncPiece * 32)()
        ret = ErrorCode.lookup(TAiChannel.getScaleTable(self._ai_channel_obj, pSize, buffer))
        if ret == ErrorCode.ErrorBufferTooSmall:
            buffer = (MapFuncPiece * pSize[0])()
            ret = ErrorCode.lookup(TAiChannel.getScaleTable(self._ai_channel_obj, pSize, buffer))

        if BioFailed(ret):
            raise ValueError('get scaletable is failed, the error code is 0x%X' % (ret.value))
            return None
        else:
            data = []
            for i in range(pSize[0]):
                data.append(buffer[i])
            return data

    @scaleTable.setter
    def scaleTable(self, table):
        size = len(table)
        dataArra = (MapFuncPiece * size)()
        for i in range(size):
            dataArra[i] = table[i]
        ret = ErrorCode.lookup(TAiChannel.setScaleTable(self._ai_channel_obj, size, dataArra))
        if BioFailed(ret):
            raise ValueError('set scaleTable is failed, the error code is 0x%X' % (ret.value))
