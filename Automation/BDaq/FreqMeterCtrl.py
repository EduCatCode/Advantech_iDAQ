#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_double

from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq import Scenario, ErrorCode
from Automation.BDaq.FmChannel import FmChannel
from Automation.BDaq.BDaqApi import TArray, TFreqMeterCtrl


class FreqMeterCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(FreqMeterCtrl, self).__init__(Scenario.SceFreqMeter, devInfo)
        self._fm_channls = []
        self._fm_channls.append(FmChannel(None))
        self._fm_channls = []

    @property
    def channels(self):
        if not self._fm_channls:
            count = self.features.channelCountMax
            nativeArr = TFreqMeterCtrl.getChannels(self._obj)
            for i in range(count):
                fmChannObj = FmChannel(TArray.getItem(nativeArr, i))
                self._fm_channls.append(fmChannObj)
        return self._fm_channls

    def read(self, count = 1):
        dataArr = (c_double * count)()
        data = []
        ret = ErrorCode.lookup(TFreqMeterCtrl.Read(self._obj, count, dataArr))

        for i in range(count):
            data.append(dataArr[i])
        return ret, data
