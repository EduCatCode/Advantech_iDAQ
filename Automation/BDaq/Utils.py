#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq import *


def CreateArray(DataType, DataNum):
    dataArray = (DataType * DataNum)()
    return dataArray

def toAccessMode(value):
    value = int(value)
    for x in AccessMode:
        if x.value == value:
            return x
    return AccessMode.ModeRead

def toControlState(value):
    value = int(value)
    for x in ControlState:
        if x.value == value:
            return x
    return ControlState.Uninited

def toProductId(value):
    value = int(value)
    for x in ProductId:
        if x.value == value:
            return x
    return ProductId.BD_UNKNOWN

def toTerminalBoard(value):
    value = int(value)
    for x in TerminalBoard:
        if x.value == value:
            return x

    return TerminalBoard.WiringBoard

def toDepository(value):
    value = int(value)
    for x in Depository:
        if x.value == value:
            return x
    return Depository.DepositoryNone

def toAiChannelType(value):
    value = int(value)
    for x in AiChannelType:
        if x.value == value:
            return x
    return AiChannelType.AllSingleEnded

def toAiSignalType(value):
    value = int(value)
    for x in AiSignalType:
        if x.value == value:
            return x
    return AiSignalType.PseudoDifferential

def toValueRange(value):
    value = int(value)
    for x in ValueRange:
        if x.value == value:
            return x
    return ValueRange.V_OMIT

def toSamplingMethod(value):
    value = int(value)
    return SamplingMethod.EqualTimeSwitch if value == SamplingMethod.EqualTimeSwitch.value else SamplingMethod.Simultaneous

def toFilterType(value):
    value = int(value)
    for x in FilterType:
        if x.value == value:
            return x
    return FilterType.FilterNone

def toBurnoutRetType(value):
    value = int(value)
    for x in BurnoutRetType:
        if x.value == value:
            return x
    return BurnoutRetType.Current

def toSignalDrop(value):
    value = int(value)

    for x in SignalDrop:
        if x.value == value:
            return x
    return SignalDrop.SignalNone

def toSignalPolarity(value):
    value = int(value)

    for x in SignalPolarity:
        if x.value == value:
            return x
    return SignalPolarity.Negative

def toTriggerAction(value):
    value = int(value)

    for x in TriggerAction:
        if x.value == value:
            return x
    return TriggerAction.ActionNone

def toActiveSignal(value):
    value = int(value)

    for x in ActiveSignal:
        if x.value == value:
            return x
    return ActiveSignal.ActiveNone

def toDioPortDir(value):
    value = int(value)
    for x in DioPortDir:
        if x.value == value:
            return x
    return DioPortDir.Input

def toDoCircuitType(value):
    value = int(value)

    for x in DoCircuitType:
        if x.value == value:
            return x
    return DoCircuitType.TTL

def toEventId(value):
    value = int(value)

    for x in EventId:
        if x.value == value:
            return x
    return EventId.EvtPropertyChanged

def toCounterCapability(value):
    value = int(value)

    for x in CounterCapability:
        if x.value == value:
            return x
    return CounterCapability.Primary

def toCounterCascadeGroup(value):
    value = int(value)

    for x in CounterCascadeGroup:
        if x.value == value:
            return x
    return CounterCascadeGroup.GroupNone

def toFreqMeasureMethod(value):
    value = int(value)

    for x in FreqMeasureMethod:
        if x.value == value:
            return x
    return FreqMeasureMethod.AutoAdaptive

def toCountingType(value):
    value = int(value)
    for x in CountingType:
        if x.value == value:
            return x
    return CountingType.CountingNone

def toOutSignaleType(value):
    value = int(value)

    for x in OutSignalType:
        if x.value == value:
            return x
    return OutSignalType.SignalOutNone

def toCouplingType(value):
    value = int(value)

    for x in CouplingType:
        if x.value == value:
            return x

    return CouplingType.ACCoupling

def toIepeType(value):
    value = int(value)

    for x in IepeType:
        if x.value == value:
            return x
    return IepeType.IEPENone

def toImpedanceType(value):
    value = int(value)

    for x in ImpedanceType:
        if x.value == value:
            return x
    return ImpedanceType.Ipd1Momh
