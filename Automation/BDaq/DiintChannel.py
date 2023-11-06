#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TDiintChannel, BioFailed
from Automation.BDaq import ErrorCode, ActiveSignal
from Automation.BDaq import Utils


class DiintChannel(object):
    def __init__(self, diIntChan):
        self._diIntChan = diIntChan

    @property
    def channel(self):
        return TDiintChannel.getChannel(self._diIntChan)

    @property
    def enabled(self):
        value = TDiintChannel.getEnabled(self._diIntChan)
        return True if value else False

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TDiintChannel.setEnabled(self._diIntChan, value))
        if BioFailed(ret):
            raise ValueError('set enabled is failed, the error code is 0x%X' % (ret.value))

    @property
    def gated(self):
        value = TDiintChannel.getGated(self._diIntChan)
        return True if value else False

    @gated.setter
    def gated(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TDiintChannel.setGated(self._diIntChan, value))
        if BioFailed(ret):
            raise ValueError('set gated is failed, the error code is 0x%X' % (ret.value))

    @property
    def trigEdge(self):
        return Utils.toActiveSignal(TDiintChannel.getTrigEdge(self._diIntChan))

    @trigEdge.setter
    def trigEdge(self, value):
        if not isinstance(value, ActiveSignal):
            raise TypeError('a ActiveSignal is required')
        ret = ErrorCode.lookup(TDiintChannel.setTrigEdge(self._diIntChan, value))
        if BioFailed(ret):
            raise ValueError('set trigEdge is failed, the error code is 0x%X' % (ret.value))
