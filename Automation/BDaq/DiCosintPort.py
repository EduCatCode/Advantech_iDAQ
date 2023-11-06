#!/usr/bin/python
# -*- coding:utf-8 -*-


from Automation.BDaq.BDaqApi import TDiCosintPort, BioFailed
from Automation.BDaq import ErrorCode


class DiCosintPort(object):
    def __init__(self, nativeDiCosintPortObj):
        self._nativeDiCosintPortObj = nativeDiCosintPortObj

    @property
    def port(self):
        return TDiCosintPort.getPort(self._nativeDiCosintPortObj)

    # The channels in the port that enabled change of state interrupt
    @property
    def mask(self):
        return TDiCosintPort.getMask(self._nativeDiCosintPortObj)

    @mask.setter
    def mask(self, value):
        ret = ErrorCode.lookup(TDiCosintPort.setMask(self._nativeDiCosintPortObj, value & 0xff))
        if BioFailed(ret):
            raise ValueError('set mask is failed, the error code is 0x%X' % (ret.value))

