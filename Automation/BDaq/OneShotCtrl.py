#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq import Scenario
from Automation.BDaq.CntrCtrlBase import CntrCtrlBase
from Automation.BDaq.OsChannel import OsChannel
from Automation.BDaq.BDaqApi import TArray, TOneShotCtrl


class OneShotCtrl(CntrCtrlBase):
    def __init__(self, devInfo = None):
        super(OneShotCtrl, self).__init__(Scenario.SceOneShot, devInfo)
        self._os_channels = []
        self._os_channels.append(OsChannel(None))
        self._os_channels = []

    @property
    def channels(self):
        if not self._os_channels:
            count = self.features.channelCountMax
            nativeArr = TOneShotCtrl.getChannels(self._obj)

            for i in range(count):
                poChannObj = OsChannel(TArray.getItem(nativeArr, i))
                self._os_channels.append(poChannObj)
        return self._os_channels
