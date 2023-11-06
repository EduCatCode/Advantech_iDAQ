#!/usr/bin/python
# -*- coding:utf-8 -*-

import platform
from ctypes import *
from Automation.BDaq import *
from Automation.BDaq import Utils

if platform.architecture()[0] == '32bit':
    c_uint64 = c_uint32


if platform.system().lower() == 'windows':
    dll = windll.LoadLibrary(r"biodaq")
else:
    dll = cdll.LoadLibrary(r"libbiodaq.so")


def AdxEnumToString(enumName, enumValue, enumStrLen):
    pStr = create_unicode_buffer(enumStrLen, "\0")
    dll.AdxEnumToString.argtypes = [c_wchar_p, c_uint32, c_uint32, c_wchar_p]
    dll.AdxEnumToString.restype = c_int32
    dll.AdxEnumToString(enumName, enumValue, enumStrLen, pStr)
    enumStrBuffer = pStr.value
    pStr = None
    return enumStrBuffer


def AdxGetValueRangeInformation(valueRangeArg, sizeofDesc, pDescription, pMathIntervalRange, pValueUnit):
    dll.AdxGetValueRangeInformation.argtypes = [c_uint32, c_uint32, c_wchar_p, POINTER(MathInterval), POINTER(pValueUnit)]
    dll.AdxGetValueRangeInformation.restype = c_uint32

    ret = dll.AdxGetValueRangeInformation(valueRangeArg, sizeofDesc, pDescription, pMathIntervalRange, pValueUnit)
    return ret


def BioFailed(ret):
    if isinstance(ret, ErrorCode):
        ret = ret.value
    if c_ulong(ret).value >= c_ulong(0xC0000000).value:
        return True
    return False


class TArray(object):
    
    @staticmethod
    def ToInt32(TArrayObj, autoFree):
        if TArrayObj == 0 or TArray.getLength(TArrayObj) == 0:
            return None
        count = TArray.getLength(TArrayObj)
        arr = []
        for i in range(count):
            item = TArray.getItem(TArrayObj, i)
            int_obj = cast(item, POINTER(c_int32)).contents
            arr.append(int_obj.value)

        if autoFree:
            TArray.dispose(TArrayObj)
        return arr

    @staticmethod
    def ToInt64(TArrayObj, autoFree):
        if TArrayObj == 0 or TArray.getLength(TArrayObj) == 0:
            return None
        count = TArray.getLength(TArrayObj)
        arr = []
        for i in range(count):
            item = TArray.getItem(TArrayObj, i)
            int64_obj = cast(item, POINTER(c_int64)).contents
            arr.append(int64_obj.value)

        if autoFree:
            TArray.dispose(TArrayObj)
        return arr

    @staticmethod
    def ToByte(TArrayObj, autoFree):
        if TArrayObj == 0 or TArray.getLength(TArrayObj) == 0:
            return None
        count = TArray.getLength(TArrayObj)
        arr = []
        for i in range(count):
            item = TArray.getItem(TArrayObj, i)
            byte_obj = cast(item, POINTER(c_byte)).contents
            arr.append(byte_obj.value)

        if autoFree:
            TArray.dispose(TArrayObj)
            return arr

    @staticmethod
    def dispose(TArrayObj):
        dll.TArray_Dispose.argtypes = [c_uint64]
        dll.TArray_Dispose(TArrayObj)

    @staticmethod
    def getLength(TArrayObj):
        dll.TArray_getLength.argtypes = [c_uint64]
        dll.TArray_getLength.restype = c_int32
        return dll.TArray_getLength(TArrayObj)

    @staticmethod
    def getItem(TArrayObj, index):
        dll.TArray_getItem.argtypes = [c_uint64, c_int32]
        dll.TArray_getItem.restype = c_uint64
        return dll.TArray_getItem(TArrayObj, index)

    @staticmethod
    def toDeviceTreeNode(nativeArr, autoFree=True):
        count = TArray.getLength(nativeArr)
        DeviceTreeNodeList = []
        for i in range(count):
            item = TArray.getItem(nativeArr, i)
            deviceTreeNodeObjSave = DeviceTreeNode()
            deviceTreeNodeObj = cast(item, POINTER(DeviceTreeNode)).contents

            deviceTreeNodeObjSave.DevicIntEnumber = deviceTreeNodeObj.DevicIntEnumber
            deviceTreeNodeObjSave.Description = deviceTreeNodeObj.Description
            for j in range(8):
                deviceTreeNodeObjSave.ModulesIndex[j] = deviceTreeNodeObj.ModulesIndex[j]

            DeviceTreeNodeList.append(deviceTreeNodeObjSave)
            del deviceTreeNodeObj
        if autoFree:
            TArray.dispose(nativeArr)
        return DeviceTreeNodeList

    @staticmethod
    def ToEnum(nptr, autoFree, enumName, convert):
        if nptr == 0:
            return None
        count = TArray.getLength(nptr)
        data_list = []
        for i in range(count):
            item = TArray.getItem(nptr, i)
            enumValue = cast(item, POINTER(c_int)).contents.value
            # cast to enum
            enumObj = convert(enumValue)
            data_list.append(enumObj)
        if autoFree:
            TArray.dispose(nptr)
        return data_list

    @staticmethod
    def ToTerminalBoard(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, TerminalBoard, Utils.toTerminalBoard)

    @staticmethod
    def ToEventId(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, EventId, Utils.toEventId)

    @staticmethod
    def toAccessMode(nativeArr, autoFree=True):
        return TArray.ToEnum(nativeArr, autoFree, AccessMode, Utils.toAccessMode)

    @staticmethod
    def ToValueRange(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, ValueRange, Utils.toValueRange)

    @staticmethod
    def ToAiSignalType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, AiSignalType, Utils.toAiSignalType)

    @staticmethod
    def ToBurnoutRetType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, BurnoutRetType, Utils.toBurnoutRetType)

    @staticmethod
    def ToFilterType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, FilterType, Utils.toFilterType)

    @staticmethod
    def ToSignalDrop(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, SignalDrop, Utils.toSignalDrop)

    @staticmethod
    def ToActiveSignal(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, ActiveSignal, Utils.toActiveSignal)

    @staticmethod
    def ToActiveSignal(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, ActiveSignal, Utils.toActiveSignal)

    @staticmethod
    def ToTriggerAction(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, TriggerAction, Utils.toTriggerAction)

    @staticmethod
    def ToCounterCapability(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, CounterCapability, Utils.toCounterCapability)

    @staticmethod
    def ToSignalPolarity(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, SignalPolarity, Utils.toSignalPolarity)

    @staticmethod
    def ToOutSignalType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, OutSignalType, Utils.toOutSignaleType)

    @staticmethod
    def ToFreqMeasureMethod(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, FreqMeasureMethod, Utils.toFreqMeasureMethod)

    @staticmethod
    def ToCounterCascadeGroup(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, CounterCascadeGroup, Utils.toCounterCascadeGroup)

    @staticmethod
    def ToCountingType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, CountingType, Utils.toCountingType)

    @staticmethod
    def ToCouplingType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, CouplingType, Utils.toCouplingType)

    @staticmethod
    def ToIepeType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, IepeType, Utils.toIepeType)

    @staticmethod
    def ToImpedanceType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, ImpedanceType, Utils.toImpedanceType)

    @staticmethod
    def ToDoCircuitType(nativeArr, autoFree):
        return TArray.ToEnum(nativeArr, autoFree, DoCircuitType, Utils.toDoCircuitType)


class TScanChannel(object):
    @staticmethod
    def getChannelStart(obj):
        dll.TScanChannel_getChannelStart.restype = c_int32
        dll.TScanChannel_getChannelStart.argtypes = [c_uint64]
        return dll.TScanChannel_getChannelStart(obj)

    @staticmethod
    def setChannelStart(obj, value):
        dll.TScanChannel_setChannelStart.argtypes = [c_uint64, c_int32]
        return dll.TScanChannel_setChannelStart(obj, value)

    @staticmethod
    def getChannelCount(obj):
        dll.TScanChannel_getChannelCount.restype = c_int32
        dll.TScanChannel_getChannelCount.argtypes = [c_uint64]
        return dll.TScanChannel_getChannelCount(obj)

    @staticmethod
    def setChannelCount(obj, value):
        dll.TScanChannel_setChannelCount.argtypes = [c_uint64, c_int32]
        return dll.TScanChannel_setChannelCount(obj, value)

    @staticmethod
    def getIntervalCount(obj):
        dll.TScanChannel_getIntervalCount.restype = c_int32
        dll.TScanChannel_getIntervalCount.argtypes = [c_uint64]
        return dll.TScanChannel_getIntervalCount(obj)

    @staticmethod
    def setIntervalCount(obj, value):
        dll.TScanChannel_setIntervalCount.argtypes = [c_uint64, c_int32]
        return dll.TScanChannel_setIntervalCount(obj, value)

    @staticmethod
    def getSamples(obj):
        dll.TScanChannel_getSamples.restype = c_int32
        dll.TScanChannel_getSamples.argtypes = [c_uint64]
        return dll.TScanChannel_getSamples(obj)

    @staticmethod
    def setSamples(obj, value):
        dll.TScanChannel_setSamples.argtypes = [c_uint64, c_int32]
        return dll.TScanChannel_setSamples(obj, value)


class TConvertClock(object):
    @staticmethod
    def getSource(obj):
        dll.TConvertClock_getSource.argtypes = [c_uint64]
        return dll.TConvertClock_getSource(obj)

    @staticmethod
    def setSource(obj, value):
        dll.TConvertClock_setSource.argtypes = [c_uint64, c_int32]
        return dll.TConvertClock_setSource(obj, value)

    @staticmethod
    def getRate(obj):
        dll.TConvertClock_getRate.restype = c_double
        dll.TConvertClock_getRate.argtypes = [c_uint64]
        return dll.TConvertClock_getRate(obj)

    @staticmethod
    def setRate(obj, value):
        dll.TConvertClock_setRate.argtypes = [c_uint64, c_double]
        return dll.TConvertClock_setRate(obj, c_double(value))


class TTrigger(object):
    @staticmethod
    def getSource(obj):
        dll.TTrigger_getSource.argtypes = [c_uint64]
        dll.TTrigger_getSource.restype = c_int32
        return dll.TTrigger_getSource(obj)

    @staticmethod
    def setSource(obj, value):
        dll.TTrigger_setSource.argtypes = [c_uint64, c_int32]
        return dll.TTrigger_setSource(obj, value)

    @staticmethod
    def getEdge(obj):
        dll.TTrigger_getEdge.argtypes = [c_uint64]
        dll.TTrigger_getEdge.restype = c_int32
        return dll.TTrigger_getEdge(obj)

    @staticmethod
    def setEdge(obj, value):
        dll.TTrigger_setEdge.argtypes = [c_uint64, c_int32]
        return dll.TTrigger_setEdge(obj, value)

    @staticmethod
    def getLevel(obj):
        dll.TTrigger_getLevel.argtypes = [c_uint64]
        dll.TTrigger_getLevel.restype = c_double
        return dll.TTrigger_getLevel(obj)

    @staticmethod
    def setLevel(obj, value):
        dll.TTrigger_setLevel.argtypes = [c_uint64, c_double]
        return dll.TTrigger_setLevel(obj, c_double(value))

    @staticmethod
    def getAction(obj):
        dll.TTrigger_getAction.argtypes = [c_uint64]
        dll.TTrigger_getAction.restype = c_int32
        return dll.TTrigger_getAction(obj)

    @staticmethod
    def setAction(obj, value):
        dll.TTrigger_setAction.argtypes = [c_uint64, c_int32]
        return dll.TTrigger_setAction(obj, value)

    @staticmethod
    def getDelayCount(obj):
        dll.TTrigger_getDelayCount.argtypes = [c_uint64]
        dll.TTrigger_getDelayCount.restype = c_int32
        return dll.TTrigger_getDelayCount(obj)

    @staticmethod
    def setDelayCount(obj, value):
        dll.TTrigger_setDelayCount.argtypes = [c_uint64, c_int32]
        return dll.TTrigger_setDelayCount(obj, value)

    @staticmethod
    def getHysteresisIndex(obj):
        dll.TTrigger_getHysteresisIndex.argtypes = [c_uint64]
        dll.TTrigger_getHysteresisIndex.restype = c_double
        return dll.TTrigger_getHysteresisIndex(obj)

    @staticmethod
    def setHysteresisIndex(obj, value):
        dll.TTrigger_setHysteresisIndex.argtypes = [c_uint64, c_double]
        return dll.TTrigger_setHysteresisIndex(obj, c_double(value))

    @staticmethod
    def getFilterType(obj):
        dll.TTrigger_getFilterType.argtypes = [c_uint64]
        dll.TTrigger_getFilterType.restype = c_int32
        return dll.TTrigger_getFilterType(obj)

    @staticmethod
    def setFilterType(obj, value):
        dll.TTrigger_setFilterType.argtypes = [c_uint64, c_int32]
        return dll.TTrigger_setFilterType(obj, value)

    @staticmethod
    def getFilterCutoffFreq(obj):
        dll.TTrigger_getFilterCutoffFreq.argtypes = [c_uint64]
        dll.TTrigger_getFilterCutoffFreq.restype = c_double
        return dll.TTrigger_getFilterCutoffFreq(obj)

    @staticmethod
    def setFilterCutoffFreq(obj, value):
        dll.TTrigger_setFilterCutoffFreq.argtypes = [c_uint64, c_double]
        return dll.TTrigger_setFilterCutoffFreq(obj, c_double(value))


