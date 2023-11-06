#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.DaqCtrlBase import DaqCtrlBase
from Automation.BDaq.BDaqApi import TAiCtrlBase, TArray
from Automation.BDaq.AiFeatures import AiFeatures
from Automation.BDaq.AiChannel import AiChannel


class AiCtrlBase(DaqCtrlBase):
    def __init__(self, scenario, devInfo):
        super(AiCtrlBase, self).__init__(scenario, devInfo)
        self._ai_features = None
        self._ai_channels = []
        self._ai_channels.append(AiChannel(None))
        self._ai_channels = []

    @property
    def features(self):
        if self._ai_features is None:
            self._ai_features = AiFeatures(TAiCtrlBase.getFeatures(self._obj))
        return self._ai_features

    @property
    def channels(self):
        if not self._ai_channels:
            count = self.features.channelCountMax
            nativeArray = TAiCtrlBase.getChannels(self._obj)
            for i in range(count):
                aiChannObj = AiChannel(TArray.getItem(nativeArray, i))
                self._ai_channels.append(aiChannObj)
        return self._ai_channels

    @property
    def channelCount(self):
        return TAiCtrlBase.getChannelCount(self._obj)
