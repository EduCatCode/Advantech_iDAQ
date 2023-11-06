#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq import ErrorCode
from Automation.BDaq.BDaqApi import TDaqCtrlBase, TArray, BioFailed
from Automation.BDaq import DeviceInformation, ControlState
from Automation.BDaq.DeviceCtrl import DeviceCtrl
from Automation.BDaq import Utils
from Automation.BDaq import ErrorCode


class DaqCtrlBase(object):
    def __init__(self, scenario, devInfo):
        self._deviceCtrl = None
        self._obj = self.create(scenario)
        
        if devInfo is not None:
            self.selectedDevice = devInfo

    @property
    def initialized(self):
        return self.state != ControlState.Uninited

    def cleanup(self):
        TDaqCtrlBase.cleanup(self._obj)

    def dispose(self):
        TDaqCtrlBase.dispose(self._obj)

    @property
    def selectedDevice(self):
        devInfo = DeviceInformation()
        TDaqCtrlBase.getSelectedDevice(self._obj, devInfo)
        return devInfo

    @selectedDevice.setter
    def selectedDevice(self, devInfo):
        if not isinstance(devInfo, (DeviceInformation, int, str)):
            raise TypeError('The parameter value is not supported.')
        
        if isinstance(devInfo, str):
            ret = ErrorCode.lookup(TDaqCtrlBase.setSelectedDevice(self._obj, DeviceInformation(Description=devInfo)))
        elif isinstance(devInfo, int):
            ret = ErrorCode.lookup(TDaqCtrlBase.setSelectedDevice(self._obj, DeviceInformation(Description=u'', DeviceNumber=devInfo)))
        else:
            ret = ErrorCode.lookup(TDaqCtrlBase.setSelectedDevice(self._obj, devInfo))
        
        if BioFailed(ret):
            raise ValueError('The device is not opened, and the error code is 0x%X' % (ret.value))

    @property
    def state(self):
        ret = TDaqCtrlBase.getState(self._obj)
        return Utils.toControlState(ret)

    @property
    def device(self):
        if self._deviceCtrl is None:
            self._deviceCtrl = DeviceCtrl(TDaqCtrlBase.getDevice(self._obj))
        return self._deviceCtrl

    @property
    def supportedDevices(self):
        nativeArray = TDaqCtrlBase.getSupportedDevices(self._obj)
        deviceTreeNodeArr = TArray.toDeviceTreeNode(nativeArray)
        return deviceTreeNodeArr

    @property
    def supportedModes(self):
        nativeArray = TDaqCtrlBase.getSupportedModes(self._obj)
        accessModeList = TArray.toAccessMode(nativeArray)
        return accessModeList

    @property
    def module(self):
        return TDaqCtrlBase.getModule(self._obj)

    def create(self, scenario):
        return TDaqCtrlBase.Create(scenario.value)

    def __set_loadProfile(self, profile):
        ret = ErrorCode.lookup(TDaqCtrlBase.LoadProfile(self._obj, profile))
        if BioFailed(ret):
            raise ValueError('set loadProfile is failed, the error code is 0x%X' % (ret.value))
    
    loadProfile = property(None, __set_loadProfile)