class TConversion(object):
    @staticmethod
    def getClockSource(obj):
        dll.TConversion_getClockSource.argtypes = [c_uint64]
        return dll.TConversion_getClockSource(obj)

    @staticmethod
    def setClockSource(obj, value):
        dll.TConversion_setClockSource.argtypes = [c_uint64, c_int32]
        return dll.TConversion_setClockSource(obj, value)

    @staticmethod
    def getClockRate(obj):
        dll.TConversion_getClockRate.restype = c_double
        dll.TConversion_getClockRate.argtypes = [c_uint64]
        return dll.TConversion_getClockRate(obj)

    @staticmethod
    def setClockRate(obj, value):
        dll.TConversion_setClockRate.argtypes = [c_uint64, c_double]
        return dll.TConversion_setClockRate(obj, c_double(value))

    @staticmethod
    def getChannelStart(obj):
        dll.TConversion_getChannelStart.restype = c_int32
        dll.TConversion_getChannelStart.argtypes = [c_uint64]
        return dll.TConversion_getChannelStart(obj)

    @staticmethod
    def setChannelStart(obj, value):
        dll.TConversion_setChannelStart.argtypes = [c_uint64, c_int32]
        return dll.TConversion_setChannelStart(obj, value)

    @staticmethod
    def getChannelCount(obj):
        dll.TConversion_getChannelCount.restype = c_int32
        dll.TConversion_getChannelCount.argtypes = [c_uint64]
        return dll.TConversion_getChannelCount(obj)

    @staticmethod
    def setChannelCount(obj, value):
        dll.TConversion_setChannelCount.argtypes = [c_uint64, c_int32]
        return dll.TConversion_setChannelCount(obj, value)

    @staticmethod
    def getChannelMap(obj, count, chMap):
        dll.TConversion_getChannelMap.argtypes = [c_uint64, c_int32, POINTER(c_byte)]  # need attention
        return dll.TConversion_getChannelMap(obj, count, chMap)

    @staticmethod
    def setChannelMap(obj, count, chMap):
        dll.TConversion_setChannelMap.argtypes = [c_uint64, c_int32, POINTER(c_byte)]  # need attention
        return dll.TConversion_setChannelMap(obj, count, chMap)


class TRecord(object):
    @staticmethod
    def getSectionLength(obj):
        dll.TRecord_getSectionLength.restype = c_int32
        dll.TRecord_getSectionLength.argtypes = [c_uint64]
        return dll.TRecord_getSectionLength(obj)

    @staticmethod
    def setSectionLength(obj, value):
        dll.TRecord_setSectionLength.argtypes = [c_uint64, c_int32]
        return dll.TRecord_setSectionLength(obj, value)

    @staticmethod
    def getSectionCount(obj):
        dll.TRecord_getSectionCount.argtypes = [c_uint64]
        return dll.TRecord_getSectionCount(obj)

    @staticmethod
    def setSectionCount(obj, value):
        dll.TRecord_setSectionCount.argtypes = [c_uint64, c_int32]
        return dll.TRecord_setSectionCount(obj, value)

    @staticmethod
    def getCycles(obj):
        dll.TRecord_getCycles.restype = c_int32
        dll.TRecord_getCycles.argtypes = [c_uint64]
        return dll.TRecord_getCycles(obj)

    @staticmethod
    def setCycles(obj, value):
        dll.TRecord_setCycles.argtypes = [c_uint64, c_int32]
        return dll.TRecord_setCycles(obj, value)


class TNosFltChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TNosFltChannel_getChannel.argtypes = [c_uint64]
        return dll.TNosFltChannel_getChannel(obj)

    @staticmethod
    def getEnabled(obj):
        dll.TNosFltChannel_getEnabled.restype = c_int8
        dll.TNosFltChannel_getEnabled.argtypes = [c_uint64]
        return dll.TNosFltChannel_getEnabled(obj)

    @staticmethod
    def setEnabled(obj, value):
        dll.TNosFltChannel_setEnabled.argtypes = [c_uint64, c_int8]
        return dll.TNosFltChannel_setEnabled(obj, value)


class TDeviceCtrl(object):
    @staticmethod
    def Refresh(dev_obj):
        dll.TDeviceCtrl_Refresh.argtypes = [c_void_p]
        return dll.TDeviceCtrl_Refresh(dev_obj)

    @staticmethod
    def ReadRegister(dev_obj, space, offset, length, data_arr):
        dll.TDeviceCtrl_ReadRegister.argtypes = [c_void_p, c_int32, c_int32, c_int32, c_void_p]    # need attention
        return dll.TDeviceCtrl_ReadRegister(dev_obj, space, offset, length, data_arr)

    @staticmethod
    def WriteRegister(dev_obj, space, offset, length, data_arr):
        dll.TDeviceCtrl_WriteRegister.argtypes = [c_void_p, c_int32, c_int32, c_int32, c_void_p]    # need attention]
        return dll.TDeviceCtrl_WriteRegister(dev_obj, space, offset, length, data_arr)

    @staticmethod
    def ReadPrivateRegion(dev_obj, signature, length, data_arr):
        dll.TDeviceCtrl_ReadPrivateRegion.argtypes = [c_void_p, c_int32, c_int32, POINTER(c_uint8)]    # need attention]
        return dll.TDeviceCtrl_ReadPrivateRegion(dev_obj, signature, length, data_arr)

    @staticmethod
    def WritePrivateRegion(dev_obj, signature, length, data_arr):
        dll.TDeviceCtrl_WritePrivateRegion.argtypes = [c_void_p, c_int32, c_int32, POINTER(c_uint8)]    # need attention]]
        return dll.TDeviceCtrl_WritePrivateRegion(dev_obj, signature, length, data_arr)

    @staticmethod
    def SynchronizeTimebase(dev_obj):
        dll.TDeviceCtrl_SynchronizeTimebase.argtypes = [c_void_p]
        return dll.TDeviceCtrl_SynchronizeTimebase(dev_obj)

    @staticmethod
    def CalculateAbsoluteTime(dev_obj, relativeTime):
        dll.TDeviceCtrl_CalculateAbsoluteTime.restype = c_double
        dll.TDeviceCtrl_CalculateAbsoluteTime.argtypes = [c_void_p, c_double]
        return dll.TDeviceCtrl_CalculateAbsoluteTime(dev_obj, c_double(relativeTime))

    @staticmethod
    def getDeviceNumber(dev_obj):
        dll.TDeviceCtrl_getDeviceNumber.restype = c_int32
        dll.TDeviceCtrl_getDeviceNumber.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getDeviceNumber(dev_obj)

    @staticmethod
    def getDescription(dev_obj, length, descr):
        dll.TDeviceCtrl_getDescription.argtypes = [c_void_p, c_int32, c_wchar_p]   # need attention
        return dll.TDeviceCtrl_getDescription(dev_obj, length, descr)

    @staticmethod
    def setDescription(dev_obj, length, descr):
        dll.TDeviceCtrl_setDescription.argtypes = [c_void_p, c_int32, c_wchar_p]   # need attention]
        return dll.TDeviceCtrl_setDescription(dev_obj, length, descr)

    @staticmethod
    def getAccessMode(dev_obj):
        dll.TDeviceCtrl_getAccessMode.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getAccessMode(dev_obj)

    @staticmethod
    def getProductId(dev_obj):
        dll.TDeviceCtrl_getProductId.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getProductId(dev_obj)

    @staticmethod
    def getBoardId(dev_obj):
        dll.TDeviceCtrl_getBoardId.restype = c_int32
        dll.TDeviceCtrl_getBoardId.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getBoardId(dev_obj)

    @staticmethod
    def setBoardId(dev_obj, value):
        dll.TDeviceCtrl_setBoardId.argtypes = [c_void_p, c_int32]
        return dll.TDeviceCtrl_setBoardId(dev_obj, value)

    @staticmethod
    def getBoardVersion(dev_obj, length, version):
        dll.TDeviceCtrl_getBoardVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
        return dll.TDeviceCtrl_getBoardVersion(dev_obj, length, version)

    @staticmethod
    def getDriverVersion(dev_obj, length, version):
        dll.TDeviceCtrl_getDriverVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
        return dll.TDeviceCtrl_getDriverVersion(dev_obj, length, version)

    @staticmethod
    def getDllVersion(dev_obj, length, version):
        dll.TDeviceCtrl_getDllVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
        return dll.TDeviceCtrl_getDllVersion(dev_obj, length, version)

    @staticmethod
    def getLocation(dev_obj, length, location):
        dll.TDeviceCtrl_getLocation.argtypes = [c_void_p, c_int32, c_wchar_p]
        return dll.TDeviceCtrl_getLocation(dev_obj, length, location)

    @staticmethod
    def getPrivateRegionLength(dev_obj):
        dll.TDeviceCtrl_getPrivateRegionLength.restype = c_int32
        dll.TDeviceCtrl_getPrivateRegionLength.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getPrivateRegionLength(dev_obj)

    @staticmethod
    def getHotResetPreventable(dev_obj):
        dll.TDeviceCtrl_getHotResetPreventable.restype = c_int32
        dll.TDeviceCtrl_getHotResetPreventable.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getHotResetPreventable(dev_obj)

    @staticmethod
    def getBaseAddresses(dev_obj):
        dll.TDeviceCtrl_getBaseAddresses.argtypes = [c_void_p]
        dll.TDeviceCtrl_getBaseAddresses.restype = c_uint64
        return dll.TDeviceCtrl_getBaseAddresses(dev_obj)

    @staticmethod
    def getInterrupts(dev_obj):
        dll.TDeviceCtrl_getInterrupts.argtypes = [c_void_p]
        dll.TDeviceCtrl_getInterrupts.restype = c_uint64
        return dll.TDeviceCtrl_getInterrupts(dev_obj)

    @staticmethod
    def getSupportedTerminalBoard(dev_obj):
        dll.TDeviceCtrl_getSupportedTerminalBoard.argtypes = [c_void_p]
        dll.TDeviceCtrl_getSupportedTerminalBoard.restype = c_uint64
        return dll.TDeviceCtrl_getSupportedTerminalBoard(dev_obj)

    @staticmethod
    def getSupportedEvents(dev_obj):
        dll.TDeviceCtrl_getSupportedEvents.argtypes = [c_void_p]
        dll.TDeviceCtrl_getSupportedEvents.restype = c_uint64
        return dll.TDeviceCtrl_getSupportedEvents(dev_obj)

    @staticmethod
    def getSupportedScenarios(dev_obj):
        dll.TDeviceCtrl_getSupportedScenarios.restype = c_int32
        dll.TDeviceCtrl_getSupportedScenarios.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getSupportedScenarios(dev_obj)

    @staticmethod
    def getTerminalBoard(dev_obj):
        dll.TDeviceCtrl_getTerminalBoard.argtypes = [c_void_p]
        return dll.TDeviceCtrl_getTerminalBoard(dev_obj)

    @staticmethod
    def setTerminalBoard(dev_obj, value):
        dll.TDeviceCtrl_setTerminalBoard.argtypes = [c_void_p, c_int32]
        return dll.TDeviceCtrl_setTerminalBoard(dev_obj, value)

    @staticmethod
    def setLocateEnabled(dev_obj, value):
        dll.TDeviceCtrl_setLocateEnabled.argtypes = [c_void_p, c_int32]
        return dll.TDeviceCtrl_setLocateEnabled(dev_obj, value)

    @staticmethod
    def getInstalledDevices():
        dll.TDeviceCtrl_getInstalledDevices.restype = c_uint64
        return dll.TDeviceCtrl_getInstalledDevices()

    @staticmethod
    def getHwSpecific(dev_obj, name, pSize, dataArr):
        dll.TDeviceCtrl_getHwSpecific.argtypes = [c_void_p, c_wchar_p, POINTER(c_int32), c_void_p]
        return dll.TDeviceCtrl_getHwSpecific(dev_obj, name, pSize, dataArr)

    @staticmethod
    def setHwSpecific(dev_obj, name, size, dataArr):
        dll.TDeviceCtrl_setHwSpecific.argtypes = [c_void_p, c_wchar_p, c_int32, c_void_p]
        return dll.TDeviceCtrl_setHwSpecific(dev_obj, name, size, dataArr)


class TDaqCtrlBase(object):
    @staticmethod
    def addEventHandler(obj, eventId, eventProc, userParam):
        dll.TDaqCtrlBase_addEventHandler.argtypes = [c_uint64]
        dll.TDaqCtrlBase_addEventHandler(obj, eventId, eventProc, userParam)  # after add types

    @staticmethod
    def removeEventHandler(obj, eventId, eventProc, userParam):
        dll.TDaqCtrlBase_removeEventHandler.argtypes = [c_uint64]
        dll.TDaqCtrlBase_removeEventHandler(obj, eventId, eventProc, userParam)   # after add types

    @staticmethod
    def cleanup(obj):
        dll.TDaqCtrlBase_Cleanup.argtypes = [c_uint64]
        dll.TDaqCtrlBase_Cleanup(obj)

    @staticmethod
    def dispose(obj):
        dll.TDaqCtrlBase_Dispose.argtypes = [c_uint64]
        dll.TDaqCtrlBase_Dispose(obj)

    @staticmethod
    def getSelectedDevice(obj, devInfo):
        dll.TDaqCtrlBase_getSelectedDevice.argtypes = [c_uint64, POINTER(DeviceInformation)]
        return dll.TDaqCtrlBase_getSelectedDevice(obj, byref(devInfo))

    @staticmethod
    def setSelectedDevice(obj, devInfo):
        dll.TDaqCtrlBase_setSelectedDevice.argtypes = [c_uint64, POINTER(DeviceInformation)]
        return dll.TDaqCtrlBase_setSelectedDevice(obj, byref(devInfo))

    @staticmethod
    def getState(obj):
        dll.TDaqCtrlBase_getState.argtypes = [c_uint64]
        return dll.TDaqCtrlBase_getState(obj)

    @staticmethod
    def getDevice(obj):
        dll.TDaqCtrlBase_getDevice.argtypes = [c_uint64]
        dll.TDaqCtrlBase_getDevice.restype = c_void_p
        return dll.TDaqCtrlBase_getDevice(obj)

    @staticmethod
    def getSupportedDevices(obj):
        dll.TDaqCtrlBase_getSupportedDevices.argtypes = [c_uint64]
        dll.TDaqCtrlBase_getSupportedDevices.restype = c_uint64
        return dll.TDaqCtrlBase_getSupportedDevices(obj)

    @staticmethod
    def getSupportedModes(obj):
        dll.TDaqCtrlBase_getSupportedModes.argtypes = [c_uint64]
        dll.TDaqCtrlBase_getSupportedModes.restype = c_uint64
        return dll.TDaqCtrlBase_getSupportedModes(obj)

    @staticmethod
    def Create(scenario):
        dll.TDaqCtrlBase_Create.argtypes = [c_int32]
        dll.TDaqCtrlBase_Create.restype = c_uint64
        return dll.TDaqCtrlBase_Create(scenario)

    @staticmethod
    def getModule(obj):
        dll.TDaqCtrlBase_getModule.argtypes = [c_uint64]
        dll.TDaqCtrlBase_getModule.restype = c_void_p
        return dll.TDaqCtrlBase_getModule(obj)

    @staticmethod
    def LoadProfile(obj, profile):
        dll.TDaqCtrlBase_LoadProfile.argtypes = [c_uint64, c_wchar_p]
        return dll.TDaqCtrlBase_LoadProfile(obj, profile)


