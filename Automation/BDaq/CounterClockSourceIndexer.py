#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.CounterIndexer import CounterIndexer
from Automation.BDaq import SignalDrop
from Automation.BDaq import Utils


class CounterClockSourceIndexer(CounterIndexer):
    def __init__(self, nativeIndexer):
        super(CounterClockSourceIndexer, self).__init__(nativeIndexer, SignalDrop, Utils.toSignalDrop)
