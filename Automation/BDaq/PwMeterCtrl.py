#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq import Scenario, PulseWidth, ErrorCode
from Automation.BDaq.BDaqApi import TArray, TPwMeterCtrl
from Automation.BDaq.PiChannel import PiChannel


class PwMeterCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(PwMeterCtrl, self).__init__(Scenario.ScePwMeter, devInfo)
        self._pi_channesl = []
        self._pi_channesl.append(PiChannel(None))
        self._pi_channesl = []

    @property
    def channels(self):
        if not self._pi_channesl:
            count = self.features.channelCountMax
            nativeArr = TPwMeterCtrl.getChannels(self._obj)
            for i in range(count):
                piChanObj = PiChannel(TArray.getItem(nativeArr, i))
                self._pi_channesl.append(piChanObj)
        return self._pi_channesl

    def read(self, count = 1):
        pulseWidthArr = (PulseWidth * count)()
        ret = ErrorCode.lookup(TPwMeterCtrl.Read(self._obj, count, pulseWidthArr))
        data = []
        if ret == ErrorCode.Success:
            for i in range(count):
                data.append(pulseWidthArr[i])
        return ret, data
