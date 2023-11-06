#!/usr/bin/python
# -*- coding:utf-8 -*-

import ctypes

from Automation.BDaq.BDaqApi import TArray
from Automation.BDaq.BDaqApi import TDioFeatures
from Automation.BDaq import MathInterval
from Automation.BDaq import Utils


class DioFeatures(object):
    def __init__(self, nativeFeatures):
        self._dio_features = nativeFeatures

    # common
    @property
    def portProgrammable(self):
        ret = TDioFeatures.getPortProgrammable(self._dio_features)
        return True if ret else False

    @property
    def channelCountMax(self):
        return TDioFeatures.getChannelCountMax(self._dio_features)

    @property
    def portCount(self):
        return TDioFeatures.getPortCount(self._dio_features)

    @property
    def portsType(self):
        nativeArr = TDioFeatures.getPortsType(self._dio_features)
        return TArray.ToByte(nativeArr, True)

    @property
    def diSupported(self):
        ret = TDioFeatures.getDiSupported(self._dio_features)
        return True if ret else False

    @property
    def doSupported(self):
        ret = TDioFeatures.getDoSupported(self._dio_features)
        return True if ret else False

    @property
    def diDataMask(self):
        nativeArray = TDioFeatures.getDiDataMask(self._dio_features)
        return TArray.ToByte(nativeArray, True)

    @property
    def diNoiseFilterSupported(self):
        ret = TDioFeatures.getDiNoiseFilterSupported(self._dio_features)
        return True if ret else False

    @property
    def diNoiseFilterOfChannels(self):
        nativeArray = TDioFeatures.getDiNoiseFilterOfChannels(self._dio_features)
        return TArray.ToByte(nativeArray, True)

    @property
    def diNoiseFilterBlockTimeRange(self):
        x = MathInterval()
        TDioFeatures.getDiNoiseFilterBlockTimeRange(self._dio_features, ctypes.pointer(x))
        return x

    @property
    def doDataMask(self):
        nativeArray = TDioFeatures.getDoDataMask(self._dio_features)
        return TArray.ToByte(nativeArray, True)

    @property
    def doFreezeSignalSources(self):
        nativeArray = TDioFeatures.getDoFreezeSignalSources(self._dio_features)
        return TArray.ToSignalDrop(nativeArray, True)

    @property
    def reflectWdtFeedIntervalRange(self):
        x = MathInterval()
        TDioFeatures.getDoReflectWdtFeedIntervalRange(self._dio_features, ctypes.pointer(x))
        return x

    @property
    def doPresetValueDepository(self):
        ret = TDioFeatures.getDoPresetValueDepository(self._dio_features)
        return Utils.toDepository(ret)

    @property
    def doCircuitSelectableTypes(self):
        nativeArray = TDioFeatures.getDoCircuitSelectableTypes(self._dio_features)
        return TArray.ToDoCircuitType(nativeArray, True)
