#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TTrigger, BioFailed
from Automation.BDaq import Utils
from Automation.BDaq import SignalDrop, ErrorCode, ActiveSignal, TriggerAction, FilterType


class Trigger(object):
    def __init__(self, nativeTrigObj):
        self._nativeTrigObj = nativeTrigObj

    @property
    def source(self):
        value = TTrigger.getSource(self._nativeTrigObj)
        return Utils.toSignalDrop(value)

    @source.setter
    def source(self, value):
        if not isinstance(value, SignalDrop):
            raise TypeError("a SignalDrop is required")
        ret = ErrorCode.lookup(TTrigger.setSource(self._nativeTrigObj, value.value))
        if BioFailed(ret):
            raise ValueError('set source is failed, the error code is 0x%X' % (ret.value))

    @property
    def edge(self):
        value = TTrigger.getEdge(self._nativeTrigObj)
        return Utils.toActiveSignal(value)

    @edge.setter
    def edge(self, value):
        if not isinstance(value, ActiveSignal):
            raise TypeError('a ActiveSignal is required')
        ret = ErrorCode.lookup(TTrigger.setEdge(self._nativeTrigObj, value.value))
        if BioFailed(ret):
            raise ValueError('set edge is failed, the error code is 0x%X' % (ret.value))

    @property
    def level(self):
        value = TTrigger.getLevel(self._nativeTrigObj)
        return value

    @level.setter
    def level(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TTrigger.setLevel(self._nativeTrigObj, value))
        if BioFailed(ret):
            raise ValueError('set level is failed, the error code is 0x%X' % (ret.value))

    @property
    def action(self):
        value = TTrigger.getAction(self._nativeTrigObj)
        return Utils.toTriggerAction(value)

    @action.setter
    def action(self, value):
        if not isinstance(value, TriggerAction):
            raise TypeError('a TriggerAction is required')
        ret = ErrorCode.lookup(TTrigger.setAction(self._nativeTrigObj, value.value))
        if BioFailed(ret):
            raise ValueError('set action is failed, the error code is 0x%X' % (ret.value))

    @property
    def delayCount(self):
        return TTrigger.getDelayCount(self._nativeTrigObj)

    @delayCount.setter
    def delayCount(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is requires')
        ret = ErrorCode.lookup(TTrigger.setDelayCount(self._nativeTrigObj, value))
        if BioFailed(ret):
            raise ValueError('set delayCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def hysteresisIndex(self):
        return TTrigger.getHysteresisIndex(self._nativeTrigObj)

    @hysteresisIndex.setter
    def hysteresisIndex(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TTrigger.setHysteresisIndex(self._nativeTrigObj, value))
        if BioFailed(ret):
            raise ValueError('set hysteresisIndex is failed, the error code is 0x%X' % (ret.value))

    @property
    def filterType(self):
        value = TTrigger.getFilterType(self._nativeTrigObj)
        return Utils.toFilterType(value)

    @filterType.setter
    def filterType(self, value):
        if not isinstance(value, FilterType):
            raise TypeError('a FilterType is required')
        ret = ErrorCode.lookup(TTrigger.setFilterType(self._nativeTrigObj, value.value))
        if BioFailed(ret):
            raise ValueError('set filterType is failed, the error code is 0x%X' % (ret.value))

    @property
    def filterCutoffFreq(self):
        return TTrigger.getFilterCutoffFreq(self._nativeTrigObj)

    @filterCutoffFreq.setter
    def filterCutoffFreq(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('a float is required')
        ret = ErrorCode.lookup(TTrigger.setFilterCutoffFreq(self._nativeTrigObj, value))
        if BioFailed(ret):
            raise ValueError('set filterCutoffFreq is failed, the error code is 0x%X' % (ret.value))