class TAoCtrlBase(object):
    @staticmethod
    def getFeatures(obj):
        dll.TAoCtrlBase_getFeatures.argtypes = [c_uint64]
        dll.TAoCtrlBase_getFeatures.restype = c_uint64
        return dll.TAoCtrlBase_getFeatures(obj)

    @staticmethod
    def getChannels(obj):
        dll.TAoCtrlBase_getChannels.argtypes = [c_uint64]
        dll.TAoCtrlBase_getChannels.restype = c_uint64
        return dll.TAoCtrlBase_getChannels(obj)

    @staticmethod
    def getChannelCount(obj):
        dll.TAoCtrlBase_getChannelCount.restype = c_int32
        dll.TAoCtrlBase_getChannelCount.argtypes = [c_uint64]
        return dll.TAoCtrlBase_getChannelCount(obj)

    @staticmethod
    def getExtRefValueForUnipolar(obj):
        dll.TAoCtrlBase_getExtRefValueForUnipolar.restype = c_double
        dll.TAoCtrlBase_getExtRefValueForUnipolar.argtypes = [c_uint64]
        return dll.TAoCtrlBase_getExtRefValueForUnipolar(obj)

    @staticmethod
    def setExtRefValueForUnipolar(obj, value):
        dll.TAoCtrlBase_setExtRefValueForUnipolar.argtypes = [c_uint64, c_double]
        return dll.TAoCtrlBase_setExtRefValueForUnipolar(obj, c_double(value))

    @staticmethod
    def getExtRefValueForBipolar(obj):
        dll.TAoCtrlBase_getExtRefValueForBipolar.restype = c_double
        dll.TAoCtrlBase_getExtRefValueForBipolar.argtypes = [c_uint64]
        return dll.TAoCtrlBase_getExtRefValueForBipolar(obj)

    @staticmethod
    def setExtRefValueForBipolar(obj, value):
        dll.TAoCtrlBase_setExtRefValueForBipolar.argtypes = [c_uint64, c_double]
        return dll.TAoCtrlBase_setExtRefValueForBipolar(obj, c_double(value))


class TInstantAoCtrl(object):
    @staticmethod
    def writeAny(obj, chStart, chCount, dataRaw, dataScaled):
        dll.TInstantAoCtrl_WriteAny.argtypes = [c_uint64, c_int32, c_int32, c_void_p, POINTER(c_double)]
        return dll.TInstantAoCtrl_WriteAny(obj, chStart, chCount, dataRaw, dataScaled)


class TAoFeatures(object):
    # DAC features
    @staticmethod
    def getResolution(aoFeatureObj):
        dll.TAoFeatures_getResolution.restype = c_int32
        dll.TAoFeatures_getResolution.argtypes = [c_uint64]
        return dll.TAoFeatures_getResolution(aoFeatureObj)

    @staticmethod
    def getDataSize(aoFeatureObj):
        dll.TAoFeatures_getDataSize.restype = c_int32
        dll.TAoFeatures_getDataSize.argtypes = [c_uint64]
        return dll.TAoFeatures_getDataSize(aoFeatureObj)

    @staticmethod
    def getDataMask(aoFeatureObj):
        dll.TAoFeatures_getDataMask.restype = c_int32
        dll.TAoFeatures_getDataMask.argtypes = [c_uint64]
        return dll.TAoFeatures_getDataMask(aoFeatureObj)

    # channel features
    @staticmethod
    def getChannelCountMax(aoFeatureObj):
        dll.TAoFeatures_getChannelCountMax.restype = c_int32
        dll.TAoFeatures_getChannelCountMax.argtypes = [c_uint64]
        return dll.TAoFeatures_getChannelCountMax(aoFeatureObj)

    @staticmethod
    def getValueRanges(aoFeatureObj):
        dll.TAoFeatures_getValueRanges.argtypes = [c_uint64]
        dll.TAoFeatures_getValueRanges.restype = c_uint64
        return dll.TAoFeatures_getValueRanges(aoFeatureObj)

    @staticmethod
    def getExternalRefAntiPolar(aoFeatureObj):
        dll.TAoFeatures_getExternalRefAntiPolar.restype = c_int8
        dll.TAoFeatures_getExternalRefAntiPolar.argtypes = [c_uint64]
        return dll.TAoFeatures_getExternalRefAntiPolar(aoFeatureObj)

    @staticmethod
    def getExternalRefRange(aoFeatureObj, mathIntervalObj):
        dll.TAoFeatures_getExternalRefRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAoFeatures_getExternalRefRange(aoFeatureObj, mathIntervalObj)

    # buffered ao->basic features
    @staticmethod
    def getBufferedAoSupported(aoFeatureObj):
        dll.TAoFeatures_getBufferedAoSupported.restype = c_int8
        dll.TAoFeatures_getBufferedAoSupported.argtypes = [c_uint64]
        return dll.TAoFeatures_getBufferedAoSupported(aoFeatureObj)

    @staticmethod
    def getSamplingMethod(aoFeatureObj):
        dll.TAoFeatures_getSamplingMethod.argtypes = [c_uint64]
        return dll.TAoFeatures_getSamplingMethod(aoFeatureObj)

    @staticmethod
    def getChannelStartBase(aoFeatureObj):
        dll.TAoFeatures_getChannelStartBase.restype = c_int32
        dll.TAoFeatures_getChannelStartBase.argtypes = [c_uint64]
        return dll.TAoFeatures_getChannelStartBase(aoFeatureObj)

    @staticmethod
    def getChannelCountBase(aoFeatureObj):
        dll.TAoFeatures_getChannelCountBase.restype = c_int32
        dll.TAoFeatures_getChannelCountBase.argtypes = [c_uint64]
        return dll.TAoFeatures_getChannelCountBase(aoFeatureObj)

    # buffered ao->conversion clock features
    @staticmethod
    def getConvertClockSources(aoFeatureObj):
        dll.TAoFeatures_getConvertClockSources.argtypes = [c_uint64]
        dll.TAoFeatures_getConvertClockSources.restype = c_uint64
        return dll.TAoFeatures_getConvertClockSources(aoFeatureObj)

    @staticmethod
    def getConvertClockRange(aoFeatureObj, mathInterval):
        dll.TAoFeatures_getConvertClockRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAoFeatures_getConvertClockRange(aoFeatureObj, mathInterval)

    # buffered ao->trigger features
    @staticmethod
    def getTriggerCount(aoFeatureObj):
        dll.TAoFeatures_getTriggerCount.restype = c_int32
        dll.TAoFeatures_getTriggerCount.argtypes = [c_uint64]
        return dll.TAoFeatures_getTriggerCount(aoFeatureObj)

    @staticmethod
    def getRetriggerable(aoFeatureObj):
        dll.TAoFeatures_getRetriggerable.restype = c_int8
        dll.TAoFeatures_getRetriggerable.argtypes = [c_uint64]
        return dll.TAoFeatures_getRetriggerable(aoFeatureObj)

    # buffered ao->trigger0/1/.../x features
    @staticmethod
    def getTriggerSources(aoFeatureObj, trigger):
        dll.TAoFeatures_getTriggerSources.argtypes = [c_uint64, c_int32]
        dll.TAoFeatures_getTriggerSources.restype = c_uint64
        return dll.TAoFeatures_getTriggerSources(aoFeatureObj, trigger)

    @staticmethod
    def getTriggerActions(aoFeatureObj, trigger):
        dll.TAoFeatures_getTriggerActions.argtypes = [c_uint64, c_int32]
        dll.TAoFeatures_getTriggerActions.restype = c_uint64
        return dll.TAoFeatures_getTriggerActions(aoFeatureObj, trigger)

    @staticmethod
    def getTriggerDelayRange(aoFeatureObj, trigger, mathIntervalX):
        dll.TAoFeatures_getTriggerDelayRange.argtypes = [c_uint64, c_int32, POINTER(MathInterval)]
        return dll.TAoFeatures_getTriggerDelayRange(aoFeatureObj, trigger, mathIntervalX)


class TAoChannel(object):
    @staticmethod
    def getChannel(aoChannelObj):
        dll.TAoChannel_getChannel.restype = c_int32
        dll.TAoChannel_getChannel.argtypes = [c_uint64]
        return dll.TAoChannel_getChannel(aoChannelObj)

    @staticmethod
    def getValueRange(aoChannelObj):
        dll.TAoChannel_getValueRange.argtypes = [c_uint64]
        return dll.TAoChannel_getValueRange(aoChannelObj)

    @staticmethod
    def setValueRange(aoChannelObj, valueRange):
        dll.TAoChannel_setValueRange.argtypes = [c_uint64, c_int32]
        return dll.TAoChannel_setValueRange(aoChannelObj, valueRange)

    @staticmethod
    def getExtRefBipolar(aoChannelObj):
        dll.TAoChannel_getExtRefBipolar.restype = c_double
        dll.TAoChannel_getExtRefBipolar.argtypes = [c_uint64]
        return dll.TAoChannel_getExtRefBipolar(aoChannelObj)

    @staticmethod
    def setExtRefBipolar(aoChannelObj, value):
        dll.TAoChannel_setExtRefBipolar.argtypes = [c_uint64, c_double]
        return dll.TAoChannel_setExtRefBipolar(aoChannelObj, c_double(value))

    @staticmethod
    def getExtRefUnipolar(aoChannelObj):
        dll.TAoChannel_getExtRefUnipolar.restype = c_double
        dll.TAoChannel_getExtRefUnipolar.argtypes = [c_uint64]
        return dll.TAoChannel_getExtRefUnipolar(aoChannelObj)

    @staticmethod
    def setExtRefUnipolar(aoChannelObj, value):
        dll.TAoChannel_setExtRefUnipolar.argtypes = [c_uint64, c_double]
        return dll.TAoChannel_setExtRefUnipolar(aoChannelObj, c_double(value))

    # new: scale table
    @staticmethod
    def getScaleTable(aoChannelObj, pSize, mapFuncPieceTable):
        dll.TAoChannel_getScaleTable.argtypes = [c_uint64, POINTER(c_int32), POINTER(MapFuncPiece)]
        return dll.TAoChannel_getScaleTable(aoChannelObj, pSize, mapFuncPieceTable)

    @staticmethod
    def setScaleTable(aoChannelObj, size, mapFuncPieceTable):
        dll.TAoChannel_setScaleTable.argtypes = [c_uint64, c_int32, POINTER(MapFuncPiece)]
        return dll.TAoChannel_setScaleTable(aoChannelObj, size, mapFuncPieceTable)


class TAiCtrlBase(object):
    @staticmethod
    def getFeatures(obj):
        dll.TAiCtrlBase_getFeatures.argtypes = [c_uint64]
        dll.TAiCtrlBase_getFeatures.restype = c_uint64
        return dll.TAiCtrlBase_getFeatures(obj)

    @staticmethod
    def getChannels(obj):
        dll.TAiCtrlBase_getChannels.restype = c_uint64
        dll.TAiCtrlBase_getChannels.argtypes = [c_uint64]
        return dll.TAiCtrlBase_getChannels(obj)

    @staticmethod
    def getChannelCount(obj):
        dll.TAiCtrlBase_getChannelCount.restype = c_int32
        dll.TAiCtrlBase_getChannelCount.argtypes = [c_uint64]
        return dll.TAiCtrlBase_getChannelCount(obj)


class TWaveformAiCtrl(object):
    @staticmethod
    def Prepare(obj):
        dll.TWaveformAiCtrl_Prepare.argtypes = [c_uint64]
        return dll.TWaveformAiCtrl_Prepare(obj)

    @staticmethod
    def Start(obj):
        dll.TWaveformAiCtrl_Start.argtypes = [c_uint64]
        return dll.TWaveformAiCtrl_Start(obj)

    @staticmethod
    def Stop(obj):
        dll.TWaveformAiCtrl_Stop.argtypes = [c_uint64]
        return dll.TWaveformAiCtrl_Stop(obj)

    @staticmethod
    def GetData(obj, dt, count, buffer, timeout, returned, startTime, markCount, makrBuf):
        dll.TWaveformAiCtrl_GetData.argtypes = [c_uint64, c_int32, c_int32, c_void_p, c_int32, POINTER(c_int32), POINTER(c_double), POINTER(c_int32), POINTER(DataMark)]
        return dll.TWaveformAiCtrl_GetData(obj, dt, count, buffer, timeout, returned, startTime, markCount, makrBuf)

    @staticmethod
    def getConversion(obj):
        dll.TWaveformAiCtrl_getConversion.argtypes = [c_uint64]
        dll.TWaveformAiCtrl_getConversion.restype = c_uint64
        return dll.TWaveformAiCtrl_getConversion(obj)

    @staticmethod
    def getRecord(obj):
        dll.TWaveformAiCtrl_getRecord.argtypes = [c_uint64]
        dll.TWaveformAiCtrl_getRecord.restype = c_uint64
        return dll.TWaveformAiCtrl_getRecord(obj)

    @staticmethod
    def getTrigger(obj, trigIdx):
        dll.TWaveformAiCtrl_getTrigger.argtypes = [c_uint64, c_int32]
        dll.TWaveformAiCtrl_getTrigger.restype = c_uint64
        return dll.TWaveformAiCtrl_getTrigger(obj, trigIdx)


