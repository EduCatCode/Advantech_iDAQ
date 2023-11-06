#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_int

from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.EcChannel import EcChannel
from Automation.BDaq.BDaqApi import TArray, TEventCounterCtrl


class EventCounterCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(EventCounterCtrl, self).__init__(Scenario.SceEventCounter, devInfo)
        self._ec_channels = []
        self._ec_channels.append(EcChannel(None))
        self._ec_channels = []

    @property
    def channels(self):
        if not self._ec_channels:
            count = self.features.channelCountMax
            nativeArr = TEventCounterCtrl.getChannels(self._obj)
            for i in range(count):
                ecChannObj = EcChannel(TArray.getItem(nativeArr, i))
                self._ec_channels.append(ecChannObj)
        return self._ec_channels

    def read(self, count = 1):
        dataArr = (c_int * count)()
        data = []
        ret = ErrorCode.lookup(TEventCounterCtrl.Read(self._obj, count, dataArr))
        for i in range(count):
            data.append(dataArr[i])
        return ret, data
