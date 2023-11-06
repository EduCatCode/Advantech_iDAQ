#!/usr/bin/python
# -*- coding:utf-8 -*-


from Automation.BDaq.BDaqApi import TCjcSetting, BioFailed
from Automation.BDaq import ErrorCode


class CjcSetting(object):
    def __init__(self, nativeCjcSetting):
        self._cjcObj = nativeCjcSetting

    @property
    def channel(self):
        return TCjcSetting.getChannel(self._cjcObj)

    @channel.setter
    def channel(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TCjcSetting.setChannel(self._cjcObj, value))
        if BioFailed(ret):
            raise ValueError('set channel is failed, the error code is 0x%X' % (ret.value))

    @property
    def value(self):
        return TCjcSetting.getValue(self._cjcObj)

    @value.setter
    def value(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TCjcSetting.setValue(self._cjcObj, value))
        if BioFailed(ret):
            raise ValueError('set value is failed, the error code is 0x%X' % (ret.value))

    @property
    def updateFrequency(self):
        return TCjcSetting.getUpdateFreq(self._cjcObj)

    @updateFrequency.setter
    def updateFrequency(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TCjcSetting.setUpdateFreq(self._cjcObj, value))
        if BioFailed(ret):
            raise ValueError('set updateFrequency is failed, the error code is 0x%X' % (ret.value))

