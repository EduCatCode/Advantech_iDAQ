#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_byte
from Automation.BDaq.BDaqApi import TConversion, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import ErrorCode, SignalDrop


class Conversion(object):
    def __init__(self, nativeConvObj, chanCount):
        self._nativeConvObj = nativeConvObj
        self._chanCount = chanCount

    @property
    def clockSource(self):
        ret = TConversion.getClockSource(self._nativeConvObj)
        return Utils.toSignalDrop(ret)

    @clockSource.setter
    def clockSource(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError('a SignalDrop is required')
        ret = ErrorCode.lookup(TConversion.setClockSource(self._nativeConvObj, value))
        if BioFailed(ret):
            raise ValueError('set clockSource is failed, the error code is 0x%X' % (ret.value))

    @property
    def clockRate(self):
        return TConversion.getClockRate(self._nativeConvObj)

    @clockRate.setter
    def clockRate(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TConversion.setClockRate(self._nativeConvObj, value))
        if BioFailed(ret):
            raise ValueError('set clockRate is failed, the error code is 0x%X' % (ret.value))

    @property
    def channelStart(self):
        return TConversion.getChannelStart(self._nativeConvObj)

    @channelStart.setter
    def channelStart(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TConversion.setChannelStart(self._nativeConvObj, int(value)))
        if BioFailed(ret):
            raise ValueError('set channelStart is failed, the error code is 0x%X' % (ret.value))

    @property
    def channelCount(self):
        return TConversion.getChannelCount(self._nativeConvObj)

    @channelCount.setter
    def channelCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TConversion.setChannelCount(self._nativeConvObj, value))
        if BioFailed(ret):
            raise ValueError('set channelCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def channelMap(self):
        data = []
        dataArr = (c_byte * self._chanCount)()
        TConversion.getChannelMap(self._nativeConvObj, self._chanCount, dataArr)
        for i in range(self._chanCount):
            data.append(dataArr[i])
        return data

    @channelMap.setter
    def channelMap(self, value):
        if not isinstance(value, list):
            raise TypeError('a list is required')
        dataLen = len(value)
        dataArr = (c_byte * dataLen)()
        for i, data in enumerate(value):
            dataArr[i] = data
        ret = ErrorCode.lookup(TConversion.setChannelMap(self._nativeConvObj, dataLen, dataArr))
        if BioFailed(ret):
            raise ValueError('set channelMap is failed, the error code is 0x%X' % (ret.value))
