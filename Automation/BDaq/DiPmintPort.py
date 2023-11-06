#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TDiPmintPort
from Automation.BDaq import ErrorCode


class DiPmintPort(object):
    def __init__(self, nativeDiPmPortObj):
        self._nativeDiPmPortObj = nativeDiPmPortObj

    @property
    def port(self):
        return TDiPmintPort.getPort(self._nativeDiPmPortObj)

    @property
    def mask(self):
        return TDiPmintPort.getMask(self._nativeDiPmPortObj)

    @mask.setter
    def mask(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TDiPmintPort.setMask(self._nativeDiPmPortObj, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set mask is failed, the error code is 0x%X' % (ret.value))

    @property
    def pattern(self):
        return TDiPmintPort.getPattern(self._nativeDiPmPortObj)

    @pattern.setter
    def pattern(self, value):
        if not isinstance(value, int):
            raise TypeError('a int is required')
        ret = ErrorCode.lookup(TDiPmintPort.setPattern(self._nativeDiPmPortObj, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set pattern is failed, the error code is 0x%X' % (ret.value))
