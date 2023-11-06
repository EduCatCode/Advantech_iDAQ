#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.DaqCtrlBase import DaqCtrlBase
from Automation.BDaq.BDaqApi import TAoCtrlBase, TArray, BioFailed
from Automation.BDaq.AoFeatures import AoFeatures
from Automation.BDaq.AoChannel import AoChannel
from Automation.BDaq import ErrorCode


class AoCtrlBase(DaqCtrlBase):
    def __init__(self, scenario, devInfo):
        super(AoCtrlBase, self).__init__(scenario, devInfo)
        self._ao_features = None
        self._ao_channels = []
        self._ao_channels.append(AoChannel(None))
        self._ao_channels = []

    @property
    def features(self):
        if self._ao_features is None:
            self._ao_features = AoFeatures(TAoCtrlBase.getFeatures(self._obj))
        return self._ao_features

    @property
    def channels(self):
        if not self._ao_channels:
            count = self.features.channelCountMax
            nativeChannArr = TAoCtrlBase.getChannels(self._obj)
            for i in range(count):
                self._ao_channels.append(AoChannel(TArray.getItem(nativeChannArr, i)))
        return self._ao_channels

    @property
    def channelCount(self):
        return self.features.channelCountMax

    @property
    def extRefValueForUnipolar(self):
        return TAoCtrlBase.getExtRefValueForUnipolar(self._obj)

    @extRefValueForUnipolar.setter
    def extRefValueForUnipolar(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAoCtrlBase.setExtRefValueForUnipolar(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set extRefValueForUnipolar is failed, the error code is 0x%X' % (ret.value))

    @property
    def extRefValueForBipolar(self):
        return TAoCtrlBase.getExtRefValueForBipolar(self._obj)

    @extRefValueForBipolar.setter
    def extRefValueForBipolar(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TAoCtrlBase.setExtRefValueForBipolar(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set extRefValueForBipolar is failed, the error code is 0x%X' % (ret.value))
