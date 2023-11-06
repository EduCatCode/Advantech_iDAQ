#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TCounterIndexer, TArray


class CounterIndexer(object):
    def __init__(self, nativeIndex, clazz, convert):
        self._nativeIndex = nativeIndex
        self._clazz = clazz
        self._convert = convert

    @property
    def length(self):
        return TCounterIndexer.getLength(self._nativeIndex)

    def getItem(self, channel):
        nativeArray = TCounterIndexer.getItem(self._nativeIndex, channel)
        return TArray.ToEnum(nativeArray, True, self._clazz, self._convert)
