#!/usr/bin/python
# -*- coding:utf-8 -*-

import ctypes

from Automation.BDaq.BDaqApi import TAoFeatures
from Automation.BDaq.BDaqApi import TArray
from Automation.BDaq import MathInterval
from Automation.BDaq import Utils


class AoFeatures(object):
    def __init__(self, nativeFeatures):
        self._ao_feature = nativeFeatures

    # DAC features
    @property
    def resolution(self):
        return TAoFeatures.getResolution(self._ao_feature)

    @property
    def dataSize(self):
        return TAoFeatures.getDataSize(self._ao_feature)

    @property
    def dataMask(self):
        return TAoFeatures.getDataMask(self._ao_feature)

    # channel features
    @property
    def channelCountMax(self):
        return TAoFeatures.getChannelCountMax(self._ao_feature)

    @property
    def valueRanges(self):
        nativeArray = TAoFeatures.getValueRanges(self._ao_feature)
        return TArray.ToValueRange(nativeArray, True)

    @property
    def externalRefAntiPolar(self):
        ret = TAoFeatures.getExternalRefAntiPolar(self._ao_feature)
        return True if ret else False

    @property
    def externalRefRange(self):
        x = MathInterval()
        TAoFeatures.getExternalRefRange(self._ao_feature, ctypes.pointer(x))
        return x

    # buffered ao->basic features
    @property
    def bufferedAoSupported(self):
        ret = TAoFeatures.getBufferedAoSupported(self._ao_feature)
        return True if ret else False

    @property
    def samplingMethod(self):
        ret = TAoFeatures.getSamplingMethod(self._ao_feature)
        return Utils.toSamplingMethod(ret)

    @property
    def channelStartBase(self):
        return TAoFeatures.getChannelStartBase(self._ao_feature)

    @property
    def channelCountBase(self):
        return TAoFeatures.getChannelCountBase(self._ao_feature)

    # buffered ao->conversion clock features
    @property
    def convertClockSources(self):
        nativeArray = TAoFeatures.getConvertClockSources(self._ao_feature)
        return TArray.ToSignalDrop(nativeArray, True)

    @property
    def convertClockRange(self):
        x = MathInterval()
        TAoFeatures.getConvertClockRange(self._ao_feature, ctypes.pointer(x))
        return x

    # buffered ao->trigger features
    @property
    def triggerCount(self):
        return TAoFeatures.getTriggerCount(self._ao_feature)

    @property
    def retriggerable(self):
        value = TAoFeatures.getRetriggerable(self._ao_feature)
        return True if value else False

    # trigger 0
    @property
    def triggerSupported(self):
        return self.triggerCount != 0

    # trigger 1
    @property
    def trigger1Supported(self):
        return self.triggerCount > 1

    def getTriggerActions(self, trigger = 0):
        nativeArray = TAoFeatures.getTriggerActions(self._ao_feature, trigger)
        return TArray.ToTriggerAction(nativeArray, True)

    def getTriggerDelayRange(self, trigger = 0):
        x = MathInterval()
        TAoFeatures.getTriggerDelayRange(self._ao_feature, trigger, ctypes.byref(x))
        return x

    def getTriggerSources(self, trigger = 0):
        nativeArray = TAoFeatures.getTriggerSources(self._ao_feature, trigger)
        return TArray.ToSignalDrop(nativeArray, True)