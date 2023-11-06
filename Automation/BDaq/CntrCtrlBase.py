#!/usr/bin/python
# -*- coding:utf-8 -*-


from Automation.BDaq.DaqCtrlBase import DaqCtrlBase
from Automation.BDaq.CntrFeatures import CntrFeatures
from Automation.BDaq.BDaqApi import TCntrCtrlBase, BioFailed
from Automation.BDaq.NosFltChannel import NosFltChannel
from Automation.BDaq import ErrorCode


class CntrCtrlBase(DaqCtrlBase):
    def __init__(self, scenario, devInfo):
        super(CntrCtrlBase, self).__init__(scenario, devInfo)
        self._cntr_features = None

    @property
    def features(self):
        if self._cntr_features is None:
            self._cntr_features = CntrFeatures(TCntrCtrlBase.getFeatures(self._obj))
        return self._cntr_features

    @property
    def channelStart(self):
        return TCntrCtrlBase.getChannelStart(self._obj)

    @channelStart.setter
    def channelStart(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TCntrCtrlBase.setChannelStart(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set channelStart is failed, the error code is 0x%X' % (ret.value))

    @property
    def channelCount(self):
        return TCntrCtrlBase.getChannelCount(self._obj)

    @channelCount.setter
    def channelCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TCntrCtrlBase.setChannelCount(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set channelCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def enabled(self):
        value = TCntrCtrlBase.getEnabled(self._obj)
        return value != 0

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        # value = 1 if value else 0
        ret = ErrorCode.lookup(TCntrCtrlBase.setEnabled(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set enabled is failed, the error code is 0x%X' % (ret.value))

    @property
    def running(self):
        value = TCntrCtrlBase.getRunning(self._obj)
        return True if value else False

    @property
    def noiseFilterBlockTime(self):
        return TCntrCtrlBase.getNoiseFilterBlockTime(self._obj)

    @noiseFilterBlockTime.setter
    def noiseFilterBlockTime(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TCntrCtrlBase.setNoiseFilterBlockTime(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFilterBlockTime is failed, the error code is 0x%X' % (ret.value))

    @property
    def noiseFilter(self):
        if not self.features.noiseFilterSupported:
            return None
        nativeObj = TCntrCtrlBase.getNoiseFilter(self._obj)
        return NosFltChannel(nativeObj)

    @property
    def measurementTimeout(self):
        return TCntrCtrlBase.getMeasurementTimeout(self._obj)

    @measurementTimeout.setter
    def measurementTimeout(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TCntrCtrlBase.setMeasurementTimeout(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set measurementTimeout is failed, the error code is 0x%X' % (ret.value))
