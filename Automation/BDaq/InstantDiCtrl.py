#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import *

from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.DioCtrlBase import DioCtrlBase
from Automation.BDaq.BDaqApi import TInstantDiCtrl, TArray, BioFailed
from Automation.BDaq.DiintChannel import DiintChannel
from Automation.BDaq.NosFltChannel import NosFltChannel
from Automation.BDaq.DiPmintPort import DiPmintPort
from Automation.BDaq.DiCosintPort import DiCosintPort


class InstantDiCtrl(DioCtrlBase):
    def __init__(self, devInfo = None):
        super(InstantDiCtrl, self).__init__(Scenario.SceInstantDi, devInfo)
        self._nosFltChans = []
        self._nosFltChans.append(NosFltChannel(None))
        self._nosFltChans = []
        self._intChans = []
        self._intChans.append(DiintChannel(None))
        self._intChans = []
        self._cosPorts = []
        self._cosPorts.append(DiCosintPort(None))
        self._cosPorts = []
        self._pmPorts = []
        self._pmPorts.append(DiPmintPort(None))
        self._pmPorts = []

    @property
    def noiseFilterBlockTime(self):
        return TInstantDiCtrl.getNoiseFilterBlockTime(self._obj)

    @noiseFilterBlockTime.setter
    def noiseFilterBlockTime(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TInstantDiCtrl.setNoiseFilterBlockTime(self._obj, value))
        if BioFailed(ret):
            raise ValueError('set noiseFilterBlockTime is failed, the error code is 0x%X' % (ret.value))

    @property
    def noiseFilter(self):
        if not self._nosFltChans:
            nativeArr = TInstantDiCtrl.getNoiseFilter(self._obj)
            count = TArray.getLength(nativeArr)
            for i in range(count):
                nosFltChannObj = NosFltChannel(TArray.getItem(nativeArr, i))
                self._nosFltChans.append(nosFltChannObj)
        return self._nosFltChans

    @property
    def diIntChannels(self):
        if not self._intChans:
            nativeArray = TInstantDiCtrl.getDiintChannels(self._obj)
            count = TArray.getLength(nativeArray)
            for i in range(count):
                diintChannObj = DiintChannel(TArray.getItem(nativeArray, i))
                self._intChans.append(diintChannObj)
        return self._intChans

    @property
    def diCosintPorts(self):
        if not self._cosPorts:
            nativeArray = TInstantDiCtrl.getDiCosintPorts(self._obj)
            count = TArray.getLength(nativeArray)
            for i in range(count):
                cosPortsObj = DiCosintPort(TArray.getItem(nativeArray, i))
                self._cosPorts.append(cosPortsObj)
        return self._cosPorts

    @property
    def diPmintPorts(self):
        if not self._pmPorts:
            nativeArray = TInstantDiCtrl.getDiPmintPorts(self._obj)
            count = TArray.getLength(nativeArray)
            for i in range(count):
                pmPortsObj = DiPmintPort(TArray.getItem(nativeArray, i))
                self._pmPorts.append(pmPortsObj)
        return self._pmPorts

    def readAny(self, portStart, portCount):
        dataArray = (c_uint8 * portCount)()
        data = []
        ret = TInstantDiCtrl.readAny(self._obj, portStart, portCount, dataArray)
        for i in range(portCount):
            data.append(dataArray[i])
        return ErrorCode.lookup(ret), data

    def readBit(self, port, bit):
        dataArray = (c_uint8 * 1)()
        ret = TInstantDiCtrl.readBit(self._obj, port, bit, dataArray)
        data = dataArray[0]
        return ErrorCode.lookup(ret), data