class TBufferedAoCtrl(object):
    @staticmethod
    def getScanChannel(obj):
        dll.TBufferedAoCtrl_getScanChannel.argtypes = [c_uint64]
        dll.TBufferedAoCtrl_getScanChannel.restype = c_uint64
        return dll.TBufferedAoCtrl_getScanChannel(obj)

    @staticmethod
    def getConvertClock(obj):
        dll.TBufferedAoCtrl_getConvertClock.argtypes = [c_uint64]
        dll.TBufferedAoCtrl_getConvertClock.restype = c_uint64
        return dll.TBufferedAoCtrl_getConvertClock(obj)

    @staticmethod
    def getTrigger(obj, trigIdx):
        dll.TBufferedAoCtrl_getTrigger.argtypes = [c_uint64, c_int32]
        dll.TBufferedAoCtrl_getTrigger.restype = c_uint64
        return dll.TBufferedAoCtrl_getTrigger(obj, trigIdx)

    @staticmethod
    def getStreaming(obj):
        dll.TBufferedAoCtrl_getStreaming.argtypes = [c_uint64]
        dll.TBufferedAoCtrl_getStreaming.restype = c_int8
        return dll.TBufferedAoCtrl_getStreaming(obj)

    @staticmethod
    def setStreaming(obj, value):
        dll.TBufferedAoCtrl_setStreaming.argtypes = [c_uint64, c_int8]
        return dll.TBufferedAoCtrl_setStreaming(obj, value)

    @staticmethod
    def Prepare(obj):
        dll.TBufferedAoCtrl_Prepare.argtypes = [c_uint64]
        return dll.TBufferedAoCtrl_Prepare(obj)

    @staticmethod
    def RunOnce(obj):
        dll.TBufferedAoCtrl_RunOnce.argtypes = [c_uint64]
        return dll.TBufferedAoCtrl_RunOnce(obj)

    @staticmethod
    def Start(obj):
        dll.TBufferedAoCtrl_Start.argtypes = [c_uint64]
        return dll.TBufferedAoCtrl_Start(obj)

    @staticmethod
    def Stop(obj, value):
        dll.TBufferedAoCtrl_Stop.argtypes = [c_uint64, c_int32]
        return dll.TBufferedAoCtrl_Stop(obj, value)

    @staticmethod
    def SetData(obj, dt, count, buffer):
        dll.TBufferedAoCtrl_SetData.argtypes = [c_uint64, c_int32, c_int32, c_void_p]
        return dll.TBufferedAoCtrl_SetData(obj, dt, count, buffer)


class TInstantAiCtrl(object):
    @staticmethod
    def getCjc(obj):
        dll.TInstantAiCtrl_getCjc.argtypes = [c_uint64]
        dll.TInstantAiCtrl_getCjc.restype = c_uint64
        return dll.TInstantAiCtrl_getCjc(obj)

    @staticmethod
    def getAutoConvertClockRate(obj):
        dll.TInstantAiCtrl_getAutoConvertClockRate.restype = c_double
        dll.TInstantAiCtrl_getAutoConvertClockRate.argtypes = [c_uint64]
        return dll.TInstantAiCtrl_getAutoConvertClockRate(obj)

    @staticmethod
    def setAutoConvertClockRate(obj, value):
        dll.TInstantAiCtrl_setAutoConvertClockRate.argtypes = [c_uint64, c_double]
        return dll.TInstantAiCtrl_setAutoConvertClockRate(obj, c_double(value))

    @staticmethod
    def getAutoConvertChannelStart(obj):
        dll.TInstantAiCtrl_getAutoConvertChannelStart.argtypes = [c_uint64]
        return dll.TInstantAiCtrl_getAutoConvertChannelStart(obj)

    @staticmethod
    def setAutoConvertChannelStart(obj, intValue):
        dll.TInstantAiCtrl_setAutoConvertChannelStart.argtypes = [c_uint64, c_int32]
        return dll.TInstantAiCtrl_setAutoConvertChannelStart(obj, intValue)

    @staticmethod
    def getAutoConvertChannelCount(obj):
        dll.TInstantAiCtrl_getAutoConvertChannelCount.argtypes = [c_uint64]
        return dll.TInstantAiCtrl_getAutoConvertChannelCount(obj)

    @staticmethod
    def setAutoConvertChannelCount(obj, intValue):
        dll.TInstantAiCtrl_setAutoConvertChannelCount.argtypes = [c_uint64, c_int32]
        return dll.TInstantAiCtrl_setAutoConvertChannelCount(obj, intValue)

    @staticmethod
    def readAny(obj, chStart, chCount, dataRaw, dataScaled):
        dll.TInstantAiCtrl_ReadAny.restype = c_uint32
        dll.TInstantAiCtrl_ReadAny.argtypes = [c_uint64, c_int32, c_int32, c_void_p, POINTER(c_double)]
        return dll.TInstantAiCtrl_ReadAny(obj, chStart, chCount, dataRaw, dataScaled)


class TCjcSetting(object):
    @staticmethod
    def getChannel(cjcSetObj):
        dll.TCjcSetting_getChannel.restype = c_int32
        dll.TCjcSetting_getChannel.argtypes = [c_uint64]
        return dll.TCjcSetting_getChannel(cjcSetObj)

    @staticmethod
    def setChannel(cjcSetObj, intCh):
        dll.TCjcSetting_setChannel.argtypes = [c_uint64, c_int32]
        return dll.TCjcSetting_setChannel(cjcSetObj, intCh)

    @staticmethod
    def getValue(cjcSetObj):
        dll.TCjcSetting_getValue.restype = c_double
        dll.TCjcSetting_getValue.argtypes = [c_uint64]
        return dll.TCjcSetting_getValue(cjcSetObj)

    @staticmethod
    def setValue(cjcSetObj, value):
        dll.TCjcSetting_setValue.argtypes = [c_uint64, c_double]
        return dll.TCjcSetting_setValue(cjcSetObj, c_double(value))

    @staticmethod
    def getUpdateFreq(cjcSetObj):
        dll.TCjcSetting_getUpdateFreq.restype = c_double
        dll.TCjcSetting_getUpdateFreq.argtypes = [c_uint64]
        return dll.TCjcSetting_getUpdateFreq(cjcSetObj)

    @staticmethod
    def setUpdateFreq(cjcSetObj, value):
        dll.TCjcSetting_setUpdateFreq.argtypes = [c_uint64, c_double]
        return dll.TCjcSetting_setUpdateFreq(cjcSetObj, c_double(value))


class TAiFeatures(object):
    # ADC features
    @staticmethod
    def getResolution(aiFeatureObj):
        dll.TAiFeatures_getResolution.restype = c_int32
        dll.TAiFeatures_getResolution.argtypes = [c_uint64]
        return dll.TAiFeatures_getResolution(aiFeatureObj)

    @staticmethod
    def getDataSize(aiFeatureObj):
        dll.TAiFeatures_getDataSize.restype = c_int32
        dll.TAiFeatures_getDataSize.argtypes = [c_uint64]
        return dll.TAiFeatures_getDataSize(aiFeatureObj)

    @staticmethod
    def getDataMask(aiFeatureObj):
        dll.TAiFeatures_getDataMask.restype = c_int32
        dll.TAiFeatures_getDataMask.argtypes = [c_uint64]
        return dll.TAiFeatures_getDataMask(aiFeatureObj)

    # new: timestamp resolution
    @staticmethod
    def getTimestampResolution(aiFeatureObj):
        dll.TAiFeatures_getTimestampResolution.restype = c_double
        dll.TAiFeatures_getTimestampResolution.argtypes = [c_uint64]
        return dll.TAiFeatures_getTimestampResolution(aiFeatureObj)

    #  channel features
    @staticmethod
    def getChannelCountMax(aiFeatureObj):
        dll.TAiFeatures_getChannelCountMax.restype = c_int32
        dll.TAiFeatures_getChannelCountMax.argtypes = [c_uint64]
        return dll.TAiFeatures_getChannelCountMax(aiFeatureObj)

    @staticmethod
    def getChannelType(aiFeatureObj):
        dll.TAiFeatures_getChannelType.restype = c_int
        dll.TAiFeatures_getChannelType.argtypes = [c_uint64]
        return dll.TAiFeatures_getChannelType(aiFeatureObj)

    @staticmethod
    def getOverallValueRange(aiFeatureObj):
        dll.TAiFeatures_getOverallValueRange.restype = c_int8
        dll.TAiFeatures_getOverallValueRange.argtypes = [c_uint64]
        return dll.TAiFeatures_getOverallValueRange(aiFeatureObj)

    @staticmethod
    def getValueRanges(aiFeatureObj):
        dll.TAiFeatures_getValueRanges.argtypes = [c_uint64]
        dll.TAiFeatures_getValueRanges.restype = c_uint64
        return dll.TAiFeatures_getValueRanges(aiFeatureObj)

    @staticmethod
    def getBurnoutReturnTypes(aiFeatureObj):
        dll.TAiFeatures_getBurnoutReturnTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getBurnoutReturnTypes.restype = c_uint64
        return dll.TAiFeatures_getBurnoutReturnTypes(aiFeatureObj)

    @staticmethod
    def getConnectionTypes(aiFeatureObj):
        dll.TAiFeatures_getConnectionTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getConnectionTypes.restype = c_uint64
        return dll.TAiFeatures_getConnectionTypes(aiFeatureObj)

    @staticmethod
    def getOverallConnection(aiFeatureObj):
        dll.TAiFeatures_getOverallConnection.restype = c_int8
        dll.TAiFeatures_getOverallConnection.argtypes = [c_uint64]
        return dll.TAiFeatures_getOverallConnection(aiFeatureObj)

    # filter
    @staticmethod
    def getFilterTypes(aiFeatureObj):
        dll.TAiFeatures_getFilterTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getFilterTypes.restype = c_uint64
        return dll.TAiFeatures_getFilterTypes(aiFeatureObj)

    @staticmethod
    def getFilterCutoffFreqRange(aiFeaturesObj, mathIntervalVal):
        dll.TAiFeatures_getFilterCutoffFreqRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAiFeatures_getFilterCutoffFreqRange(aiFeaturesObj, mathIntervalVal)

    @staticmethod
    def getFilterCutoffFreq1Range(aiFeaturesObj, mathIntervalVal):
        dll.TAiFeatures_getFilterCutoffFreq1Range.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAiFeatures_getFilterCutoffFreq1Range(aiFeaturesObj, mathIntervalVal)

    # CJC features
    @staticmethod
    def getThermoSupported(aiFeaturesObj):
        dll.TAiFeatures_getThermoSupported.restype = c_int8
        dll.TAiFeatures_getThermoSupported.argtypes = [c_uint64]
        return dll.TAiFeatures_getThermoSupported(aiFeaturesObj)

    @staticmethod
    def getCjcChannels(aiFeaturesObj):
        dll.TAiFeatures_getCjcChannels.argtypes = [c_uint64]
        dll.TAiFeatures_getCjcChannels.restype = c_uint64
        return dll.TAiFeatures_getCjcChannels(aiFeaturesObj)

    # buffered ai -> basic features
    @staticmethod
    def getBufferedAiSupported(aiFeaturesObj):
        dll.TAiFeatures_getBufferedAiSupported.restype = c_int8
        dll.TAiFeatures_getBufferedAiSupported.argtypes = [c_uint64]
        return dll.TAiFeatures_getBufferedAiSupported(aiFeaturesObj)

    @staticmethod
    def getSamplingMethod(aiFeaturesObj):
        dll.TAiFeatures_getSamplingMethod.restype = c_int
        dll.TAiFeatures_getSamplingMethod.argtypes = [c_uint64]
        return dll.TAiFeatures_getSamplingMethod(aiFeaturesObj)

    @staticmethod
    def getChannelStartBase(aiFeaturesObj):
        dll.TAiFeatures_getChannelStartBase.restype = c_int32
        dll.TAiFeatures_getChannelStartBase.argtypes = [c_uint64]
        return dll.TAiFeatures_getChannelStartBase(aiFeaturesObj)

    @staticmethod
    def getChannelCountBase(aiFeaturesObj):
        dll.TAiFeatures_getChannelCountBase.restype = c_int32
        dll.TAiFeatures_getChannelCountBase.argtypes = [c_uint64]
        return dll.TAiFeatures_getChannelCountBase(aiFeaturesObj)

    # buffered ai->conversion clock features
    @staticmethod
    def getConvertClockSources(aiFeaturesObj):
        dll.TAiFeatures_getConvertClockSources.argtypes = [c_uint64]
        dll.TAiFeatures_getConvertClockSources.restype = c_uint64
        return dll.TAiFeatures_getConvertClockSources(aiFeaturesObj)

    @staticmethod
    def getConvertClockRange(aiFeaturesObj, mathIntervalValue):
        dll.TAiFeatures_getConvertClockRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAiFeatures_getConvertClockRange(aiFeaturesObj, mathIntervalValue)

    # buffered ai->burst scan
    @staticmethod
    def getBurstScanSupported(aiFeaturesObj):
        dll.TAiFeatures_getBurstScanSupported.restype = c_int8
        dll.TAiFeatures_getBurstScanSupported.argtypes = [c_uint64]
        return dll.TAiFeatures_getBurstScanSupported(aiFeaturesObj)

    @staticmethod
    def getScanClockSources(aiFeaturesObj):
        dll.TAiFeatures_getScanClockSources.argtypes = [c_uint64]
        dll.TAiFeatures_getScanClockSources.restype = c_uint64
        return dll.TAiFeatures_getScanClockSources(aiFeaturesObj)

    @staticmethod
    def getScanClockRange(aiFeaturesObj, mathIntervalValue):
        dll.TAiFeatures_getScanClockRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TAiFeatures_getScanClockRange(aiFeaturesObj, mathIntervalValue)

    @staticmethod
    def getScanCountMax(aiFeaturesObj):
        dll.TAiFeatures_getScanCountMax.restype = c_int32
        dll.TAiFeatures_getScanCountMax.argtypes = [c_uint64]
        return dll.TAiFeatures_getScanCountMax(aiFeaturesObj)

    # buffered ai->trigger features
    @staticmethod
    def getRetriggerable(aiFeaturesObj):
        dll.TAiFeatures_getRetriggerable.restype = c_int8
        dll.TAiFeatures_getRetriggerable.argtypes = [c_uint64]
        return dll.TAiFeatures_getRetriggerable(aiFeaturesObj)

    @staticmethod
    def getTriggerCount(aiFeaturesObj):
        dll.TAiFeatures_getTriggerCount.restype = c_int32
        dll.TAiFeatures_getTriggerCount.argtypes = [c_uint64]
        return dll.TAiFeatures_getTriggerCount(aiFeaturesObj)

    @staticmethod
    def getTriggerFilterTypes(aiFeaturesObj, reserved):
        dll.TAiFeatures_getTriggerFilterTypes.argtypes = [c_uint64, c_int32]
        dll.TAiFeatures_getTriggerFilterTypes.restype = c_uint64
        return dll.TAiFeatures_getTriggerFilterTypes(aiFeaturesObj, reserved)

    @staticmethod
    def getTriggerFilterCutoffFreqRange(aiFeaturesObj, reserved, mathIntervalValue):
        dll.TAiFeatures_getTriggerFilterCutoffFreqRange.argtypes = [c_uint64, c_int32, POINTER(MathInterval)]
        return dll.TAiFeatures_getTriggerFilterCutoffFreqRange(aiFeaturesObj, reserved, mathIntervalValue)

    # buffered ai->trigger0/1/.../x features
    @staticmethod
    def getTriggerActions(aiFeaturesObj, trigger):
        dll.TAiFeatures_getTriggerActions.argtypes = [c_uint64, c_int32]
        dll.TAiFeatures_getTriggerActions.restype = c_uint64
        return dll.TAiFeatures_getTriggerActions(aiFeaturesObj, trigger)

    @staticmethod
    def getTriggerDelayRange(aiFeaturesObj, trigger, mathIntervalX):
        dll.TAiFeatures_getTriggerDelayRange.argtypes = [c_uint64, c_int32, POINTER(MathInterval)]
        return dll.TAiFeatures_getTriggerDelayRange(aiFeaturesObj, trigger, mathIntervalX)

    @staticmethod
    def getTriggerSources(aiFeaturesObj, trigger):
        dll.TAiFeatures_getTriggerSources.argtypes = [c_uint64, c_int32]
        dll.TAiFeatures_getTriggerSources.restype = c_uint64
        return dll.TAiFeatures_getTriggerSources(aiFeaturesObj, trigger)

    @staticmethod
    def getTriggerSourceVrg(aiFeaturesObj, trigger):
        dll.TAiFeatures_getTriggerSourceVrg.argtypes = [c_uint64, c_int32]
        return dll.TAiFeatures_getTriggerSourceVrg(aiFeaturesObj, trigger)

    @staticmethod
    def getTriggerHysteresisIndexMax(aiFeaturesObj, trigger):
        dll.TAiFeatures_getTriggerHysteresisIndexMax.argtypes = [c_uint64, c_int32]
        dll.TAiFeatures_getTriggerHysteresisIndexMax.restype = c_double
        return dll.TAiFeatures_getTriggerHysteresisIndexMax(aiFeaturesObj, trigger)

    @staticmethod
    def getTriggerHysteresisIndexStep(aiFeaturesObj, trigger):
        dll.TAiFeatures_getTriggerHysteresisIndexStep.argtypes = [c_uint64, c_int32]
        return dll.TAiFeatures_getTriggerHysteresisIndexStep(aiFeaturesObj, trigger)

    # new coupling & IEPE & Impedance
    @staticmethod
    def getCouplingTypes(aiFeaturesObj):
        dll.TAiFeatures_getCouplingTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getCouplingTypes.restype = c_uint64
        return dll.TAiFeatures_getCouplingTypes(aiFeaturesObj)

    @staticmethod
    def getIepeTypes(aiFeaturesObj):
        dll.TAiFeatures_getIepeTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getIepeTypes.restype = c_uint64
        return dll.TAiFeatures_getIepeTypes(aiFeaturesObj)

    @staticmethod
    def getImpedanceTypes(aiFeaturesObj):
        dll.TAiFeatures_getImpedanceTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getImpedanceTypes.restype = c_uint64
        return dll.TAiFeatures_getImpedanceTypes(aiFeaturesObj)

    # new: sensor features
    @staticmethod
    def getMeasureTypes(aiFeaturesObj):
        dll.TAiFeatures_getMeasureTypes.argtypes = [c_uint64]
        dll.TAiFeatures_getMeasureTypes.restype = c_uint64
        return dll.TAiFeatures_getMeasureTypes(aiFeaturesObj)

    @staticmethod
    def getBridgeResistances(aiFeaturesObj):
        dll.TAiFeatures_getBridgeResistances.argtypes = [c_uint64]
        dll.TAiFeatures_getBridgeResistances.restype = c_uint64
        return dll.TAiFeatures_getBridgeResistances(aiFeaturesObj)

    @staticmethod
    def getExcitingVoltageRange(aiFeaturesObj):
        dll.TAiFeatures_getExcitingVoltageRange.argtypes = [c_uint64]
        return dll.TAiFeatures_getExcitingVoltageRange(aiFeaturesObj)


