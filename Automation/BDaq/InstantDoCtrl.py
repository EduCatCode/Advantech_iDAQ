#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import *

from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.BDaqApi import TInstantDoCtrl
from Automation.BDaq.DioCtrlBase import DioCtrlBase


class InstantDoCtrl(DioCtrlBase):
    def __init__(self, devInfo = None):
        super(InstantDoCtrl, self).__init__(Scenario.SceInstantDo, devInfo)

    def writeAny(self, portStart, portCount, data):
        dataArray = (c_uint8 * portCount)()
        for i in range(portCount):
            dataArray[i] = data[i]
        ret = TInstantDoCtrl.writeAny(self._obj, portStart, portCount, dataArray)
        return ErrorCode.lookup(ret)

    def writeBit(self, port, bit, data):
        ret = TInstantDoCtrl.writeBit(self._obj, port, bit, data)
        return ErrorCode.lookup(ret)

    def readAny(self, portStart, portCount):
        dataArray = (c_uint8 * portCount)()
        data = []
        ret = TInstantDoCtrl.readAny(self._obj, portStart, portCount, dataArray)
        for i in range(portCount):
            data.append(dataArray[i])
        return ErrorCode.lookup(ret), data

    def readBit(self, port, bit):
        dataArray = (c_uint8 * 1)()
        ret = TInstantDoCtrl.readBit(self._obj, port, bit, dataArray)
        data = dataArray[0]
        return ErrorCode.lookup(ret), data
