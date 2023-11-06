#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TNosFltChannel, BioFailed
from Automation.BDaq import ErrorCode


class NoiseFilterChannel(object):
    def __init__(self, native_nos_flt_chann_obj):
        self._native_nos_flt_chann_obj = native_nos_flt_chann_obj

    @property
    def channel(self):
        return TNosFltChannel.getChannel(self._native_nos_flt_chann_obj)

    @property
    def enabled(self):
        ret = TNosFltChannel.getEnabled(self._native_nos_flt_chann_obj)
        return True if ret else False

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        ret = ErrorCode.lookup(TNosFltChannel.setEnabled(self._native_nos_flt_chann_obj, value))
        if BioFailed(ret):
            raise ValueError('set enabled is failed, the error code is 0x%X' % (ret.value))
