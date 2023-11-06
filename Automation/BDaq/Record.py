#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TRecord, BioFailed
from Automation.BDaq import ErrorCode


class Record(object):
    def __init__(self, nativeRecordObj):
        self._nativeRecordObj = nativeRecordObj

    @property
    def sectionLength(self):
        return TRecord.getSectionLength(self._nativeRecordObj)

    @sectionLength.setter
    def sectionLength(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TRecord.setSectionLength(self._nativeRecordObj, value))
        if BioFailed(ret):
            raise ValueError('set sectionLength is failed, the error code is 0x%X' % (ret.value))

    @property
    def sectionCount(self):
        return TRecord.getSectionCount(self._nativeRecordObj)

    @sectionCount.setter
    def sectionCount(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TRecord.setSectionCount(self._nativeRecordObj, value))
        if BioFailed(ret):
            raise ValueError('set sectionCount is failed, the error code is 0x%X' % (ret.value))

    @property
    def cycles(self):
        return TRecord.getCycles(self._nativeRecordObj)

    @cycles.setter
    def cycles(self, value):
        if not isinstance(value, int):
            raise TypeError("a int is required")
        ret = ErrorCode.lookup(TRecord.setCycles(self._nativeRecordObj, value))
        if BioFailed(ret):
            raise ValueError('set cycles is failed, the error code is 0x%X' % (ret.value))
