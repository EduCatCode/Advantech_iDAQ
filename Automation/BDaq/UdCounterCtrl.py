#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_int

from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.UdChannel import UdChannel
from Automation.BDaq.BDaqApi import TArray, TUdCounterCtrl


class UdCounterCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(UdCounterCtrl, self).__init__(Scenario.SceUdCounter, devInfo)
        self._ud_channels = []
        self._ud_channels.append(UdChannel(None))
        self._ud_channels = []

    @property
    def channels(self):
        if not self._ud_channels:
            count = self.features.channelCountMax
            nativeArr = TUdCounterCtrl.getChannels(self._obj)

            for i in range(count):
                udChannObj = UdChannel(TArray.getItem(nativeArr, i))
                self._ud_channels.append(udChannObj)
        return self._ud_channels

    def read(self, count = 1):
        dataArr = (c_int * count)()
        data = []
        ret = TUdCounterCtrl.Read(self._obj, count, dataArr)
        for i in range(count):
            data.append(dataArr[i])
        return ErrorCode.lookup(ret), data

    def valueReset(self):
        return ErrorCode.lookup(TUdCounterCtrl.ValueReset(self._obj))
