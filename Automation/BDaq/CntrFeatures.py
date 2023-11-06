#!/usr/bin/python
# -*- coding:utf-8 -*-

from Automation.BDaq.BDaqApi import TCntrFeatures, TArray
from Automation.BDaq.CounterCapabilityIndexer import CounterCapabilityIndexer
from Automation.BDaq.CounterClockSourceIndexer import CounterClockSourceIndexer
from Automation.BDaq.CounterGateSourceIndexer import CounterGateSourceIndexer
from Automation.BDaq import MathInterval


class CntrFeatures(object):
    def __init__(self, native_cntr_features):
        self._native_cntr_features = native_cntr_features

    # Channel features
    @property
    def channelCountMax(self):
        return TCntrFeatures.getChannelCountMax(self._native_cntr_features)

    @property
    def resolution(self):
        return TCntrFeatures.getResolution(self._native_cntr_features)

    @property
    def dataSize(self):
        return TCntrFeatures.getDataSize(self._native_cntr_features)

    @property
    def capabilities(self):
        return CounterCapabilityIndexer(TCntrFeatures.getCapabilities(self._native_cntr_features))

    # noise filter features
    @property
    def noiseFilterSupported(self):
        value = TCntrFeatures.getNoiseFilterSupported(self._native_cntr_features)
        return True if value else False

    @property
    def noiseFilterOfChannels(self):
        nativeArray = TCntrFeatures.getNoiseFilterOfChannels(self._native_cntr_features)
        return TArray.ToByte(nativeArray, True)

    @property
    def noiseFilterBlockTimeRange(self):
        x = MathInterval()
        TCntrFeatures.getNoiseFilterBlockTimeRange(self._native_cntr_features, x)
        return x

    # event counting features
    @property
    def ecClockSources(self):
        clockObj = TCntrFeatures.getEcClockSources(self._native_cntr_features)
        return CounterClockSourceIndexer(clockObj)

    @property
    def ecClockPolarities(self):
        nativeArray = TCntrFeatures.getEcClockPolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def ecGatePolarities(self):
        nativeArray = TCntrFeatures.getEcGatePolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def ecGateControlOfChannels(self):
        nativeArray = TCntrFeatures.getEcGateControlOfChannels(self._native_cntr_features)
        return TArray.ToInt32(nativeArray, True)

    # frequency measurement features
    @property
    def fmMethods(self):
        nativeArray = TCntrFeatures.getFmMethods(self._native_cntr_features)
        return TArray.ToFreqMeasureMethod(nativeArray, True)

    # one-shot features
    @property
    def osClockSources(self):
        clockObj = TCntrFeatures.getOsClockSources(self._native_cntr_features)
        return CounterClockSourceIndexer(clockObj)

    @property
    def osClockPolarities(self):
        nativeArray = TCntrFeatures.getOsClockPolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def osGateSources(self):
        clockObj = TCntrFeatures.getOsGateSources(self._native_cntr_features)
        return CounterGateSourceIndexer(clockObj)

    @property
    def osGatePolarities(self):
        nativeArray = TCntrFeatures.getOsGatePolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def osOutSignals(self):
        nativeArray = TCntrFeatures.getOsOutSignals(self._native_cntr_features)
        return TArray.ToOutSignalType(nativeArray, True)

    @property
    def osDelayCountRange(self):
        x = MathInterval()
        TCntrFeatures.getOsDelayCountRange(self._native_cntr_features, x)
        return x

    # Timer/pulse features
    @property
    def tmrGateControlOfChannels(self):
        nativeArray = TCntrFeatures.getTmrGateControlOfChannels(self._native_cntr_features)
        return TArray.ToInt32(nativeArray, True)

    @property
    def tmrGatePolarities(self):
        nativeArray = TCntrFeatures.getTmrGatePolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def tmrOutSignals(self):
        nativeArray = TCntrFeatures.getTmrOutSignals(self._native_cntr_features)
        return TArray.ToOutSignalType(nativeArray, True)

    @property
    def tmrFrequencyRange(self):
        x = MathInterval()
        TCntrFeatures.getTmrFrequencyRange(self._native_cntr_features, x)
        return x

    # pulse width measurement features
    @property
    def piCascadeGroup(self):
        nativeArray = TCntrFeatures.getPiCascadeGroup(self._native_cntr_features)
        return TArray.ToCounterCascadeGroup(nativeArray, True)

    # pulse width modulation features
    @property
    def poGateControlOfChannels(self):
        nativeArray = TCntrFeatures.getPoGateControlOfChannels(self._native_cntr_features)
        return TArray.ToInt32(nativeArray, True)

    @property
    def poGatePolarities(self):
        nativeArray = TCntrFeatures.getPoGatePolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def poOutSignals(self):
        nativeArray = TCntrFeatures.getPoOutSignals(self._native_cntr_features)
        return TArray.ToOutSignalType(nativeArray, True)

    @property
    def poHiPeriodRange(self):
        x = MathInterval()
        TCntrFeatures.getPoHiPeriodRange(self._native_cntr_features, x)
        return x

    @property
    def poLoPeriodRange(self):
        x = MathInterval()
        TCntrFeatures.getPoLoPeriodRange(self._native_cntr_features, x)
        return x

    @property
    def poOutCountRange(self):
        x = MathInterval()
        TCntrFeatures.getPoOutCountRange(self._native_cntr_features, x)
        return x

    # Up-down counter features
    @property
    def udCountingTypes(self):
        nativeArray = TCntrFeatures.getUdCountingTypes(self._native_cntr_features)
        return TArray.ToCountingType(nativeArray, True)

    @property
    def udInitialValues(self):
        nativeArray = TCntrFeatures.getUdInitialValues(self._native_cntr_features)
        return TArray.ToInt32(nativeArray, True)

    @property
    def udSnapEventSources(self):
        nativeArray = TCntrFeatures.getUdSnapEventSources(self._native_cntr_features)
        return TArray.ToEventId(nativeArray, True)

    # new: measurement timeout range
    @property
    def measurementTimeoutRange(self):
        x = MathInterval()
        TCntrFeatures.getMeasurementTimeoutRange(self._native_cntr_features, x)
        return x

    @property
    def udValueResetTimes(self):
        x = MathInterval()
        TCntrFeatures.getUdValueResetTimes(self._native_cntr_features, x)
        return x

    # Counter continue comparing: outputting pulse settings
    @property
    def ccpGateControlOfChannels(self):
        nativeArray = TCntrFeatures.getCcpGateControlOfChannels(self._native_cntr_features)
        return TArray.ToInt32(nativeArray, True)

    @property
    def ccpGatePolarities(self):
        nativeArray = TCntrFeatures.getCcpGatePolarities(self._native_cntr_features)
        return TArray.ToSignalPolarity(nativeArray, True)

    @property
    def ccpOutSignals(self):
        nativeArray = TCntrFeatures.getCcpOutSignals(self._native_cntr_features)
        return TArray.ToOutSignalType(nativeArray, True)

    @property
    def ccpHiPeriodRange(self):
        x = MathInterval()
        TCntrFeatures.getCcpHiPeriodRange(self._native_cntr_features, x)
        return x

    @property
    def ccpLoPeriodRange(self):
        x = MathInterval()
        TCntrFeatures.getCcpLoPeriodRange(self._native_cntr_features, x)
        return x

    @property
    def ccpOutCountRange(self):
        x = MathInterval()
        TCntrFeatures.getCcpOutCountRange(self._native_cntr_features, x)
        return x