class TAiChannel(object):
    @staticmethod
    def getChannel(aiChannObj):
        dll.TAiChannel_getChannel.restype = c_int32
        dll.TAiChannel_getChannel.argtypes = [c_uint64]
        return dll.TAiChannel_getChannel(aiChannObj)

    @staticmethod
    def getLogicalNumber(aiChannObj):
        dll.TAiChannel_getLogicalNumber.restype = c_int32
        dll.TAiChannel_getLogicalNumber.argtypes = [c_uint64]
        return dll.TAiChannel_getLogicalNumber(aiChannObj)

    @staticmethod
    def getValueRange(aiChannObj):
        dll.TAiChannel_getValueRange.restype = c_int
        dll.TAiChannel_getValueRange.argtypes = [c_uint64]
        return dll.TAiChannel_getValueRange(aiChannObj)

    @staticmethod
    def setValueRange(aiChannObj, valueRangeValue):
        dll.TAiChannel_setValueRange.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setValueRange(aiChannObj, valueRangeValue)

    @staticmethod
    def getSignalType(aiChannObj):
        dll.TAiChannel_getSignalType.restype = c_int
        dll.TAiChannel_getSignalType.argtypes = [c_uint64]
        return dll.TAiChannel_getSignalType(aiChannObj)

    @staticmethod
    def setSignalType(aiChannObj, aiSignalTypeValue):
        dll.TAiChannel_setSignalType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setSignalType(aiChannObj, aiSignalTypeValue)

    @staticmethod
    def getBurnoutRetType(aiChannObj):
        dll.TAiChannel_getBurnoutRetType.restype = c_int
        dll.TAiChannel_getBurnoutRetType.argtypes = [c_uint64]
        return dll.TAiChannel_getBurnoutRetType(aiChannObj)

    @staticmethod
    def setBurnoutRetType(aiChannObj, burnoutRetTypeValue):
        dll.TAiChannel_setBurnoutRetType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setBurnoutRetType(aiChannObj, burnoutRetTypeValue)

    @staticmethod
    def getBurnoutRetValue(aiChannObj):
        dll.TAiChannel_getBurnoutRetValue.restype = c_double
        dll.TAiChannel_getBurnoutRetValue.argtypes = [c_uint64]
        return dll.TAiChannel_getBurnoutRetValue(aiChannObj)

    @staticmethod
    def setBurnoutRetValue(aiChannObj, value):
        dll.TAiChannel_setBurnoutRetValue.argtypes = [c_uint64, c_double]
        return dll.TAiChannel_setBurnoutRetValue(aiChannObj, c_double(value))

    @staticmethod
    def getBurnShortRetValue(aiChannObj):
        dll.TAiChannel_getBurnShortRetValue.restype = c_double
        dll.TAiChannel_getBurnShortRetValue.argtypes = [c_uint64]
        return dll.TAiChannel_getBurnShortRetValue(aiChannObj)

    @staticmethod
    def setBurnShortRetValue(aiChannObj, value):
        dll.TAiChannel_setBurnShortRetValue.argtypes = [c_uint64, c_double]
        return dll.TAiChannel_setBurnShortRetValue(aiChannObj, c_double(value))

    @staticmethod
    def getFilterType(aiChannObj):
        dll.TAiChannel_getFilterType.restype = c_int
        dll.TAiChannel_getFilterType.argtypes = [c_uint64]
        return dll.TAiChannel_getFilterType(aiChannObj)

    @staticmethod
    def setFilterType(aiChannObj, filterTypeValue):
        dll.TAiChannel_setFilterType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setFilterType(aiChannObj, filterTypeValue)

    @staticmethod
    def getFilterCutoffFreq(aiChannObj):
        dll.TAiChannel_getFilterCutoffFreq.restype = c_double
        dll.TAiChannel_getFilterCutoffFreq.argtypes = [c_uint64]
        return dll.TAiChannel_getFilterCutoffFreq(aiChannObj)

    @staticmethod
    def setFilterCutoffFreq(aiChannObj, value):
        dll.TAiChannel_setFilterCutoffFreq.argtypes = [c_uint64, c_double]
        return dll.TAiChannel_setFilterCutoffFreq(aiChannObj, c_double(value))

    @staticmethod
    def getFilterCutoffFreq1(aiChannObj):
        dll.TAiChannel_getFilterCutoffFreq1.restype = c_double
        dll.TAiChannel_getFilterCutoffFreq1.argtypes = [c_uint64]
        return dll.TAiChannel_getFilterCutoffFreq1(aiChannObj)

    @staticmethod
    def setFilterCutoffFreq1(aiChannObj, value):
        dll.TAiChannel_setFilterCutoffFreq1.argtypes = [c_uint64, c_double]
        return dll.TAiChannel_setFilterCutoffFreq1(aiChannObj, c_double(value))

    # new: Coupling & IEPE & Impedance
    @staticmethod
    def getCouplingType(aiChannObj):
        dll.TAiChannel_getCouplingType.restype = c_int
        dll.TAiChannel_getCouplingType.argtypes = [c_uint64]
        return dll.TAiChannel_getCouplingType(aiChannObj)

    @staticmethod
    def setCouplingType(aiChannObj, couplingTypeValue):
        dll.TAiChannel_setCouplingType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setCouplingType(aiChannObj, couplingTypeValue)

    @staticmethod
    def getIepeType(aiChannObj):
        dll.TAiChannel_getIepeType.restype = c_int
        dll.TAiChannel_getIepeType.argtypes = [c_uint64]
        return dll.TAiChannel_getIepeType(aiChannObj)

    @staticmethod
    def setIepeType(aiChannObj, iepeTypeValue):
        dll.TAiChannel_setIepeType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setIepeType(aiChannObj, iepeTypeValue)

    @staticmethod
    def getImpedanceType(aiChannObj):
        dll.TAiChannel_getImpedanceType.restype = c_int
        dll.TAiChannel_getImpedanceType.argtypes = [c_uint64]
        return dll.TAiChannel_getImpedanceType(aiChannObj)

    @staticmethod
    def setImpedanceType(aiChannObj, impedanceTypeValue):
        dll.TAiChannel_setImpedanceType.argtypes = [c_uint64, c_int32]
        return dll.TAiChannel_setImpedanceType(aiChannObj, impedanceTypeValue)

    # new: Sensor Scaling
    @staticmethod
    def getSensorDescription(aiChannObj, pSize, wDescArr):
        dll.TAiChannel_getSensorDescription.argtypes = [c_uint64, POINTER(c_int32), c_wchar_p]
        return dll.TAiChannel_getSensorDescription(aiChannObj, pSize, wDescArr)

    @staticmethod
    def setSensorDescription(aiChannObj, size, wDescArr):
        dll.TAiChannel_setSensorDescription.argtypes = [c_uint64, c_int32, c_wchar_p]
        return dll.TAiChannel_setSensorDescription(aiChannObj, size, wDescArr)

    # new: scale table
    @staticmethod
    def getScaleTable(aiChannObj, pSize, mapFuncPieceTable):
        dll.TAiChannel_getScaleTable.argtypes = [c_uint64, POINTER(c_int32), POINTER(MapFuncPiece)]
        return dll.TAiChannel_getScaleTable(aiChannObj, pSize, mapFuncPieceTable)

    @staticmethod
    def setScaleTable(aiChannObj, size, mapFuncPieceTable):
        dll.TAiChannel_setScaleTable.argtypes = [c_uint64, c_int32, POINTER(MapFuncPiece)]
        return dll.TAiChannel_setScaleTable(aiChannObj, size, mapFuncPieceTable)


##################################################
#            DIO部分
##################################################
class TDioCtrlBase(object):
    @staticmethod
    def getFeatures(obj):
        dll.TDioCtrlBase_getFeatures.argtypes = [c_uint64]
        dll.TDioCtrlBase_getFeatures.restype = c_uint64
        return dll.TDioCtrlBase_getFeatures(obj)

    @staticmethod
    def getPortCount(obj):
        dll.TDioCtrlBase_getPortCount.restype = c_int32
        dll.TDioCtrlBase_getPortCount.argtypes = [c_uint64]
        return dll.TDioCtrlBase_getPortCount(obj)

    @staticmethod
    def getPorts(obj):
        dll.TDioCtrlBase_getPorts.argtypes = [c_uint64]
        dll.TDioCtrlBase_getPorts.restype = c_uint64
        return dll.TDioCtrlBase_getPorts(obj)


class TInstantDoCtrl(object):
    @staticmethod
    def writeAny(obj, startPort, portCount, dataArray):
        dll.TInstantDoCtrl_WriteAny.argtypes = [c_uint64, c_int32, c_int32, POINTER(c_uint8)]
        return dll.TInstantDoCtrl_WriteAny(obj, startPort, portCount, dataArray)

    @staticmethod
    def readAny(obj, startPort, portCount, dataArray):
        dll.TInstantDoCtrl_ReadAny.argtypes = [c_uint64, c_int32, c_int32, POINTER(c_uint8)]
        return dll.TInstantDoCtrl_ReadAny(obj, startPort, portCount, dataArray)

    @staticmethod
    def writeBit(obj, port, bit, data):
        dll.TInstantDoCtrl_WriteBit.argtypes = [c_uint64, c_int32, c_int32, c_uint8]
        return dll.TInstantDoCtrl_WriteBit(obj, port, bit, data)

    @staticmethod
    def readBit(obj, port, bit, data):
        dll.TInstantDoCtrl_ReadBit.argtypes = [c_uint64, c_int32, c_int32, POINTER(c_uint8)]
        return dll.TInstantDoCtrl_ReadBit(obj, port, bit, byref(data))


