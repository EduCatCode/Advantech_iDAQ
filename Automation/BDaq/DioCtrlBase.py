#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TDioCtrlBase, TArray
from Automation.BDaq.DaqCtrlBase import DaqCtrlBase
from Automation.BDaq.DioFeatures import DioFeatures
from Automation.BDaq.DioPort import DioPort


class DioCtrlBase(DaqCtrlBase):
    def __init__(self, scenario, devInfo):
        super(DioCtrlBase, self).__init__(scenario, devInfo)
        self._dio_features = None
        self._dio_ports = []
        self._dio_ports.append(DioPort(None))
        self._dio_ports = []

    @property
    def features(self):
        if self._dio_features is None:
            self._dio_features = DioFeatures(TDioCtrlBase.getFeatures(self._obj))
        return self._dio_features

    @property
    def portCount(self):
        return self.features.portCount

    @property
    def ports(self):
        if not self._dio_ports:
            nativeArray = TDioCtrlBase.getPorts(self._obj)
            count = self.portCount
            for i in range(count):
                dioPortObj = DioPort(TArray.getItem(nativeArray, i))
                self._dio_ports.append(dioPortObj)

        return self._dio_ports
