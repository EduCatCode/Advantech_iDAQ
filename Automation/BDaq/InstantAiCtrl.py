#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import *

from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.BDaqApi import TInstantAiCtrl, BioFailed
from Automation.BDaq.AiCtrlBase import AiCtrlBase
from Automation.BDaq.CjcSetting import CjcSetting


class InstantAiCtrl(AiCtrlBase):
    def __init__(self, devInfo = None):
        super(InstantAiCtrl, self).__init__(Scenario.SceInstantAi, devInfo)
        self._cjc = None

    @property
    def cjc(self):
        if self._cjc is None:
            self._cjc = CjcSetting(TInstantAiCtrl.getCjc(self._obj))
        return self._cjc
    
    @property
    def autoConvertClockRate(self):
        return TInstantAiCtrl.getAutoConvertClockRate(self._obj)
    
    @autoConvertClockRate.setter
    def autoConvertClockRate(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TInstantAiCtrl.setAutoConvertClockRate(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set autoConvertClockRate is failed, the error code is 0x%X' % (ret.value))
    
    @property
    def autoConvertChannelStart(self):
        return TInstantAiCtrl.getAutoConvertChannelStart(self._obj)

    @autoConvertChannelStart.setter
    def autoConvertChannelStart(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TInstantAiCtrl.setAutoConvertChannelStart(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set autoConvertChannelStart is failed, the error code is 0x%X' % (ret.value))

    @property
    def autoConvertChannelCount(self):
        return TInstantAiCtrl.getAutoConvertChannelCount(self._obj)

    @autoConvertChannelCount.setter
    def autoConvertChannelCount(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TInstantAiCtrl.setAutoConvertChannelCount(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set autoConvertChannelCount is failed, the error code is 0x%X' % (ret.value))
    
    def readDataF64(self, chStart, chCount):
        if not isinstance(chStart, int):
            raise TypeError("a int is required")
        if not isinstance(chCount, int):
            raise TypeError("a int is required")
        
        scaledArray = (c_double * chCount)()
        dataScaled = []
        ret = ErrorCode.lookup(TInstantAiCtrl.readAny(self._obj, chStart, chCount, None, scaledArray))
        if BioFailed(ret):
            return ret, dataScaled

        for i in range(chCount):
            dataScaled.append(scaledArray[i])
        return ret, dataScaled

    def readDataI32(self, chStart, chCount):
        if not isinstance(chStart, int):
            raise TypeError("a int is required")
        if not isinstance(chCount, int):
            raise TypeError("a int is required")
        
        rawArray = (c_int32 * chCount)()
        dataRaw = []
        ret = ErrorCode.lookup(TInstantAiCtrl.readAny(self._obj, chStart, chCount, rawArray, None))
        if BioFailed(ret):
            return ret, dataRaw

        for i in range(chCount):
            dataRaw.append(rawArray[i])
        return ret, dataRaw
    
    def readDataI16(self, chStart, chCount):
        if not isinstance(chStart, int):
            raise TypeError("a int is required")
        if not isinstance(chCount, int):
            raise TypeError("a int is required")
        
        rawArray = (c_int16 * chCount)()
        dataRaw = []
        ret = ErrorCode.lookup(TInstantAiCtrl.readAny(self._obj, chStart, chCount, rawArray, None))
        if BioFailed(ret):
            return ret, dataRaw

        for i in range(chCount):
            dataRaw.append(rawArray[i])
        return ret, dataRaw
