#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq import Scenario
from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq.TmrChannel import TmrChannel
from Automation.BDaq.BDaqApi import TArray, TTimerPulseCtrl


class TimerPulseCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(TimerPulseCtrl, self).__init__(Scenario.SceTimerPulse, devInfo)
        self._tmr_channels = []
        self._tmr_channels.append(TmrChannel(None))
        self._tmr_channels = []

    @property
    def channels(self):
        if not self._tmr_channels:
            count = self.features.channelCountMax
            nativeArr = TTimerPulseCtrl.getChannels(self._obj)

            for i in range(count):
                tmrChannObj = TmrChannel(TArray.getItem(nativeArr, i))
                self._tmr_channels.append(tmrChannObj)
        return self._tmr_channels