class TInstantDiCtrl(object):
    @staticmethod
    def readAny(obj, portStart, portCount, dataArray):
        dll.TInstantDiCtrl_ReadAny.argtypes = [c_uint64, c_int32, c_int32, POINTER(c_uint8)]
        return dll.TInstantDiCtrl_ReadAny(obj, portStart, portCount, dataArray)

    @staticmethod
    def readBit(obj, port, bit, data):
        dll.TInstantDiCtrl_ReadBit.argtypes = [c_uint64, c_int32, c_int32, POINTER(c_uint8)]
        return dll.TInstantDiCtrl_ReadBit(obj, port, bit, data)

    @staticmethod
    def snapStart(obj):
        dll.TInstantDiCtrl_SnapStart.argtypes = [c_uint64]
        return dll.TInstantDiCtrl_SnapStart(obj)

    @staticmethod
    def snapStop(obj):
        dll.TInstantDiCtrl_SnapStop.argtypes = [c_uint64]
        return dll.TInstantDiCtrl_SnapStop(obj)

    @staticmethod
    def getNoiseFilterBlockTime(obj):
        dll.TInstantDiCtrl_getNoiseFilterBlockTime.restype = c_double
        dll.TInstantDiCtrl_getNoiseFilterBlockTime.argtypes = [c_uint64]
        return dll.TInstantDiCtrl_getNoiseFilterBlockTime(obj)

    @staticmethod
    def setNoiseFilterBlockTime(obj, value):
        dll.TInstantDiCtrl_setNoiseFilterBlockTime.argtypes = [c_uint64, c_double]
        return dll.TInstantDiCtrl_setNoiseFilterBlockTime(obj, c_double(value))

    @staticmethod
    def getNoiseFilter(obj):
        dll.TInstantDiCtrl_getNoiseFilter.argtypes = [c_uint64]
        dll.TInstantDiCtrl_getNoiseFilter.restype = c_uint64
        return dll.TInstantDiCtrl_getNoiseFilter(obj)

    @staticmethod
    def getDiintChannels(obj):
        dll.TInstantDiCtrl_getDiintChannels.argtypes = [c_uint64]
        dll.TInstantDiCtrl_getDiintChannels.restype = c_uint64
        return dll.TInstantDiCtrl_getDiintChannels(obj)

    @staticmethod
    def getDiCosintPorts(obj):
        dll.TInstantDiCtrl_getDiCosintPorts.argtypes = [c_uint64]
        dll.TInstantDiCtrl_getDiCosintPorts.restype = c_uint64
        return dll.TInstantDiCtrl_getDiCosintPorts(obj)

    @staticmethod
    def getDiPmintPorts(obj):
        dll.TInstantDiCtrl_getDiPmintPorts.argtypes = [c_uint64]
        dll.TInstantDiCtrl_getDiPmintPorts.restype = c_uint64
        return dll.TInstantDiCtrl_getDiPmintPorts(obj)


class TDioPort(object):
    @staticmethod
    def getPort(obj):
        dll.TDioPort_getPort.restype = c_int32
        dll.TDioPort_getPort.argtypes = [c_uint64]
        return dll.TDioPort_getPort(obj)

    @staticmethod
    def getDirection(obj):
        dll.TDioPort_getDirection.argtypes = [c_uint64]
        return dll.TDioPort_getDirection(obj)

    @staticmethod
    def setDirection(obj, value):
        dll.TDioPort_setDirection.argtypes = [c_uint64, c_int32]
        return dll.TDioPort_setDirection(obj, value)

    @staticmethod
    def getDiInversePort(obj):
        dll.TDioPort_getDiInversePort.restype = c_uint8
        dll.TDioPort_getDiInversePort.argtypes = [c_uint64]
        return dll.TDioPort_getDiInversePort(obj)

    @staticmethod
    def setDiInversePort(obj, value):
        dll.TDioPort_setDiInversePort.argtypes = [c_uint64, c_uint8]
        return dll.TDioPort_setDiInversePort(obj, value)

    @staticmethod
    def getDiOpenState(obj):
        dll.TDioPort_getDiOpenState.restype = c_uint8
        dll.TDioPort_getDiOpenState.argtypes = [c_uint64]
        return dll.TDioPort_getDiOpenState(obj)

    @staticmethod
    def setDiOpenState(obj, value):
        dll.TDioPort_setDiOpenState.argtypes = [c_uint64, c_uint8]
        return dll.TDioPort_setDiOpenState(obj, value)

    @staticmethod
    def getDoPresetValue(obj):
        dll.TDioPort_getDoPresetValue.restype = c_uint8
        dll.TDioPort_getDoPresetValue.argtypes = [c_uint64]
        return dll.TDioPort_getDoPresetValue(obj)

    @staticmethod
    def setDoPresetValue(obj, value):
        dll.TDioPort_setDoPresetValue.argtypes = [c_uint64, c_uint8]
        return dll.TDioPort_setDoPresetValue(obj, value)

    @staticmethod
    def getDoCircuitType(obj):
        dll.TDioPort_getDoCircuitType.argtypes = [c_uint64]
        return dll.TDioPort_getDoCircuitType(obj)

    @staticmethod
    def setDoCircuitType(obj, value):
        dll.TDioPort_setDoCircuitType.argtypes = [c_uint64, c_int32]
        return dll.TDioPort_setDoCircuitType(obj, value)


class TDiintChannel(object):
    @staticmethod
    def getChannel(diIntChanObj):
        dll.TDiintChannel_getChannel.restype = c_int32
        dll.TDiintChannel_getChannel.argtypes = [c_uint64]
        return dll.TDiintChannel_getChannel(diIntChanObj)

    @staticmethod
    def getEnabled(diIntChanObj):
        dll.TDiintChannel_getEnabled.restype = c_int8
        dll.TDiintChannel_getEnabled.argtypes = [c_uint64]
        return dll.TDiintChannel_getEnabled(diIntChanObj)

    @staticmethod
    def setEnabled(diIntChanObj, value):
        dll.TDiintChannel_setEnabled.argtypes = [c_uint64, c_int8]
        return dll.TDiintChannel_setEnabled(diIntChanObj, value)

    @staticmethod
    def getGated(diIntChanObj):
        dll.TDiintChannel_getGated.restype = c_int8
        dll.TDiintChannel_getGated.argtypes = [c_uint64]
        return dll.TDiintChannel_getGated(diIntChanObj)

    @staticmethod
    def setGated(diIntChanObj, value):
        dll.TDiintChannel_setGated.argtypes = [c_uint64, c_int8]
        return dll.TDiintChannel_setGated(diIntChanObj, value)

    @staticmethod
    def getTrigEdge(diIntChanObj):
        dll.TDiintChannel_getTrigEdge.argtypes = [c_uint64]
        return dll.TDiintChannel_getTrigEdge(diIntChanObj)

    @staticmethod
    def setTrigEdge(diIntChanObj, value):
        dll.TDiintChannel_setTrigEdge.argtypes = [c_uint64, c_int32]
        return dll.TDiintChannel_setTrigEdge(diIntChanObj, value)


class TDiCosintPort(object):
    @staticmethod
    def getPort(obj):
        dll.TDiCosintPort_getPort.restype = c_int32
        dll.TDiCosintPort_getPort.argtypes = [c_uint64]
        return dll.TDiCosintPort_getPort(obj)

    @staticmethod
    def getMask(obj):
        dll.TDiCosintPort_getMask.restype = c_byte
        dll.TDiCosintPort_getMask.argtypes = [c_uint64]
        return dll.TDiCosintPort_getMask(obj)

    @staticmethod
    def setMask(obj, value):
        dll.TDiCosintPort_setMask.argtypes = [c_uint64, c_uint8]
        return dll.TDiCosintPort_setMask(obj, value)


class TDiPmintPort(object):
    @staticmethod
    def getPort(obj):
        dll.TDiPmintPort_getPort.restype = c_int32
        dll.TDiPmintPort_getPort.argtypes = [c_uint64]
        return dll.TDiPmintPort_getPort(obj)

    @staticmethod
    def getMask(obj):
        dll.TDiPmintPort_getMask.restype = c_uint8
        dll.TDiPmintPort_getMask.argtypes = [c_uint64]
        return dll.TDiPmintPort_getMask(obj)

    @staticmethod
    def setMask(obj, value):
        dll.TDiPmintPort_setMask.argtypes = [c_uint64, c_uint8]
        return dll.TDiPmintPort_setMask(obj, value)

    @staticmethod
    def getPattern(obj):
        dll.TDiPmintPort_getPattern.restype = c_uint8
        dll.TDiPmintPort_getPattern.argtypes = [c_uint64]
        return dll.TDiPmintPort_getPattern(obj)

    @staticmethod
    def setPattern(obj, value):
        dll.TDiPmintPort_setPattern.argtypes = [c_uint64, c_uint8]
        return dll.TDiPmintPort_setPattern(obj, value)


class TDioFeatures(object):
    @staticmethod
    def getPortProgrammable(obj):
        dll.TDioFeatures_getPortProgrammable.restype = c_int8
        dll.TDioFeatures_getPortProgrammable.argtypes = [c_uint64]
        return dll.TDioFeatures_getPortProgrammable(obj)

    @staticmethod
    def getChannelCountMax(obj):
        dll.TDioFeatures_getChannelCountMax.restype = c_int32
        dll.TDioFeatures_getChannelCountMax.argtypes = [c_uint64]
        return dll.TDioFeatures_getChannelCountMax(obj)

    @staticmethod
    def getPortCount(obj):
        dll.TDioFeatures_getPortCount.restype = c_int32
        dll.TDioFeatures_getPortCount.argtypes = [c_uint64]
        return dll.TDioFeatures_getPortCount(obj)

    @staticmethod
    def getPortsType(obj):
        dll.TDioFeatures_getPortsType.argtypes = [c_uint64]
        dll.TDioFeatures_getPortsType.restype = c_uint64
        return dll.TDioFeatures_getPortsType(obj)

    @staticmethod
    def getDiSupported(obj):
        dll.TDioFeatures_getDiSupported.restype = c_int8
        dll.TDioFeatures_getDiSupported.argtypes = [c_uint64]
        return dll.TDioFeatures_getDiSupported(obj)

    @staticmethod
    def getDoSupported(obj):
        dll.TDioFeatures_getDoSupported.restype = c_int8
        dll.TDioFeatures_getDoSupported.argtypes = [c_uint64]
        return dll.TDioFeatures_getDoSupported(obj)

    @staticmethod
    def getDiDataMask(obj):
        dll.TDioFeatures_getDiDataMask.argtypes = [c_uint64]
        dll.TDioFeatures_getDiDataMask.restype = c_uint64
        return dll.TDioFeatures_getDiDataMask(obj)

    @staticmethod
    def getDiNoiseFilterSupported(obj):
        dll.TDioFeatures_getDiNoiseFilterSupported.restype = c_int8
        dll.TDioFeatures_getDiNoiseFilterSupported.argtypes = [c_uint64]
        return dll.TDioFeatures_getDiNoiseFilterSupported(obj)

    @staticmethod
    def getDiNoiseFilterOfChannels(obj):
        dll.TDioFeatures_getDiNoiseFilterOfChannels.argtypes = [c_uint64]
        dll.TDioFeatures_getDiNoiseFilterOfChannels.restype = c_uint64
        return dll.TDioFeatures_getDiNoiseFilterOfChannels(obj)

    @staticmethod
    def getDiNoiseFilterBlockTimeRange(obj, mathIntervalValue):
        dll.TDioFeatures_getDiNoiseFilterBlockTimeRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TDioFeatures_getDiNoiseFilterBlockTimeRange(obj, mathIntervalValue)

    @staticmethod
    def getDoDataMask(obj):
        dll.TDioFeatures_getDoDataMask.argtypes = [c_uint64]
        return dll.TDioFeatures_getDoDataMask(obj)

    @staticmethod
    def getDoFreezeSignalSources(obj):
        dll.TDioFeatures_getDoFreezeSignalSources.argtypes = [c_uint64]
        return dll.TDioFeatures_getDoFreezeSignalSources(obj)

    @staticmethod
    def getDoReflectWdtFeedIntervalRange(obj, mathInterValValue):
        dll.TDioFeatures_getDoReflectWdtFeedIntervalRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TDioFeatures_getDoReflectWdtFeedIntervalRange(obj, mathInterValValue)

    @staticmethod
    def getDoPresetValueDepository(obj):
        dll.TDioFeatures_getDoPresetValueDepository.argtypes = [c_uint64]
        return dll.TDioFeatures_getDoPresetValueDepository(obj)

    @staticmethod
    def getDoCircuitSelectableTypes(obj):
        dll.TDioFeatures_getDoCircuitSelectableTypes.argtypes = [c_uint64]
        return dll.TDioFeatures_getDoCircuitSelectableTypes(obj)


class TCounterIndexer(object):
    @staticmethod
    def getLength(obj):
        dll.TCounterIndexer_getLength.restype = c_int32
        dll.TCounterIndexer_getLength.argtypes = [c_uint64]
        return dll.TCounterIndexer_getLength(obj)

    @staticmethod
    def getItem(obj, index):
        dll.TCounterIndexer_getItem.argtypes = [c_uint64, c_int32]
        dll.TCounterIndexer_getItem.restype = c_uint64
        return dll.TCounterIndexer_getItem(obj, index)

    @staticmethod
    def dispose(obj):
        dll.TCounterIndexer_Dispose.argtypes = [c_uint64]
        dll.TCounterIndexer_Dispose(obj)


