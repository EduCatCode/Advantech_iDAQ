#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import c_int32, c_byte, c_uint8
from ctypes import create_unicode_buffer
from ctypes import pointer

from Automation.BDaq.BDaqApi import TArray, TerminalBoard
from Automation.BDaq.BDaqApi import TDeviceCtrl, BioFailed
from Automation.BDaq import ErrorCode
from Automation.BDaq import Utils


class DeviceCtrl(object):
    def __init__(self, nativeDev):
        self._nativeDev = nativeDev

    # method
    def refresh(self):
        return ErrorCode.lookup(TDeviceCtrl.Refresh(self._nativeDev))

    def readRegister(self, space, offset, length):
        dataArr = (c_byte * length)()
        data = []
        ret = TDeviceCtrl.ReadRegister(self._nativeDev, space, offset, length, dataArr)
        if not BioFailed(ret):
            for i in range(length):
                data.append(dataArr[i])
        return ErrorCode.lookup(ret), data

    def writeRegister(self, space, offset, length, data):
        if not isinstance(data, list):
            raise TypeError('a list is required')
        if length != len(data):
            raise ValueError('Length mismatch: length:%d, len(data):%d' % (length, len(data)))
        dataArr = (c_byte * length)()
        for i in range(length):
            dataArr[i] = data[i]
        ret = TDeviceCtrl.WriteRegister(self._nativeDev, space, offset, length, dataArr)
        return ErrorCode.lookup(ret)

    def readPrivateRegion(self, signature, length):
        dataArr = (c_uint8 * length)()
        data = []

        ret = TDeviceCtrl.ReadPrivateRegion(self._nativeDev, signature, length, dataArr)
        if not BioFailed(ret):
            for i in range(length):
                data.append(dataArr[i])
        return ErrorCode.lookup(ret), data

    def writePrivateRegion(self, signature, length, data):
        if not isinstance(data, list):
            raise TypeError('a list is required')

        if length != len(data):
            raise ValueError('Length mismatch: length:%d, len(data):%d' % (length, len(data)))

        dataArr = (c_uint8 * length)()
        for i in range(length):
            dataArr[i] = data[i]

        ret = TDeviceCtrl.WritePrivateRegion(self._nativeDev, signature, length, dataArr)
        return ErrorCode.lookup(ret)

    def synchronizeTimeBase(self):
        return ErrorCode.lookup(TDeviceCtrl.SynchronizeTimebase(self._nativeDev))

    def calculateAbsoluteTime(self, relativeTime):
        if not isinstance(relativeTime, float):
            raise TypeError('a float is required')
        return TDeviceCtrl.CalculateAbsoluteTime(self._nativeDev, relativeTime)

    # properties
    @property
    def deviceNumber(self):
        return TDeviceCtrl.getDeviceNumber(self._nativeDev)

    @property
    def description(self):
        descr = create_unicode_buffer(256)
        TDeviceCtrl.getDescription(self._nativeDev, 256, descr)

        return descr.value.encode()

    @description.setter
    def description(self, desc):
        ret = ErrorCode.lookup(TDeviceCtrl.setDescription(self._nativeDev, len(desc), desc))
        if BioFailed(ret):
            raise ValueError('set description is failed, the error code is 0x%X' % (ret.value))

    @property
    def accessMode(self):
        return Utils.toAccessMode(TDeviceCtrl.getAccessMode(self._nativeDev))

    @property
    def productId(self):
        return Utils.toProductId(TDeviceCtrl.getProductId(self._nativeDev))

    @property
    def boardId(self):
        return TDeviceCtrl.getBoardId(self._nativeDev)

    @boardId.setter
    def boardId(self, value):
        ret = ErrorCode.lookup(TDeviceCtrl.setBoardId(self._nativeDev, value))
        if BioFailed(ret):
            raise ValueError('set boardId is failed, the error code is 0x%X' % (ret.value))

    @property
    def boardVersion(self):
        version = create_unicode_buffer(256)
        TDeviceCtrl.getBoardVersion(self._nativeDev, 256, version)
        return version.value.encode()

    @property
    def driverVersion(self):
        version = create_unicode_buffer(256)
        TDeviceCtrl.getDriverVersion(self._nativeDev, 256, version)
        return version.value.encode()

    @property
    def dllVersion(self):
        version = create_unicode_buffer(256)
        TDeviceCtrl.getDllVersion(self._nativeDev, 256, version)
        return version.value.encode()

    @property
    def location(self):
        version = create_unicode_buffer(256)
        TDeviceCtrl.getLocation(self._nativeDev, 256, version)
        return version.value.encode()

    @property
    def privateRegionLength(self):
        return TDeviceCtrl.getPrivateRegionLength(self._nativeDev)

    @property
    def hotResetPreventable(self):
        return TDeviceCtrl.getHotResetPreventable(self._nativeDev)

    @property
    def baseAddresses(self):
        nativeArray = TDeviceCtrl.getBaseAddresses(self._nativeDev)
        return TArray.ToInt64(nativeArray, True)

    @property
    def interrupts(self):
        nativeArray = TDeviceCtrl.getInterrupts(self._nativeDev)
        return TArray.ToInt32(nativeArray, True)

    @property
    def supportedTerminalBoard(self):
        nativeArray = TDeviceCtrl.getSupportedTerminalBoard(self._nativeDev)
        return TArray.ToTerminalBoard(nativeArray, True)

    @property
    def supportedEvents(self):
        nativeArray = TDeviceCtrl.getSupportedEvents(self._nativeDev)
        return TArray.ToEventId(nativeArray, True)

    @property
    def supportedScenarios(self):
        return TDeviceCtrl.getSupportedScenarios(self._nativeDev)

    @property
    def terminalBoard(self):
        return Utils.toTerminalBoard(TDeviceCtrl.getTerminalBoard(self._nativeDev))

    @terminalBoard.setter
    def terminalBoard(self, value):
        if not isinstance(value, TerminalBoard):
            raise TypeError("a TerminalBoard is required")
        ret = ErrorCode.lookup(TDeviceCtrl.setTerminalBoard(self._nativeDev, value))
        if BioFailed(ret):
            raise ValueError('set terminalBoard is failed, the error code is 0x%X' % (ret.value))

    def setLocateEnabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('a bool is required')
        return ErrorCode.lookup(TDeviceCtrl.setLocateEnabled(self._nativeDev, value))

    @property
    def installedDevices(self):
        nativeArray = TDeviceCtrl.getInstalledDevices()
        arr = TArray.toDeviceTreeNode(nativeArray, True)
        return arr

    def getHwSpecific(self, name):
        dataArr = (c_int32 * 1)()
        size = c_int32(4)
        pSize = pointer(size)
        data = None
        ret = ErrorCode.lookup(TDeviceCtrl.getHwSpecific(self._nativeDev, name, pSize, dataArr))
        if ret == ErrorCode.Success:
            data = dataArr[0]
        return ret, data

    def setHwSpecific(self, name, data):
        dataArr = (c_int32 * 1)()
        dataArr[0] = data
        ret = TDeviceCtrl.setHwSpecific(self._nativeDev, name, 4, dataArr)
        return ErrorCode.lookup(ret)
