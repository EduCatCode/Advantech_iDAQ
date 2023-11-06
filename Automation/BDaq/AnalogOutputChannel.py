#!/usr/bin/python
# -*- coding:utf-8 -*-

import ctypes

from Automation.BDaq.BDaqApi import TAoChannel, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import *


class AnalogOutputChannel(object):
    def __init__(self, ao_channel_obj):
        self._ao_channel_obj = ao_channel_obj

    @property
    def channel(self):
        return TAoChannel.getChannel(self._ao_channel_obj)

    @property
    def valueRange(self):
        return Utils.toValueRange(TAoChannel.getValueRange(self._ao_channel_obj))

    @valueRange.setter
    def valueRange(self, value):
        if not isinstance(value, ValueRange):
            raise TypeError('a ValueRange is required')
        ret = ErrorCode.lookup(TAoChannel.setValueRange(self._ao_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set valueRange is failed, the error code is 0x%X' % (ret.value))

    @property
    def extRefBipolar(self):
        return TAoChannel.getExtRefBipolar(self._ao_channel_obj)

    @extRefBipolar.setter
    def extRefBipolar(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAoChannel.setExtRefBipolar(self._ao_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set extRefBipolar is failed, the error code is 0x%X' % (ret.value))

    @property
    def extRefUnipolar(self):
        return TAoChannel.getExtRefUnipolar(self._ao_channel_obj)

    @extRefUnipolar.setter
    def extRefUnipolar(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAoChannel.setExtRefUnipolar(self._ao_channel_obj, value))
        if BioFailed(ret):
            raise ValueError('set extRefUnipolar is failed, the error code is 0x%X' % (ret.value))


    @property
    def scaleTable(self):
        pSize = (ctypes.c_int * 1)(32)
        buffer = (MapFuncPiece * 32)()
        ret = ErrorCode.lookup(TAoChannel.getScaleTable(self._ao_channel_obj, pSize, buffer))
        if ret == ErrorCode.ErrorBufferTooSmall:
            buffer = (MapFuncPiece * pSize[0])()
            ret = ErrorCode.lookup(TAoChannel.getScaleTable(self._ao_channel_obj, pSize, buffer))
        
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
        ret = ErrorCode.lookup(TAoChannel.setScaleTable(self._ao_channel_obj, size, dataArra))
        if BioFailed(ret):
            raise ValueError('set scaletable is failed, the error code is 0x%X' % (ret.value))