class TCntrFeatures(object):
    @staticmethod
    def getChannelCountMax(obj):
        dll.TCntrFeatures_getChannelCountMax.restype = c_int32
        dll.TCntrFeatures_getChannelCountMax.argtypes = [c_uint64]
        return dll.TCntrFeatures_getChannelCountMax(obj)

    @staticmethod
    def getResolution(obj):
        dll.TCntrFeatures_getResolution.restype = c_int32
        dll.TCntrFeatures_getResolution.argtypes = [c_uint64]
        return dll.TCntrFeatures_getResolution(obj)

    @staticmethod
    def getDataSize(obj):
        dll.TCntrFeatures_getDataSize.restype = c_int32
        dll.TCntrFeatures_getDataSize.argtypes = [c_uint64]
        return dll.TCntrFeatures_getDataSize(obj)

    @staticmethod
    def getCapabilities(obj):
        dll.TCntrFeatures_getCapabilities.argtypes = [c_uint64]
        dll.TCntrFeatures_getCapabilities.restype = c_uint64
        return dll.TCntrFeatures_getCapabilities(obj)

    # noise filter features
    @staticmethod
    def getNoiseFilterSupported(obj):
        dll.TCntrFeatures_getNoiseFilterSupported.restype = c_int8
        dll.TCntrFeatures_getNoiseFilterSupported.argtypes = [c_uint64]
        return dll.TCntrFeatures_getNoiseFilterSupported(obj)

    @staticmethod
    def getNoiseFilterOfChannels(obj):
        dll.TCntrFeatures_getNoiseFilterOfChannels.argtypes = [c_uint64]
        dll.TCntrFeatures_getNoiseFilterOfChannels.restype = c_uint64
        return dll.TCntrFeatures_getNoiseFilterOfChannels(obj)

    @staticmethod
    def getNoiseFilterBlockTimeRange(obj, x):
        dll.TCntrFeatures_getNoiseFilterBlockTimeRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getNoiseFilterBlockTimeRange(obj, byref(x))

    # event counting features
    @staticmethod
    def getEcClockSources(obj):
        dll.TCntrFeatures_getEcClockSources.argtypes = [c_uint64]
        dll.TCntrFeatures_getEcClockSources.restype = c_uint64
        return dll.TCntrFeatures_getEcClockSources(obj)

    @staticmethod
    def getEcClockPolarities(obj):
        dll.TCntrFeatures_getEcClockPolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getEcClockPolarities.restype = c_uint64
        return dll.TCntrFeatures_getEcClockPolarities(obj)

    @staticmethod
    def getEcGatePolarities(obj):
        dll.TCntrFeatures_getEcGatePolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getEcGatePolarities.restype = c_uint64
        return dll.TCntrFeatures_getEcGatePolarities(obj)

    @staticmethod
    def getEcGateControlOfChannels(obj):
        dll.TCntrFeatures_getEcGateControlOfChannels.argtypes = [c_uint64]
        dll.TCntrFeatures_getEcGateControlOfChannels.restype = c_uint64
        return dll.TCntrFeatures_getEcGateControlOfChannels(obj)

    # frequency measurement features
    @staticmethod
    def getFmMethods(obj):
        dll.TCntrFeatures_getFmMethods.argtypes = [c_uint64]
        dll.TCntrFeatures_getFmMethods.restype = c_uint64
        return dll.TCntrFeatures_getFmMethods(obj)

    # one-shot features
    @staticmethod
    def getOsClockSources(obj):
        dll.TCntrFeatures_getOsClockSources.argtypes = [c_uint64]
        dll.TCntrFeatures_getOsClockSources.restype = c_uint64
        return dll.TCntrFeatures_getOsClockSources(obj)

    @staticmethod
    def getOsClockPolarities(obj):
        dll.TCntrFeatures_getOsClockPolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getOsClockPolarities.restype = c_uint64
        return dll.TCntrFeatures_getOsClockPolarities(obj)

    @staticmethod
    def getOsGateSources(obj):
        dll.TCntrFeatures_getOsGateSources.argtypes = [c_uint64]
        dll.TCntrFeatures_getOsGateSources.restype = c_uint64
        return dll.TCntrFeatures_getOsGateSources(obj)

    @staticmethod
    def getOsGatePolarities(obj):
        dll.TCntrFeatures_getOsGatePolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getOsGatePolarities.restype = c_uint64
        return dll.TCntrFeatures_getOsGatePolarities(obj)

    @staticmethod
    def getOsOutSignals(obj):
        dll.TCntrFeatures_getOsOutSignals.argtypes = [c_uint64]
        dll.TCntrFeatures_getOsOutSignals.restype = c_uint64
        return dll.TCntrFeatures_getOsOutSignals(obj)

    @staticmethod
    def getOsDelayCountRange(obj, x):
        dll.TCntrFeatures_getOsDelayCountRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getOsDelayCountRange(obj, byref(x))

    # Timer/pulse features
    @staticmethod
    def getTmrGateControlOfChannels(obj):
        dll.TCntrFeatures_getTmrGateControlOfChannels.argtypes = [c_uint64]
        dll.TCntrFeatures_getTmrGateControlOfChannels.restype = c_uint64
        return dll.TCntrFeatures_getTmrGateControlOfChannels(obj)

    @staticmethod
    def getTmrGatePolarities(obj):
        dll.TCntrFeatures_getTmrGatePolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getTmrGatePolarities.restype = c_uint64
        return dll.TCntrFeatures_getTmrGatePolarities(obj)

    @staticmethod
    def getTmrOutSignals(obj):
        dll.TCntrFeatures_getTmrOutSignals.argtypes = [c_uint64]
        dll.TCntrFeatures_getTmrOutSignals.restype = c_uint64
        return dll.TCntrFeatures_getTmrOutSignals(obj)

    @staticmethod
    def getTmrFrequencyRange(obj, x):
        dll.TCntrFeatures_getTmrFrequencyRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getTmrFrequencyRange(obj, byref(x))

    # pulse width measurement features
    @staticmethod
    def getPiCascadeGroup(obj):
        dll.TCntrFeatures_getPiCascadeGroup.argtypes = [c_uint64]
        dll.TCntrFeatures_getPiCascadeGroup.restype = c_uint64
        return dll.TCntrFeatures_getPiCascadeGroup(obj)

    # pulse width modulation features
    @staticmethod
    def getPoGateControlOfChannels(obj):
        dll.TCntrFeatures_getPoGateControlOfChannels.argtypes = [c_uint64]
        dll.TCntrFeatures_getPoGateControlOfChannels.restype = c_uint64
        return dll.TCntrFeatures_getPoGateControlOfChannels(obj)

    @staticmethod
    def getPoGatePolarities(obj):
        dll.TCntrFeatures_getPoGatePolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getPoGatePolarities.restype = c_uint64
        return dll.TCntrFeatures_getPoGatePolarities(obj)

    @staticmethod
    def getPoOutSignals(obj):
        dll.TCntrFeatures_getPoOutSignals.argtypes = [c_uint64]
        dll.TCntrFeatures_getPoOutSignals.restype = c_uint64
        return dll.TCntrFeatures_getPoOutSignals(obj)

    @staticmethod
    def getPoHiPeriodRange(obj, x):
        dll.TCntrFeatures_getPoHiPeriodRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getPoHiPeriodRange(obj, byref(x))

    @staticmethod
    def getPoLoPeriodRange(obj, x):
        dll.TCntrFeatures_getPoLoPeriodRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getPoLoPeriodRange(obj, byref(x))

    @staticmethod
    def getPoOutCountRange(obj, x):
        dll.TCntrFeatures_getPoOutCountRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getPoOutCountRange(obj, byref(x))

    # Up-down counter features
    @staticmethod
    def getUdCountingTypes(obj):
        dll.TCntrFeatures_getUdCountingTypes.argtypes = [c_uint64]
        dll.TCntrFeatures_getUdCountingTypes.restype = c_uint64
        return dll.TCntrFeatures_getUdCountingTypes(obj)

    @staticmethod
    def getUdInitialValues(obj):
        dll.TCntrFeatures_getUdInitialValues.argtypes = [c_uint64]
        dll.TCntrFeatures_getUdInitialValues.restype = c_uint64
        return dll.TCntrFeatures_getUdInitialValues(obj)

    @staticmethod
    def getUdSnapEventSources(obj):
        dll.TCntrFeatures_getUdSnapEventSources.argtypes = [c_uint64]
        dll.TCntrFeatures_getUdSnapEventSources.restype = c_uint64
        return dll.TCntrFeatures_getUdSnapEventSources(obj)

    # new: measurement timeout range
    @staticmethod
    def getMeasurementTimeoutRange(obj, x):
        dll.TCntrFeatures_getMeasurementTimeoutRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getMeasurementTimeoutRange(obj, byref(x))

    @staticmethod
    def getUdValueResetTimes(obj, x):
        dll.TCntrFeatures_getUdValueResetTimes.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getUdValueResetTimes(obj, byref(x))

    # Counter continue comparing: outputting pulse settings
    @staticmethod
    def getCcpGateControlOfChannels(obj):
        dll.TCntrFeatures_getCcpGateControlOfChannels.argtypes = [c_uint64]
        dll.TCntrFeatures_getCcpGateControlOfChannels.restype = c_uint64
        return dll.TCntrFeatures_getCcpGateControlOfChannels(obj)

    @staticmethod
    def getCcpGatePolarities(obj):
        dll.TCntrFeatures_getCcpGatePolarities.argtypes = [c_uint64]
        dll.TCntrFeatures_getCcpGatePolarities.restype = c_uint64
        return dll.TCntrFeatures_getCcpGatePolarities(obj)

    @staticmethod
    def getCcpOutSignals(obj):
        dll.TCntrFeatures_getCcpOutSignals.argtypes = [c_uint64]
        dll.TCntrFeatures_getCcpOutSignals.restype = c_uint64
        return dll.TCntrFeatures_getCcpOutSignals(obj)

    @staticmethod
    def getCcpHiPeriodRange(obj, x):
        dll.TCntrFeatures_getCcpHiPeriodRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getCcpHiPeriodRange(obj, byref(x))

    @staticmethod
    def getCcpLoPeriodRange(obj, x):
        dll.TCntrFeatures_getCcpLoPeriodRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getCcpLoPeriodRange(obj, byref(x))

    @staticmethod
    def getCcpOutCountRange(obj, x):
        dll.TCntrFeatures_getCcpOutCountRange.argtypes = [c_uint64, POINTER(MathInterval)]
        return dll.TCntrFeatures_getCcpOutCountRange(obj, byref(x))


class TCntrCtrlBase(object):
    @staticmethod
    def getFeatures(obj):
        dll.TCntrCtrlBase_getFeatures.argtypes = [c_uint64]
        dll.TCntrCtrlBase_getFeatures.restype = c_uint64
        return dll.TCntrCtrlBase_getFeatures(obj)

    @staticmethod
    def getChannelStart(obj):
        dll.TCntrCtrlBase_getChannelStart.restype = c_int32
        dll.TCntrCtrlBase_getChannelStart.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getChannelStart(obj)

    @staticmethod
    def setChannelStart(obj, value):
        dll.TCntrCtrlBase_setChannelStart.argtypes = [c_uint64, c_int32]
        return dll.TCntrCtrlBase_setChannelStart(obj, value)

    @staticmethod
    def getChannelCount(obj):
        dll.TCntrCtrlBase_getChannelCount.restype = c_int32
        dll.TCntrCtrlBase_getChannelCount.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getChannelCount(obj)

    @staticmethod
    def setChannelCount(obj, value):
        dll.TCntrCtrlBase_setChannelCount.argtypes = [c_uint64, c_int32]
        return dll.TCntrCtrlBase_setChannelCount(obj, value)

    @staticmethod
    def getEnabled(obj):
        dll.TCntrCtrlBase_getEnabled.restype = c_int8
        dll.TCntrCtrlBase_getEnabled.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getEnabled(obj)

    @staticmethod
    def setEnabled(obj, value):
        dll.TCntrCtrlBase_setEnabled.argtypes = [c_uint64, c_int8]
        return dll.TCntrCtrlBase_setEnabled(obj, value)

    @staticmethod
    def getRunning(obj):
        dll.TCntrCtrlBase_getRunning.restype = c_int8
        dll.TCntrCtrlBase_getRunning.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getRunning(obj)

    @staticmethod
    def getNoiseFilterBlockTime(obj):
        dll.TCntrCtrlBase_getNoiseFilterBlockTime.restype = c_double
        dll.TCntrCtrlBase_getNoiseFilterBlockTime.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getNoiseFilterBlockTime(obj)

    @staticmethod
    def setNoiseFilterBlockTime(obj, value):
        dll.TCntrCtrlBase_setNoiseFilterBlockTime.argtypes = [c_uint64, c_double]
        return dll.TCntrCtrlBase_setNoiseFilterBlockTime(obj, c_double(value))

    @staticmethod
    def getNoiseFilter(obj):
        dll.TCntrCtrlBase_getNoiseFilter.argtypes = [c_uint64]
        dll.TCntrCtrlBase_getNoiseFilter.restype = c_uint64
        return dll.TCntrCtrlBase_getNoiseFilter(obj)

    @staticmethod
    def getMeasurementTimeout(obj):
        dll.TCntrCtrlBase_getMeasurementTimeout.restype = c_double
        dll.TCntrCtrlBase_getMeasurementTimeout.argtypes = [c_uint64]
        return dll.TCntrCtrlBase_getMeasurementTimeout(obj)

    @staticmethod
    def setMeasurementTimeout(obj, value):
        dll.TCntrCtrlBase_setMeasurementTimeout.argtypes = [c_uint64, c_double]
        return dll.TCntrCtrlBase_setMeasurementTimeout(obj, c_double(value))


class TEcChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TEcChannel_getChannel.restype = c_int32
        dll.TEcChannel_getChannel.argtypes = [c_uint64]
        return dll.TEcChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TEcChannel_getNoiseFiltered.restype = c_int8
        dll.TEcChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TEcChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TEcChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TEcChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getClockSource(obj):
        dll.TEcChannel_getClockSource.argtypes = [c_uint64]
        return dll.TEcChannel_getClockSource(obj)

    @staticmethod
    def setClockSource(obj, value):
        dll.TEcChannel_setClockSource.argtypes = [c_uint64, c_int32]
        return dll.TEcChannel_setClockSource(obj, value)

    @staticmethod
    def getClockPolarity(obj):
        dll.TEcChannel_getClockPolarity.argtypes = [c_uint64]
        return dll.TEcChannel_getClockPolarity(obj)

    @staticmethod
    def setClockPolarity(obj, value):
        dll.TEcChannel_setClockPolarity.argtypes = [c_uint64, c_int32]
        return dll.TEcChannel_setClockPolarity(obj, value)

    @staticmethod
    def getGatePolarity(obj):
        dll.TEcChannel_getGatePolarity.argtypes = [c_uint64]
        return dll.TEcChannel_getGatePolarity(obj)

    @staticmethod
    def setGatePolarity(obj, value):
        dll.TEcChannel_setGatePolarity.argtypes = [c_uint64, c_int32]
        return dll.TEcChannel_setGatePolarity(obj, value)

    @staticmethod
    def getGated(obj):
        dll.TEcChannel_getGated.restype = c_int8
        dll.TEcChannel_getGated.argtypes = [c_uint64]
        return dll.TEcChannel_getGated(obj)

    @staticmethod
    def setGated(obj, value):
        dll.TEcChannel_setGated.argtypes = [c_uint64, c_int8]
        return dll.TEcChannel_setGated(obj, value)


class TEventCounterCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TEventCounterCtrl_getChannels.argtypes = [c_uint64]
        dll.TEventCounterCtrl_getChannels.restype = c_uint64
        return dll.TEventCounterCtrl_getChannels(obj)

    @staticmethod
    def Read(obj, count, buffer):
        dll.TEventCounterCtrl_Read.argtypes = [c_uint64, c_int32, POINTER(c_int32)]
        return dll.TEventCounterCtrl_Read(obj, count, buffer)


class TFmChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TFmChannel_getChannel.restype = c_int32
        dll.TFmChannel_getChannel.argtypes = [c_uint64]
        return dll.TFmChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TFmChannel_getNoiseFiltered.restype = c_int8
        dll.TFmChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TFmChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TFmChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TFmChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getFmMethod(obj):
        dll.TFmChannel_getFmMethod.argtypes = [c_uint64]
        return dll.TFmChannel_getFmMethod(obj)

    @staticmethod
    def setFmMethod(obj, value):
        dll.TFmChannel_setFmMethod.argtypes = [c_uint64, c_int32]
        return dll.TFmChannel_setFmMethod(obj, value)

    @staticmethod
    def getCollectionPeriod(obj):
        dll.TFmChannel_getCollectionPeriod.restype = c_double
        dll.TFmChannel_getCollectionPeriod.argtypes = [c_uint64]
        return dll.TFmChannel_getCollectionPeriod(obj)

    @staticmethod
    def setCollectionPeriod(obj, value):
        dll.TFmChannel_setCollectionPeriod.argtypes = [c_uint64, c_double]
        return dll.TFmChannel_setCollectionPeriod(obj, c_double(value))


class TFreqMeterCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TFreqMeterCtrl_getChannels.argtypes = [c_uint64]
        dll.TFreqMeterCtrl_getChannels.restype = c_uint64
        return dll.TFreqMeterCtrl_getChannels(obj)

    @staticmethod
    def Read(obj, count, data):
        dll.TFreqMeterCtrl_Read.argtypes = [c_uint64, c_int32, POINTER(c_double)]
        return dll.TFreqMeterCtrl_Read(obj, count, data)


class TPiChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TPiChannel_getChannel.restype = c_int32
        dll.TPiChannel_getChannel.argtypes = [c_uint64]
        return dll.TPiChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TPiChannel_getNoiseFiltered.restype = c_int8
        dll.TPiChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TPiChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TPiChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TPiChannel_setNoiseFiltered(obj, value)


class TPwMeterCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TPwMeterCtrl_getChannels.argtypes = [c_uint64]
        dll.TPwMeterCtrl_getChannels.restype = c_uint64
        return dll.TPwMeterCtrl_getChannels(obj)

    @staticmethod
    def Read(obj, count, buffer):
        dll.TPwMeterCtrl_Read.argtypes = [c_uint64, c_int32, POINTER(PulseWidth)]
        return dll.TPwMeterCtrl_Read(obj, count, buffer)


class TPoChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TPoChannel_getChannel.restype = c_int32
        dll.TPoChannel_getChannel.argtypes = [c_uint64]
        return dll.TPoChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TPoChannel_getNoiseFiltered.restype = c_int8
        dll.TPoChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TPoChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TPoChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TPoChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getPulseWidth(obj, pulseWidth):
        dll.TPoChannel_getPulseWidth.argtypes = [c_uint64, POINTER(PulseWidth)]
        return dll.TPoChannel_getPulseWidth(obj, byref(pulseWidth))

    @staticmethod
    def setPulseWidth(obj, pulseWidthValue):
        dll.TPoChannel_setPulseWidth.argtypes = [c_uint64, POINTER(PulseWidth)]
        return dll.TPoChannel_setPulseWidth(obj, byref(pulseWidthValue))

    @staticmethod
    def getGatePolarity(obj):
        dll.TPoChannel_getGatePolarity.argtypes = [c_uint64]
        return dll.TPoChannel_getGatePolarity(obj)

    @staticmethod
    def setGatePolarity(obj, signPolarValue):
        dll.TPoChannel_setGatePolarity.argtypes = [c_uint64, c_int32]
        return dll.TPoChannel_setGatePolarity(obj, signPolarValue)

    @staticmethod
    def getGated(obj):
        dll.TPoChannel_getGated.restupe = c_int8
        dll.TPoChannel_getGated.argtypes = [c_uint64]
        return dll.TPoChannel_getGated(obj)

    @staticmethod
    def setGated(obj, value):
        dll.TPoChannel_setGated.argtypes = [c_uint64]
        return dll.TPoChannel_setGated(obj, value)

    @staticmethod
    def getOutSignal(obj):
        dll.TPoChannel_getOutSignal.argtypes = [c_uint64]
        return dll.TPoChannel_getOutSignal(obj)

    @staticmethod
    def setOutSignal(obj, outSignTypeValue):
        dll.TPoChannel_setOutSignal.argtypes = [c_uint64, c_int32]
        return dll.TPoChannel_setOutSignal(obj, outSignTypeValue)

    @staticmethod
    def getOutCount(obj):
        dll.TPoChannel_getOutCount.restype = c_int32
        dll.TPoChannel_getOutCount.argtypes = [c_uint64]
        return dll.TPoChannel_getOutCount(obj)

    @staticmethod
    def setOutCount(obj, value):
        dll.TPoChannel_setOutCount.argtypes = [c_uint64, c_int32]
        return dll.TPoChannel_setOutCount(obj, value)


class TPwModulatorCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TPwModulatorCtrl_getChannels.argtypes = [c_uint64]
        dll.TPwModulatorCtrl_getChannels.restype = c_uint64
        return dll.TPwModulatorCtrl_getChannels(obj)

class TOsChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TOsChannel_getChannel.restype = c_int32
        dll.TOsChannel_getChannel.argtypes = [c_uint64]
        return dll.TOsChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TOsChannel_getNoiseFiltered.restype = c_int8
        dll.TOsChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TOsChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TOsChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TOsChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getDelayCount(obj):
        dll.TOsChannel_getDelayCount.restype = c_int32
        dll.TOsChannel_getDelayCount.argtypes = [c_uint64]
        return dll.TOsChannel_getDelayCount(obj)

    @staticmethod
    def setDelayCount(obj, value):
        dll.TOsChannel_setDelayCount.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setDelayCount(obj, value)

    @staticmethod
    def getClockSource(obj):
        dll.TOsChannel_getClockSource.argtypes = [c_uint64]
        return dll.TOsChannel_getClockSource(obj)

    @staticmethod
    def setClockSource(obj, value):
        dll.TOsChannel_setClockSource.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setClockSource(obj, value)

    @staticmethod
    def getClockPolarity(obj):
        dll.TOsChannel_getClockPolarity.argtypes = [c_uint64]
        return dll.TOsChannel_getClockPolarity(obj)

    @staticmethod
    def setClockPolarity(obj, value):
        dll.TOsChannel_setClockPolarity.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setClockPolarity(obj, value)

    @staticmethod
    def getGateSource(obj):
        dll.TOsChannel_getGateSource.argtypes = [c_uint64]
        return dll.TOsChannel_getGateSource(obj)

    @staticmethod
    def setGateSource(obj, value):
        dll.TOsChannel_setGateSource.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setGateSource(obj, value)

    @staticmethod
    def getGatePolarity(obj):
        dll.TOsChannel_getGatePolarity.argtypes = [c_uint64]
        return dll.TOsChannel_getGatePolarity(obj)

    @staticmethod
    def setGatePolarity(obj, value):
        dll.TOsChannel_setGatePolarity.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setGatePolarity(obj, value)

    @staticmethod
    def getOutSignal(obj):
        dll.TOsChannel_getOutSignal.argtypes = [c_uint64]
        return dll.TOsChannel_getOutSignal(obj)

    @staticmethod
    def setOutSignal(obj, value):
        dll.TOsChannel_setOutSignal.argtypes = [c_uint64, c_int32]
        return dll.TOsChannel_setOutSignal(obj, value)


class TOneShotCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TOneShotCtrl_getChannels.argtypes = [c_uint64]
        dll.TOneShotCtrl_getChannels.restype = c_uint64
        return dll.TOneShotCtrl_getChannels(obj)


class TTmrChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TTmrChannel_getChannel.restype = c_int32
        dll.TTmrChannel_getChannel.argtypes = [c_uint64]
        return dll.TTmrChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TTmrChannel_getNoiseFiltered.restype = c_int8
        dll.TTmrChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TTmrChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TTmrChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TTmrChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getFrequency(obj):
        dll.TTmrChannel_getFrequency.restype = c_double
        dll.TTmrChannel_getFrequency.argtypes = [c_uint64]
        return dll.TTmrChannel_getFrequency(obj)

    @staticmethod
    def setFrequency(obj, value):
        dll.TTmrChannel_setFrequency.argtypes = [c_uint64, c_double]
        return dll.TTmrChannel_setFrequency(obj, c_double(value))

    @staticmethod
    def getGatePolarity(obj):
        dll.TTmrChannel_getGatePolarity.argtypes = [c_uint64]
        return dll.TTmrChannel_getGatePolarity(obj)

    @staticmethod
    def setGatePolarity(obj, value):
        dll.TTmrChannel_setGatePolarity.argtypes = [c_uint64, c_int32]
        return dll.TTmrChannel_setGatePolarity(obj, value)

    @staticmethod
    def getGated(obj):
        dll.TTmrChannel_getGated.restype = c_int8
        dll.TTmrChannel_getGated.argtypes = [c_uint64]
        return dll.TTmrChannel_getGated(obj)

    @staticmethod
    def setGated(obj, value):
        dll.TTmrChannel_setGated.argtypes = [c_uint64, c_int8]
        return dll.TTmrChannel_setGated(obj, value)

    @staticmethod
    def getOutSignal(obj):
        dll.TTmrChannel_getOutSignal.argtypes = [c_uint64]
        return dll.TTmrChannel_getOutSignal(obj)

    @staticmethod
    def setOutSignal(obj, value):
        dll.TTmrChannel_setOutSignal.argtypes = [c_uint64, c_int32]
        return dll.TTmrChannel_setOutSignal(obj, value)


class TTimerPulseCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TTimerPulseCtrl_getChannels.argtypes = [c_uint64]
        dll.TTimerPulseCtrl_getChannels.restype = c_uint64
        return dll.TTimerPulseCtrl_getChannels(obj)


class TUdChannel(object):
    @staticmethod
    def getChannel(obj):
        dll.TUdChannel_getChannel.restype = c_int32
        dll.TUdChannel_getChannel.argtypes = [c_uint64]
        return dll.TUdChannel_getChannel(obj)

    @staticmethod
    def getNoiseFiltered(obj):
        dll.TUdChannel_getNoiseFiltered.restype = c_int8
        dll.TUdChannel_getNoiseFiltered.argtypes = [c_uint64]
        return dll.TUdChannel_getNoiseFiltered(obj)

    @staticmethod
    def setNoiseFiltered(obj, value):
        dll.TUdChannel_setNoiseFiltered.argtypes = [c_uint64, c_int8]
        return dll.TUdChannel_setNoiseFiltered(obj, value)

    @staticmethod
    def getCountingType(obj):
        dll.TUdChannel_getCountingType.argtypes = [c_uint64]
        return dll.TUdChannel_getCountingType(obj)

    @staticmethod
    def setCountingType(obj, value):
        dll.TUdChannel_setCountingType.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setCountingType(obj, value)

    @staticmethod
    def getInitialValue(obj):
        dll.TUdChannel_getInitialValue.restype = c_int32
        dll.TUdChannel_getInitialValue.argtypes = [c_uint64]
        return dll.TUdChannel_getInitialValue(obj)

    @staticmethod
    def setInitialValue(obj, value):
        dll.TUdChannel_setInitialValue.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setInitialValue(obj, value)

    @staticmethod
    def getResetTimesByIndex(obj):
        dll.TUdChannel_getResetTimesByIndex.restype = c_int32
        dll.TUdChannel_getResetTimesByIndex.argtypes = [c_uint64]
        return dll.TUdChannel_getResetTimesByIndex(obj)

    @staticmethod
    def setResetTimesByIndex(obj, value):
        dll.TUdChannel_setResetTimesByIndex.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setResetTimesByIndex(obj, value)

    @staticmethod
    def getPulseWidth(obj, width):
        dll.TUdChannel_getPulseWidth.argtypes = [c_uint64, POINTER(PulseWidth)]
        return dll.TUdChannel_getPulseWidth(obj, byref(width))

    @staticmethod
    def setPulseWidth(obj, width):
        dll.TUdChannel_setPulseWidth.restype = c_uint32
        dll.TUdChannel_setPulseWidth.argtypes = [c_uint64, POINTER(PulseWidth)]
        return dll.TUdChannel_setPulseWidth(obj, byref(width))

    @staticmethod
    def getGated(obj):
        dll.TUdChannel_getGated.restype = c_int8
        dll.TUdChannel_getGated.argtypes = [c_uint64]
        return dll.TUdChannel_getGated(obj)

    @staticmethod
    def setGated(obj, value):
        dll.TUdChannel_setGated.argtypes = [c_uint64, c_int8]
        return dll.TUdChannel_setGated(obj, value)

    @staticmethod
    def getGatePolarity(obj):
        dll.TUdChannel_getGatePolarity.argtypes = [c_uint64]
        return dll.TUdChannel_getGatePolarity(obj)

    @staticmethod
    def setGatePolarity(obj, value):
        dll.TUdChannel_setGatePolarity.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setGatePolarity(obj, value)

    @staticmethod
    def getOutSignal(obj):
        dll.TUdChannel_getOutSignal.argtypes = [c_uint64]
        return dll.TUdChannel_getOutSignal(obj)

    @staticmethod
    def setOutSignal(obj, value):
        dll.TUdChannel_setOutSignal.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setOutSignal(obj, value)

    @staticmethod
    def getOutCount(obj):
        dll.TUdChannel_getOutCount.restype = c_int32
        dll.TUdChannel_getOutCount.argtypes = [c_uint64]
        return dll.TUdChannel_getOutCount(obj)

    @staticmethod
    def setOutCount(obj, value):
        dll.TUdChannel_setOutCount.argtypes = [c_uint64, c_int32]
        return dll.TUdChannel_setOutCount(obj, value)


class TUdCounterCtrl(object):
    @staticmethod
    def getChannels(obj):
        dll.TUdCounterCtrl_getChannels.argtypes = [c_uint64]
        dll.TUdCounterCtrl_getChannels.restype = c_uint64
        return dll.TUdCounterCtrl_getChannels(obj)

    @staticmethod
    def Read(obj, count, buffer):
        dll.TUdCounterCtrl_Read.argtypes = [c_uint64, c_int32, POINTER(c_int32)]
        return dll.TUdCounterCtrl_Read(obj, count, buffer)

    @staticmethod
    def ValueReset(obj):
        dll.TUdCounterCtrl_ValueReset.argtypes = [c_uint64]
        return dll.TUdCounterCtrl_ValueReset(obj)






