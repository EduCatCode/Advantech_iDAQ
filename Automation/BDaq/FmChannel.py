#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TFmChannel, BioFailed
from Automation.BDaq import ErrorCode, FreqMeasureMethod
from Automation.BDaq import Utils


class FmChannel(object):
    def __init__(self, nativeFmChanObj):
        self._nativeFmChanObj = nativeFmChanObj

    @property
    def channel(self):
        return TFmChannel.getChannel(self._nativeFmChanObj)

    @property
    def noiseFiltered(self):
        value = TFmChannel.getNoiseFiltered(self._nativeFmChanObj)
        return True if value else False

    @noiseFiltered.setter
    def noiseFiltered(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TFmChannel.setNoiseFiltered(self._nativeFmChanObj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFiltered is failed, the error code is 0x%X' % (ret.value))

    @property
    def fmMethod(self):
        value = TFmChannel.getFmMethod(self._nativeFmChanObj)
        return Utils.toFreqMeasureMethod(value)

    @fmMethod.setter
    def fmMethod(self, value):
        if not isinstance(value, FreqMeasureMethod):
            raise TypeError("a FreqMeasureMethod is required")
        ret = ErrorCode.lookup(TFmChannel.setFmMethod(self._nativeFmChanObj, value))
        if BioFailed(ret):
            raise ValueError('set fmMethod is failed, the error code is 0x%X' % (ret.value))

    @property
    def collectionPeriod(self):
        return TFmChannel.getCollectionPeriod(self._nativeFmChanObj)

    @collectionPeriod.setter
    def collectionPeriod(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(TFmChannel.setCollectionPeriod(self._nativeFmChanObj, value))
        if BioFailed(ret):
            raise ValueError('set collectionPeriod is failed, the error code is 0x%X' % (ret.value))
