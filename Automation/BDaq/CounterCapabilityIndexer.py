#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.CounterIndexer import CounterIndexer
from Automation.BDaq import CounterCapability
from Automation.BDaq import Utils


class CounterCapabilityIndexer(CounterIndexer):
    def __init__(self, nativeIndexer):
        super(CounterCapabilityIndexer, self).__init__(nativeIndexer, CounterCapability, Utils.toCounterCapability)
