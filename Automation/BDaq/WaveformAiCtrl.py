#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_int32, c_int16, c_double, byref, c_int

from Automation.BDaq.AiCtrlBase import AiCtrlBase
from Automation.BDaq import Scenario, DataMark, ErrorCode, MAX_TRIG_COUNT
from Automation.BDaq.Conversion import Conversion
from Automation.BDaq.Record import Record
from Automation.BDaq.BDaqApi import TWaveformAiCtrl
from Automation.BDaq.Trigger import Trigger


class WaveformAiCtrl(AiCtrlBase):
    def __init__(self, devInfo = None):
        super(WaveformAiCtrl, self).__init__(Scenario.SceWaveformAi, devInfo)
        self._conversion = None
        self._record = None
        self._triggers = []
        self._triggers.append(Trigger(None))
        self._triggers = []

    @property
    def conversion(self):
        if self._conversion is None:
            nativeConver = TWaveformAiCtrl.getConversion(self._obj)
            self._conversion = Conversion(nativeConver, self.features.channelCountMax)
        return self._conversion

    @property
    def record(self):
        if self._record is None:
            nativeRecord = TWaveformAiCtrl.getRecord(self._obj)
            self._record = Record(nativeRecord)
        return self._record

    @property
    def trigger(self):
        if not self._triggers:
            for i in range(self.features.triggerCount):
                triggerObj = Trigger(TWaveformAiCtrl.getTrigger(self._obj, i))
                self._triggers.append(triggerObj)
        return self._triggers

    def prepare(self):
        ret = TWaveformAiCtrl.Prepare(self._obj)
        return ErrorCode.lookup(ret)

    def start(self):
        ret = TWaveformAiCtrl.Start(self._obj)
        return ErrorCode.lookup(ret)

    def stop(self):
        return ErrorCode.lookup(TWaveformAiCtrl.Stop(self._obj))

    def getDataI16(self, count, timeout = 0, startTime = None, markCount = None):
        dataArr = (c_int16 * count)()
        return self.__getData(2, count, dataArr, timeout, startTime, markCount)

    def getDataI32(self, count, timeout = 0, startTime = None, markCount = None):
        dataArr = (c_int32 * count)()
        return self.__getData(4, count, dataArr, timeout, startTime, markCount)

    def getDataF64(self, count, timeout = 0, startTime = None, markCount = None):
        dataArr = (c_double * count)()
        return self.__getData(8, count, dataArr, timeout, startTime, markCount)

    def __getData(self, dt, count, dataArr, timeout, startTime, markCount):
        returned = (c_int * 1)()
        dataBuf = []
        startTimeClock = startTime
        if startTime is not None:
            startTimeClock = (c_double * 1)()

        markBufTmp = None
        markCountTmp = None
        if markCount is not None and isinstance(markCount, int):
            markBufTmp = (DataMark * markCount)()
            markCountTmp = (c_int32 * 1)()

        ret = TWaveformAiCtrl.GetData(self._obj, dt, count, dataArr, timeout, returned, startTimeClock, markCountTmp,
                                      markBufTmp)

        for i in range(returned[0]):
            dataBuf.append(dataArr[i])

        startTimeClock = None if startTimeClock is None else startTimeClock[0]
        markCountTmp = None if markCount is None else markCountTmp[0]
        if markCount is None:
            markBuf = None
        else:
            markBuf = []
            for i in range(markCountTmp):
                markBuf.append(markBufTmp[i])
        return ErrorCode.lookup(ret), returned[0], dataBuf, startTimeClock, markCountTmp, markBuf

