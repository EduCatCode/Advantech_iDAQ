#!/usr/bin/python
# -*- coding:utf-8 -*-

import ctypes

from Automation.BDaq.BDaqApi import TAiFeatures, TArray
from Automation.BDaq import Utils
from Automation.BDaq import MathInterval


class AiFeatures(object):
    def __init__(self, nativeFeature):
        self._ai_feature = nativeFeature

    # ADC features
    @property
    def resolution(self):
        return TAiFeatures.getResolution(self._ai_feature)

    @property
    def dataSize(self):
        return TAiFeatures.getDataSize(self._ai_feature)

    @property
    def dataMask(self):
        return TAiFeatures.getDataMask(self._ai_feature)

    @property
    def timestampResolution(self):
        return TAiFeatures.getTimestampResolution(self._ai_feature)

    # channel features
    @property
    def channelCountMax(self):
        return TAiFeatures.getChannelCountMax(self._ai_feature)

    @property
    def channelType(self):
        value = TAiFeatures.getChannelType(self._ai_feature)
        return Utils.toAiChannelType(value)

    @property
    def overallValueRange(self):
        ret = TAiFeatures.getOverallValueRange(self._ai_feature)
        return True if ret else False

    @property
    def valueRanges(self):
        nativeArr = TAiFeatures.getValueRanges(self._ai_feature)
        return TArray.ToValueRange(nativeArr, True)

    @property
    def burnoutReturnTypes(self):
        nativeArr = TAiFeatures.getBurnoutReturnTypes(self._ai_feature)
        return TArray.ToBurnoutRetType(nativeArr, True)

    @property
    def connectionTypes(self):
        nativeArr = TAiFeatures.getConnectionTypes(self._ai_feature)
        return TArray.ToAiSignalType(nativeArr, True)

    @property
    def overallConnection(self):
        value = TAiFeatures.getOverallConnection(self._ai_feature)
        return True if value else False

    @property
    def couplingTypes(self):
        nativeArr = TAiFeatures.getCouplingTypes(self._ai_feature)
        return TArray.ToCouplingType(nativeArr, True)

    @property
    def iepeTypes(self):
        nativeArr = TAiFeatures.getIepeTypes(self._ai_feature)
        return TArray.ToIepeType(nativeArr, True)

    @property
    def impedanceTypes(self):
        nativeArr = TAiFeatures.getImpedanceTypes(self._ai_feature)
        return TArray.ToImpedanceType(nativeArr, True)

    @property
    def filterTypes(self):
        nativeArr = TAiFeatures.getFilterTypes(self._ai_feature)
        return TArray.ToFilterType(nativeArr, True)

    @property
    def filterCutoffFreqRange(self):
        x = MathInterval()
        TAiFeatures.getFilterCutoffFreqRange(self._ai_feature, ctypes.pointer(x))
        return x

    @property
    def filterCutoffFreq1Range(self):
        x = MathInterval()
        TAiFeatures.getFilterCutoffFreq1Range(self._ai_feature, ctypes.pointer(x))
        return x

    # cjc featues
    @property
    def thermoSupported(self):
        value = TAiFeatures.getThermoSupported(self._ai_feature)
        return True if value else False

    @property
    def cjcChannels(self):
        nativeArr = TAiFeatures.getCjcChannels(self._ai_feature)
        return TArray.ToInt32(nativeArr, True)

    # buffered ai -> basic features
    @property
    def bufferedAiSupported(self):
        value = TAiFeatures.getBufferedAiSupported(self._ai_feature)
        return True if value else False

    @property
    def samplingMethod(self):
        ret = TAiFeatures.getSamplingMethod(self._ai_feature)
        return Utils.toSamplingMethod(ret)

    @property
    def channelStartBase(self):
        return TAiFeatures.getChannelStartBase(self._ai_feature)

    @property
    def channelCountBase(self):
        return TAiFeatures.getChannelCountBase(self._ai_feature)

    # buffered ai -> conversion clock features
    @property
    def convertClockSources(self):
        nativeArr = TAiFeatures.getConvertClockSources(self._ai_feature)
        return TArray.ToSignalDrop(nativeArr, True)

    @property
    def convertClockRange(self):
        x = MathInterval()
        TAiFeatures.getConvertClockRange(self._ai_feature, ctypes.pointer(x))
        return x

    # buffered ai -> burst scan
    @property
    def burnstScanSupported(self):
        value = TAiFeatures.getBurstScanSupported(self._ai_feature)
        return True if value else False

    @property
    def scanClockSources(self):
        nativeArr = TAiFeatures.getScanClockSources(self._ai_feature)
        return TArray.ToSignalDrop(nativeArr, True)

    @property
    def scanClockRange(self):
        x = MathInterval()
        TAiFeatures.getScanClockRange(self._ai_feature, ctypes.pointer(x))
        return x

    @property
    def scanCountMax(self):
        return TAiFeatures.getScanCountMax(self._ai_feature)

    # buffered ai->trigger features
    @property
    def triggerCount(self):
        return TAiFeatures.getTriggerCount(self._ai_feature)

    @property
    def retriggerable(self):
        value = TAiFeatures.getRetriggerable(self._ai_feature)
        return True if value else False

    @property
    def triggerFilterTypes(self):
        nativeArr = TAiFeatures.getTriggerFilterTypes(self._ai_feature, 0)
        return TArray.ToFilterType(nativeArr, True)

    @property
    def triggerFilterCutoffFreq(self):
        x = MathInterval()
        TAiFeatures.getTriggerFilterCutoffFreqRange(self._ai_feature, 0, ctypes.byref(x))
        return x

    # trigger 0
    @property
    def triggerSupported(self):
        return self.triggerCount != 0

    # trigger 1
    @property
    def trigger1Supported(self):
        return self.triggerCount > 1

    # buffered ai->trigger0/1/../x features
    def getTriggerActions(self, trigger = 0):
        nativeArray = TAiFeatures.getTriggerActions(self._ai_feature, trigger)
        return TArray.ToTriggerAction(nativeArray, True)

    def getTriggerDelayRange(self, trigger = 0):
        x = MathInterval()
        TAiFeatures.getTriggerDelayRange(self._ai_feature, trigger, ctypes.byref(x))
        return x

    def getTriggerSources(self, trigger = 0):
        nativeArray = TAiFeatures.getTriggerSources(self._ai_feature, trigger)
        return TArray.ToSignalDrop(nativeArray, True)

    def getTriggerSourceVrg(self, trigger = 0):
        native = TAiFeatures.getTriggerSourceVrg(self._ai_feature, trigger)
        return Utils.toValueRange(native)

    def getTriggerHysteresisIndexMax(self, trigger = 0):
        return TAiFeatures.getTriggerHysteresisIndexMax(self._ai_feature, trigger)

    def getTriggerHysteresisIndexStep(self, trigger = 0):
        return TAiFeatures.getTriggerHysteresisIndexStep(self._ai_feature, trigger)
