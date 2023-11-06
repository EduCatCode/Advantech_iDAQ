#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import *

from Automation.BDaq.AoCtrlBase import AoCtrlBase
from Automation.BDaq import Scenario, ErrorCode, MAX_TRIG_COUNT
from Automation.BDaq.ScanChannel import ScanChannel
from Automation.BDaq.ConvertClock import ConvertClock
from Automation.BDaq.BDaqApi import TBufferedAoCtrl, BioFailed
from Automation.BDaq.Trigger import Trigger


class BufferedAoCtrl(AoCtrlBase):
    def __init__(self, devInfo = None):
        super(BufferedAoCtrl, self).__init__(Scenario.SceBufferedAo, devInfo)
        self._scanChannObj = None
        self._cnvtClockObj = None
        self._triggers = []
        self._triggers.append(Trigger(None))
        self._triggers = []

    @property
    def scanChannel(self):
        if self._scanChannObj is None:
            self._scanChannObj = ScanChannel(TBufferedAoCtrl.getScanChannel(self._obj))
        return self._scanChannObj

    @property
    def convertClock(self):
        if self._cnvtClockObj is None:
            self._cnvtClockObj = ConvertClock(TBufferedAoCtrl.getConvertClock(self._obj))
        return self._cnvtClockObj

    @property
    def streaming(self):
        if self.features.bufferedAoSupported:
            return TBufferedAoCtrl.getStreaming(self._obj)

    @streaming.setter
    def streaming(self, value):
        if self.features.bufferedAoSupported:
            ret = ErrorCode.lookup(TBufferedAoCtrl.setStreaming(self._obj, value))
            if BioFailed(ret):
                raise ValueError('set streaming is failed, the error code is 0x%X' % (ret.value))

    @property
    def trigger(self):
        if not self._triggers:
            for i in range(self.features.triggerCount):
                triggerObj = Trigger(TBufferedAoCtrl.getTrigger(self._obj, i))
                self._triggers.append(triggerObj)
        return self._triggers

    #  method
    def prepare(self):
        return ErrorCode.lookup(TBufferedAoCtrl.Prepare(self._obj))

    def runOnce(self):
        return ErrorCode.lookup(TBufferedAoCtrl.RunOnce(self._obj))
    
    def start(self):
        return ErrorCode.lookup(TBufferedAoCtrl.Start(self._obj))

    def stop(self, value):
        return ErrorCode.lookup(TBufferedAoCtrl.Stop(self._obj, value))

    def setDataF64(self, count, scaledData):
        doubleArray = (c_double * count)()
        for i in range(count):
            doubleArray[i] = scaledData[i]
        return ErrorCode.lookup(TBufferedAoCtrl.SetData(self._obj, 8, count, doubleArray))

    def setDataI32(self, count, rawData):
        intArray = (c_int32 * count)()
        for i in range(count):
            intArray[i] = rawData[i]
        return ErrorCode.lookup(TBufferedAoCtrl.SetData(self._obj, 4, count, intArray))

    def setDatai16(self, count, rawData):
        shortArray = (c_int16 * count)()
        for i in range(count):
            shortArray[i] = rawData[i]
        return ErrorCode.lookup(TBufferedAoCtrl.SetData(self._obj, 2, count, shortArray))
