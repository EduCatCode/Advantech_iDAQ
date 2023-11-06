#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq import ErrorCode
from Automation.BDaq.BDaqApi import TScanChannel, BioFailed


class ScanChannel(object):
    def __init__(self, nativeScanChanObj):
        self._nativeScanChanObj = nativeScanChanObj

    @property
    def channelStart(self):
        return TScanChannel.getChannelStart(self._nativeScanChanObj)

    @channelStart.setter
    def channelStart(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TScanChannel.setChannelStart(self._nativeScanChanObj, value))
        if BioFailed(ret):
            raise ValueError('set channelStart is failed, the error code is 0x%X' % (ret.value))

    @property
    def channelCount(self):
        return TScanChannel.getChannelCount(self._nativeScanChanObj)

    @channelCount.setter
    def channelCount(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TScanChannel.setChannelCount(self._nativeScanChanObj, value))
        if BioFailed(ret):
            raise ValueError('set channelCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def samples(self):
        return TScanChannel.getSamples(self._nativeScanChanObj)

    @samples.setter
    def samples(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TScanChannel.setSamples(self._nativeScanChanObj, value))
        if BioFailed(ret):
            raise ValueError('set samples is failed, the error code is 0x%X' % (ret.value))

    @property
    def intervalCount(self):
        return TScanChannel.getIntervalCount(self._nativeScanChanObj)

    @intervalCount.setter
    def intervalCount(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TScanChannel.setIntervalCount(self._nativeScanChanObj, value))
        if BioFailed(ret):
            raise ValueError('set intervalCount is failed, the error code is 0x%X' % (ret.value))
