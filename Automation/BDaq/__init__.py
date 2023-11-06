import sys
if sys.version_info[:3] < (3,4):
    sys.path.append('../3rd_party')
from enum import Enum, IntEnum
from ctypes import Structure, c_int32, c_double, c_int64, c_wchar
from ctypes import c_uint8


DAQ_NAVI_VER = 0x400

MAX_DEVICE_DESC_LEN = 64
MAX_VRG_DESC_LEN = 256
MAX_SIG_DROP_DESC_LEN = 256

MAX_AI_CH_COUNT = 128
MAX_AO_CH_COUNT = 128
MAX_DIO_PORT_COUNT = 32
MAX_CNTR_CH_COUNT = 8
MAX_TRIG_COUNT = 4
MAX_DIO_TRIG_COUNT = 2


class TerminalBoard(IntEnum):
    WiringBoard = 0
    PCLD8710 = 1
    PCLD789 = 2
    PCLD8115 = 3


class ModuleType(IntEnum):
    DaqGroup = 1
    DaqDevice = 2
    DaqAi = 3
    DaqAo = 4
    DaqDio = 5
    DaqCounter = 6
    DaqCali = 7
    DaqAny = -1


class AccessMode(IntEnum):
    ModeRead = 0
    ModeWrite = 1
    ModeWriteWithReset = 2
    ModeWriteShared = 3


class Depository(IntEnum):
    DepositoryNone = 0
    DepositoryOnSystem = 1
    DepositoryOnDevice = 2


class MathIntervalType(IntEnum):
    # Right boundary definition, define the maximum value state, use the bit 0,1
    RightOpenSet = 0x0,  # No maximum value limitation.
    RightClosedBoundary = 0x1,  # The maximum value is included.
    RightOpenBoundary = 0x2,  # The maximum value is not included.

    # Left boundary definition, define the minimum value state, used the bit 2, 3
    LeftOpenSet = 0x0,  # No minimum value limitation.
    LeftClosedBoundary = 0x4,  # The minimum value is included.
    LeftOpenBoundary = 0x8,  # The minimum value is not included

    # The signality expression
    Boundless = 0x0,  # Boundless set. (LeftOpenSet | RightOpenSet)

    # The combination notation
    LOSROS = 0x0,  # (LeftOpenSet | RightOpenSet), algebra notation: (un-limit, max)
    LOSRCB = 0x1,  # (LeftOpenSet | RightClosedBoundary), algebra notation: (un-limit, max ]
    LOSROB = 0x2,  # (LeftOpenSet | RightOpenBoundary), algebra notation: (un-limit, max)

    LCBROS = 0x4,  # (LeftClosedBoundary | RightOpenSet), algebra notation: [min, un-limit)
    LCBRCB = 0x5,  # (LeftClosedBoundary | RightClosedBoundary), algebra notation: [ min, right ]
    LCBROB = 0x6,  # (LeftClosedBoundary | RightOpenBoundary), algebra notation: [ min, right)

    LOBROS = 0x8,  # (LeftOpenBoundary | RightOpenSet), algebra notation: (min, un-limit)
    LOBRCB = 0x9,  # (LeftOpenBoundary | RightClosedBoundary), algebra notation: (min, right ]
    LOBROB = 0xA,  # (LeftOpenBoundary | RightOpenBoundary), algebra notation: (min, right)


class AiChannelType(IntEnum):
    AllSingleEnded = 0
    AllDifferential = 1
    AllSeDiffAdj = 2
    MixedSeDiffAdj = 3


class AiSignalType(IntEnum):
    SingleEnded = 0
    Differential = 1
    PseudoDifferential = 2


class CouplingType(IntEnum):
    DCCoupling = 0
    ACCoupling = 1


class ImpedanceType(IntEnum):
    Ipd1Momh = 0
    Ipd50omh = 1


class IepeType(IntEnum):
    IEPENone = 0
    IEPE4mA = 1
    IEPE10mA = 2
    IEPE2mA = 3


class FilterType(IntEnum):
    FilterNone = 0
    LowPass = 1
    HighPass = 2
    BandPass = 3
    BandStop = 4


class DioPortType(IntEnum):
    PortDi = 0  # the port number references to a DI port
    PortDo = 1  # the port number references to a DO port
    PortDio = 2  # the port number references to a DI port and a DO port
    Port8255A = 3  # the port number references to a PPI port A mode DIO port.
    Port8255C = 4  # the port number references to a PPI port C mode DIO port.
    PortIndvdlDio = 5  # the port number references to a port whose each channel can be configured as in or out.


class DioPortDir(IntEnum):
    Input = 0x00
    LoutHin = 0x0F
    LinHout = 0xF0
    Output = 0xFF


class DoCircuitType(IntEnum):
    TTL = 0
    Sink = 1
    Source = 2
    Relay = 3


class SamplingMethod(IntEnum):
    EqualTimeSwitch = 0
    Simultaneous = 1


class TemperatureDegree(IntEnum):
    Celsius = 0
    Fahrenheit = 1
    Rankine = 2
    Kelvin = 3


class BurnoutRetType(IntEnum):
    Current = 0
    ParticularValue = 1
    UpLimit = 2
    LowLimit = 3
    LastCorrectValue = 4


class ValueUnit(IntEnum):
    Kilovolt = 0  # KV
    Volt = 1  # V
    Millivolt = 2  # mV
    Microvolt = 3  # uV
    Kiloampere = 4  # KA
    Ampere = 5  # A
    Milliampere = 6  # mA
    Microampere = 7  # uA
    CelsiusUnit = 8  # Celsius


class ValueRange(IntEnum):
    V_OMIT = -1  # Unknown when get, ignored when set
    V_Neg15To15 = 0  # +/- 15 V
    V_Neg10To10 = 1  # +/- 10 V
    V_Neg5To5 = 2  # +/- 5 V
    V_Neg2pt5To2pt5 = 3  # +/- 2.5 V
    V_Neg1pt25To1pt25 = 4  # +/- 1.25 V
    V_Neg1To1 = 5  # +/- 1 V

    V_0To15 = 6  # 0~15 V
    V_0To10 = 7  # 0~10 V
    V_0To5 = 8  # 0~5 V
    V_0To2pt5 = 9  # 0~2.5 V
    V_0To1pt25 = 10  # 0~1.25 V
    V_0To1 = 11  # 0~1 V

    mV_Neg625To625 = 12  # +/- 625mV
    mV_Neg500To500 = 13  # +/- 500 mV
    mV_Neg312pt5To312pt5 = 14  # +/- 312.5 mV
    mV_Neg200To200 = 15  # +/- 200 mV
    mV_Neg150To150 = 16  # +/- 150 mV
    mV_Neg100To100 = 17  # +/- 100 mV
    mV_Neg50To50 = 18  # +/- 50 mV
    mV_Neg30To30 = 19  # +/- 30 mV
    mV_Neg20To20 = 20  # +/- 20 mV
    mV_Neg15To15 = 21  # +/- 15 mV
    mV_Neg10To10 = 22  # +/- 10 mV
    mV_Neg5To5 = 23  # +/- 5 mV

    mV_0To625 = 24  # 0 ~ 625 mV
    mV_0To500 = 25  # 0 ~ 500 mV
    mV_0To150 = 26  # 0 ~ 150 mV
    mV_0To100 = 27  # 0 ~ 100 mV
    mV_0To50 = 28  # 0 ~ 50 mV
    mV_0To20 = 29  # 0 ~ 20 mV
    mV_0To15 = 30  # 0 ~ 15 mV
    mV_0To10 = 31  # 0 ~ 10 mV

    mA_Neg20To20 = 32  # +/- 20mA
    mA_0To20 = 33  # 0 ~ 20 mA
    mA_4To20 = 34  # 4 ~ 20 mA
    mA_0To24 = 35  # 0 ~ 24 mA

    # For USB4702_4704
    V_Neg2To2 = 36  # +/- 2 V
    V_Neg4To4 = 37  # +/- 4 V
    V_Neg20To20 = 38  # +/- 20 V

    Jtype_0To760C = 0x8000  # T/C J type 0~760 'C
    Ktype_0To1370C = 0x8001  # T/C K type 0~1370 'C
    Ttype_Neg100To400C = 0x8002  # T/C T type -100~400 'C
    Etype_0To1000C = 0x8003  # T/C E type 0~1000 'C
    Rtype_500To1750C = 0x8004  # T/C R type 500~1750 'C
    Stype_500To1750C = 0x8005  # T/C S type 500~1750 'C
    Btype_500To1800C = 0x8006  # T/C B type 500~1800 'C

    Pt392_Neg50To150 = 0x8007  # Pt392 -50~150 'C
    Pt385_Neg200To200 = 0x8008  # Pt385 -200~200 'C
    Pt385_0To400 = 0x8009  # Pt385 0~400 'C
    Pt385_Neg50To150 = 0x800a  # Pt385 -50~150 'C
    Pt385_Neg100To100 = 0x800b  # Pt385 -100~100 'C
    Pt385_0To100 = 0x800c  # Pt385 0~100 'C
    Pt385_0To200 = 0x800d  # Pt385 0~200 'C
    Pt385_0To600 = 0x800e  # Pt385 0~600 'C
    Pt392_Neg100To100 = 0x800f  # Pt392 -100~100 'C
    Pt392_0To100 = 0x8010  # Pt392 0~100 'C
    Pt392_0To200 = 0x8011  # Pt392 0~200 'C
    Pt392_0To600 = 0x8012  # Pt392 0~600 'C
    Pt392_0To400 = 0x8013  # Pt392 0~400 'C
    Pt392_Neg200To200 = 0x8014  # Pt392 -200~200 'C
    Pt1000_Neg40To160 = 0x8015  # Pt1000 -40~160 'C

    Balcon500_Neg30To120 = 0x8016  # Balcon500 -30~120 'C

    Ni518_Neg80To100 = 0x8017  # Ni518 -80~100 'C
    Ni518_0To100 = 0x8018  # Ni518 0~100 'C
    Ni508_0To100 = 0x8019  # Ni508 0~100 'C
    Ni508_Neg50To200 = 0x801a  # Ni508 -50~200 'C

    Thermistor_3K_0To100 = 0x801b  # Thermistor 3K 0~100 'C
    Thermistor_10K_0To100 = 0x801c  # Thermistor 10K 0~100 'C

    Jtype_Neg210To1200C = 0x801d  # T/C J type -210~1200 'C
    Ktype_Neg270To1372C = 0x801e  # T/C K type -270~1372 'C
    Ttype_Neg270To400C = 0x801f  # T/C T type -270~400 'C
    Etype_Neg270To1000C = 0x8020  # T/C E type -270~1000 'C
    Rtype_Neg50To1768C = 0x8021  # T/C R type -50~1768 'C
    Stype_Neg50To1768C = 0x8022  # T/C S type -50~1768 'C
    Btype_40To1820C = 0x8023  # T/C B type 40~1820 'C

    Jtype_Neg210To870C = 0x8024  # T/C J type -210~870 'C
    Rtype_0To1768C = 0x8025  # T/C R type 0~1768 'C
    Stype_0To1768C = 0x8026  # T/C S type 0~1768 'C
    Ttype_Neg20To135C = 0x8027  # T/C T type -20~135 'C

    V_0To30 = 0x8028  # 0 ~ 30 V
    A_0To3 = 0x8029  # 0 ~ 3 A

    Pt100_Neg50To150 = 0x802a  # Pt100 -50~150 'C
    Pt100_Neg200To200 = 0x802b  # Pt100 -200~200 'C
    Pt100_0To100 = 0x802c  # Pt100 0~100 'C
    Pt100_0To200 = 0x802d  # Pt100 0~200 'C
    Pt100_0To400 = 0x802e  # Pt100 0~400 'C
    Btype_300To1820C = 0x802f  # T/C B type 300~1820 'C

    V_Neg12pt5To12pt5 = 0x8030  # +/- 12.5 V

    # 0xC000 ~ 0xF000 : user customized value range type
    UserCustomizedVrgStart = 0xC000
    UserCustomizedVrgEnd = 0xF000

    # AO external reference type
    V_ExternalRefBipolar = 0xF001  # External reference voltage unipolar
    V_ExternalRefUnipolar = 0xF002  # External reference voltage bipolar


class SignalPolarity(IntEnum):
    Negative = 0
    Positive = 1


class CountingType(IntEnum):
    CountingNone = 0
    DownCount = 1  # counter value decreases on each clock
    UpCount = 2  # counter value increases on each clock
    PulseDirection = 3  # counting direction is determined by two signals, one is clock, the other is direction signal
    TwoPulse = 4  # counting direction is determined by two signals, one is up-counting signal, the other is down-counting signal
    AbPhaseX1 = 5  # AB phase, 1x rate up/down counting
    AbPhaseX2 = 6  # AB phase, 2x rate up/down counting
    AbPhaseX4 = 7  # AB phase, 4x rate up/down counting


class OutSignalType(IntEnum):
    SignalOutNone = 0  # no output or output is 'disabled'
    ChipDefined = 1  # hardware chip defined
    NegChipDefined = 2  # hardware chip defined, negative logical
    PositivePulse = 3  # a low-to-high pulse
    NegativePulse = 4  # a high-to-low pulse
    ToggledFromLow = 5  # the level toggled from low to high
    ToggledFromHigh = 6  # the level toggled from high to low


class CounterCapability(IntEnum):
    Primary = 1
    InstantEventCount = 2
    OneShot = 3
    TimerPulse = 4
    InstantFreqMeter = 5
    InstantPwmIn = 6
    InstantPwmOut = 7
    UpDownCount = 8
    BufferedEventCount = 9
    BufferedPwmIn = 10
    BufferedPwmOut = 11
    BufferedUpDownCount = 12
    InstantEdgeSeparation = 13


class CounterOperationMode(IntEnum):
    C8254_M0 = 0  # 8254 mode 0, interrupt on terminal count
    C8254_M1 = 1  # 8254 mode 1, hardware retriggerable one-shot
    C8254_M2 = 2  # 8254 mode 2, rate generator
    C8254_M3 = 3  # 8254 mode 3, square save mode
    C8254_M4 = 4  # 8254 mode 4, software triggered strobe
    C8254_M5 = 5  # 8254 mode 5, hardware triggered strobe

    C1780_MA = 6  # Mode A level & pulse out, Software-Triggered without Hardware Gating
    C1780_MB = 7  # Mode B level & pulse out, Software-Triggered with Level Gating, = 8254_M0
    C1780_MC = 8  # Mode C level & pulse out, Hardware-triggered strobe level
    C1780_MD = 9  # Mode D level & Pulse out, Rate generate with no hardware gating
    C1780_ME = 10  # Mode E level & pulse out, Rate generator with level Gating
    C1780_MF = 11  # Mode F level & pulse out, Non-retriggerable One-shot (Pulse type = 8254_M1)
    C1780_MG = 12  # Mode G level & pulse out, Software-triggered delayed pulse one-shot
    C1780_MH = 13  # Mode H level & pulse out, Software-triggered delayed pulse one-shot with hardware gating
    C1780_MI = 14  # Mode I level & pulse out, Hardware-triggered delay pulse strobe
    C1780_MJ = 15  # Mode J level & pulse out, Variable Duty Cycle Rate Generator with No Hardware Gating
    C1780_MK = 16  # Mode K level & pulse out, Variable Duty Cycle Rate Generator with Level Gating
    C1780_ML = 17  # Mode L level & pulse out, Hardware-Triggered Delayed Pulse One-Shot
    C1780_MO = 18  # Mode O level & pulse out, Hardware-Triggered Strobe with Edge Disarm
    C1780_MR = 19  # Mode R level & pulse out, Non-Retriggerbale One-Shot with Edge Disarm
    C1780_MU = 20  # Mode U level & pulse out, Hardware-Triggered Delayed Pulse Strobe with Edge Disarm
    C1780_MX = 21  # Mode X level & pulse out, Hardware-Triggered Delayed Pulse One-Shot with Edge Disarm


class CounterValueRegister(IntEnum):
    CntLoad = 0
    CntPreset = 0
    CntHold = 1
    CntOverCompare = 2
    CntUnderCompare = 3


class CounterCascadeGroup(IntEnum):
    GroupNone = 0  # no cascade
    Cnt0Cnt1 = 1  # Counter 0 as first, counter 1 as second.
    Cnt2Cnt3 = 2  # Counter 2 as first, counter 3 as second
    Cnt4Cnt5 = 3  # Counter 4 as first, counter 5 as second
    Cnt6Cnt7 = 4  # Counter 6 as first, counter 7 as second


class FreqMeasureMethod(IntEnum):
    AutoAdaptive = 0  # Intelligently select the measurement method according to the input signal.
    CountingPulseBySysTime = 1  # Using system timing clock to calculate the frequency
    CountingPulseByDevTime = 2  # Using the device timing clock to calculate the frequency
    PeriodInverse = 3  # Calculate the frequency from the period of the signal


class ActiveSignal(IntEnum):
    ActiveNone = 0
    RisingEdge = 1
    FallingEdge = 2
    BothEdge = 3
    HighLevel = 4
    LowLevel = 5


class TriggerAction(IntEnum):
    ActionNone = 0  # No action to take even if the trigger condition is satisfied
    DelayToStart = 1  # Begin to start after the specified time is elapsed if the trigger condition is satisfied
    DelayToStop = 2  # Stop execution after the specified time is elapsed if the trigger condition is satisfied
    Mark = 3  # Generate a mark data


class SignalPosition(IntEnum):
    InternalSig = 0
    OnConnector = 1
    OnAmsi = 2


class SignalDrop(IntEnum):
    SignalNone = 0  # No connection

    # Internal signal connector
    SigInternalClock = 1  # Device built-in clock, If the device has several built-in clock, this represent the highest freq one.
    SigInternal1KHz = 2  # Device built-in clock, 1KHz
    SigInternal10KHz = 3  # Device built-in clock, 10KHz
    SigInternal100KHz = 4  # Device built-in clock, 100KHz
    SigInternal1MHz = 5  # Device built-in clock, 1MHz
    SigInternal10MHz = 6  # Device built-in clock, 10MHz
    SigInternal20MHz = 7  # Device built-in clock, 20MHz
    SigInternal30MHz = 8  # Device built-in clock, 30MHz
    SigInternal40MHz = 9  # Device built-in clock, 40MHz
    SigInternal50MHz = 10  # Device built-in clock, 50MHz
    SigInternal60MHz = 11  # Device built-in clock, 60MHz

    SigDiPatternMatch = 12  # When DI pattern match occurred
    SigDiStatusChange = 13  # When DI status change occurred

    # Function pin on connector
    SigExtAnaClock = 14  # Analog clock pin of connector
    SigExtAnaScanClock = 15  # scan clock pin of connector
    SigExtAnaTrigger = 16  # external analog trigger pin of connector
    SigExtAnaTrigger0 = 16,  # external analog trigger pin of connector 0
    SigExtDigClock = 17  # digital clock pin of connector
    SigExtDigTrigger0 = 18  # external digital trigger 0 pin(or DI start trigger pin) of connector
    SigExtDigTrigger1 = 19  # external digital trigger 1 pin(or DI stop trigger pin) of connector
    SigExtDigTrigger2 = 20  # external digital trigger 2 pin(or DO start trigger pin) of connector
    SigExtDigTrigger3 = 21  # external digital trigger 3 pin(or DO stop trigger pin) of connector
    SigCHFrzDo = 22  # Channel freeze DO ports pin

    # Signal source or target on the connector
    # AI channel pins
    SigAi0 = 23
    SigAi1 = 24
    SigAi2 = 25
    SigAi3 = 26
    SigAi4 = 27
    SigAi5 = 28
    SigAi6 = 29
    SigAi7 = 30
    SigAi8 = 31
    SigAi9 = 32
    SigAi10 = 33
    SigAi11 = 34
    SigAi12 = 35
    SigAi13 = 36
    SigAi14 = 37
    SigAi15 = 38
    SigAi16 = 39
    SigAi17 = 40
    SigAi18 = 41
    SigAi19 = 42
    SigAi20 = 43
    SigAi21 = 44
    SigAi22 = 45
    SigAi23 = 46
    SigAi24 = 47
    SigAi25 = 48
    SigAi26 = 49
    SigAi27 = 50
    SigAi28 = 51
    SigAi29 = 52
    SigAi30 = 53
    SigAi31 = 54
    SigAi32 = 55
    SigAi33 = 56
    SigAi34 = 57
    SigAi35 = 58
    SigAi36 = 59
    SigAi37 = 60
    SigAi38 = 61
    SigAi39 = 62
    SigAi40 = 63
    SigAi41 = 64
    SigAi42 = 65
    SigAi43 = 66
    SigAi44 = 67
    SigAi45 = 68
    SigAi46 = 69
    SigAi47 = 70,
    SigAi48 = 71
    SigAi49 = 72
    SigAi50 = 73
    SigAi51 = 74
    SigAi52 = 75
    SigAi53 = 76
    SigAi54 = 77
    SigAi55 = 78
    SigAi56 = 79
    SigAi57 = 80
    SigAi58 = 81
    SigAi59 = 82
    SigAi60 = 83
    SigAi61 = 84
    SigAi62 = 85
    SigAi63 = 86

    # AO channel pins
    SigAo0 = 87
    SigAo1 = 88
    SigAo2 = 89
    SigAo3 = 90
    SigAo4 = 91
    SigAo5 = 92
    SigAo6 = 93
    SigAo7 = 94
    SigAo8 = 95
    SigAo9 = 96
    SigAo10 = 97
    SigAo11 = 98
    SigAo12 = 99
    SigAo13 = 100
    SigAo14 = 101
    SigAo15 = 102
    SigAo16 = 103
    SigAo17 = 104
    SigAo18 = 105
    SigAo19 = 106
    SigAo20 = 107
    SigAo21 = 108
    SigAo22 = 109
    SigAo23 = 110
    SigAo24 = 111
    SigAo25 = 112
    SigAo26 = 113
    SigAo27 = 114
    SigAo28 = 115
    SigAo29 = 116
    SigAo30 = 117
    SigAo31 = 118

    # DI pins
    SigDi0 = 119
    SigDi1 = 120
    SigDi2 = 121
    SigDi3 = 122
    SigDi4 = 123
    SigDi5 = 124
    SigDi6 = 125
    SigDi7 = 126
    SigDi8 = 127
    SigDi9 = 128
    SigDi10 = 129
    SigDi11 = 130
    SigDi12 = 131
    SigDi13 = 132
    SigDi14 = 133
    SigDi15 = 134
    SigDi16 = 135
    SigDi17 = 136
    SigDi18 = 137
    SigDi19 = 138
    SigDi20 = 139
    SigDi21 = 140
    SigDi22 = 141
    SigDi23 = 142
    SigDi24 = 143
    SigDi25 = 144
    SigDi26 = 145
    SigDi27 = 146
    SigDi28 = 147
    SigDi29 = 148
    SigDi30 = 149
    SigDi31 = 150
    SigDi32 = 151
    SigDi33 = 152
    SigDi34 = 153
    SigDi35 = 154
    SigDi36 = 155
    SigDi37 = 156
    SigDi38 = 157
    SigDi39 = 158
    SigDi40 = 159
    SigDi41 = 160
    SigDi42 = 161
    SigDi43 = 162
    SigDi44 = 163
    SigDi45 = 164
    SigDi46 = 165
    SigDi47 = 166
    SigDi48 = 167
    SigDi49 = 168
    SigDi50 = 169
    SigDi51 = 170
    SigDi52 = 171
    SigDi53 = 172
    SigDi54 = 173
    SigDi55 = 174
    SigDi56 = 175
    SigDi57 = 176
    SigDi58 = 177
    SigDi59 = 178
    SigDi60 = 179
    SigDi61 = 180
    SigDi62 = 181
    SigDi63 = 182
    SigDi64 = 183
    SigDi65 = 184
    SigDi66 = 185
    SigDi67 = 186
    SigDi68 = 187
    SigDi69 = 188
    SigDi70 = 189
    SigDi71 = 190
    SigDi72 = 191
    SigDi73 = 192
    SigDi74 = 193
    SigDi75 = 194
    SigDi76 = 195
    SigDi77 = 196
    SigDi78 = 197
    SigDi79 = 198
    SigDi80 = 199
    SigDi81 = 200
    SigDi82 = 201
    SigDi83 = 202
    SigDi84 = 203
    SigDi85 = 204
    SigDi86 = 205
    SigDi87 = 206
    SigDi88 = 207
    SigDi89 = 208
    SigDi90 = 209
    SigDi91 = 210
    SigDi92 = 211
    SigDi93 = 212
    SigDi94 = 213
    SigDi95 = 214
    SigDi96 = 215
    SigDi97 = 216
    SigDi98 = 217
    SigDi99 = 218
    SigDi100 = 219
    SigDi101 = 220
    SigDi102 = 221
    SigDi103 = 222
    SigDi104 = 223
    SigDi105 = 224
    SigDi106 = 225
    SigDi107 = 226
    SigDi108 = 227
    SigDi109 = 228
    SigDi110 = 229
    SigDi111 = 230
    SigDi112 = 231
    SigDi113 = 232
    SigDi114 = 233
    SigDi115 = 234
    SigDi116 = 235
    SigDi117 = 236
    SigDi118 = 237
    SigDi119 = 238
    SigDi120 = 239
    SigDi121 = 240
    SigDi122 = 241
    SigDi123 = 242
    SigDi124 = 243
    SigDi125 = 244
    SigDi126 = 245
    SigDi127 = 246
    SigDi128 = 247
    SigDi129 = 248
    SigDi130 = 249
    SigDi131 = 250
    SigDi132 = 251
    SigDi133 = 252
    SigDi134 = 253
    SigDi135 = 254
    SigDi136 = 255
    SigDi137 = 256
    SigDi138 = 257
    SigDi139 = 258
    SigDi140 = 259
    SigDi141 = 260
    SigDi142 = 261
    SigDi143 = 262
    SigDi144 = 263
    SigDi145 = 264
    SigDi146 = 265
    SigDi147 = 266
    SigDi148 = 267
    SigDi149 = 268
    SigDi150 = 269
    SigDi151 = 270
    SigDi152 = 271
    SigDi153 = 272
    SigDi154 = 273
    SigDi155 = 274
    SigDi156 = 275
    SigDi157 = 276
    SigDi158 = 277
    SigDi159 = 278
    SigDi160 = 279
    SigDi161 = 280
    SigDi162 = 281
    SigDi163 = 282
    SigDi164 = 283
    SigDi165 = 284
    SigDi166 = 285
    SigDi167 = 286
    SigDi168 = 287
    SigDi169 = 288
    SigDi170 = 289
    SigDi171 = 290
    SigDi172 = 291
    SigDi173 = 292
    SigDi174 = 293
    SigDi175 = 294
    SigDi176 = 295
    SigDi177 = 296
    SigDi178 = 297
    SigDi179 = 298
    SigDi180 = 299
    SigDi181 = 300
    SigDi182 = 301
    SigDi183 = 302
    SigDi184 = 303
    SigDi185 = 304
    SigDi186 = 305
    SigDi187 = 306
    SigDi188 = 307
    SigDi189 = 308
    SigDi190 = 309
    SigDi191 = 310
    SigDi192 = 311
    SigDi193 = 312
    SigDi194 = 313
    SigDi195 = 314
    SigDi196 = 315
    SigDi197 = 316
    SigDi198 = 317
    SigDi199 = 318
    SigDi200 = 319
    SigDi201 = 320
    SigDi202 = 321
    SigDi203 = 322
    SigDi204 = 323
    SigDi205 = 324
    SigDi206 = 325
    SigDi207 = 326
    SigDi208 = 327
    SigDi209 = 328
    SigDi210 = 329
    SigDi211 = 330
    SigDi212 = 331
    SigDi213 = 332
    SigDi214 = 333
    SigDi215 = 334
    SigDi216 = 335
    SigDi217 = 336
    SigDi218 = 337
    SigDi219 = 338
    SigDi220 = 339
    SigDi221 = 340
    SigDi222 = 341
    SigDi223 = 342
    SigDi224 = 343
    SigDi225 = 344
    SigDi226 = 345
    SigDi227 = 346
    SigDi228 = 347
    SigDi229 = 348
    SigDi230 = 349
    SigDi231 = 350
    SigDi232 = 351
    SigDi233 = 352
    SigDi234 = 353
    SigDi235 = 354
    SigDi236 = 355
    SigDi237 = 356
    SigDi238 = 357
    SigDi239 = 358
    SigDi240 = 359
    SigDi241 = 360
    SigDi242 = 361
    SigDi243 = 362
    SigDi244 = 363
    SigDi245 = 364
    SigDi246 = 365
    SigDi247 = 366
    SigDi248 = 367
    SigDi249 = 368
    SigDi250 = 369
    SigDi251 = 370
    SigDi252 = 371
    SigDi253 = 372
    SigDi254 = 373
    SigDi255 = 374

    # DIO pins
    SigDio0 = 375
    SigDio1 = 376
    SigDio2 = 377
    SigDio3 = 378
    SigDio4 = 379
    SigDio5 = 380
    SigDio6 = 381
    SigDio7 = 382
    SigDio8 = 383
    SigDio9 = 384
    SigDio10 = 385
    SigDio11 = 386
    SigDio12 = 387
    SigDio13 = 388
    SigDio14 = 389
    SigDio15 = 390
    SigDio16 = 391
    SigDio17 = 392
    SigDio18 = 393
    SigDio19 = 394
    SigDio20 = 395
    SigDio21 = 396
    SigDio22 = 397
    SigDio23 = 398
    SigDio24 = 399
    SigDio25 = 400
    SigDio26 = 401
    SigDio27 = 402
    SigDio28 = 403
    SigDio29 = 404
    SigDio30 = 405
    SigDio31 = 406
    SigDio32 = 407
    SigDio33 = 408
    SigDio34 = 409
    SigDio35 = 410
    SigDio36 = 411
    SigDio37 = 412
    SigDio38 = 413
    SigDio39 = 414
    SigDio40 = 415
    SigDio41 = 416
    SigDio42 = 417
    SigDio43 = 418
    SigDio44 = 419
    SigDio45 = 420
    SigDio46 = 421
    SigDio47 = 422
    SigDio48 = 423
    SigDio49 = 424
    SigDio50 = 425
    SigDio51 = 426
    SigDio52 = 427
    SigDio53 = 428
    SigDio54 = 429
    SigDio55 = 430
    SigDio56 = 431
    SigDio57 = 432
    SigDio58 = 433
    SigDio59 = 434
    SigDio60 = 435
    SigDio61 = 436
    SigDio62 = 437
    SigDio63 = 438
    SigDio64 = 439
    SigDio65 = 440
    SigDio66 = 441
    SigDio67 = 442
    SigDio68 = 443
    SigDio69 = 444
    SigDio70 = 445
    SigDio71 = 446
    SigDio72 = 447
    SigDio73 = 448
    SigDio74 = 449
    SigDio75 = 450
    SigDio76 = 451
    SigDio77 = 452
    SigDio78 = 453
    SigDio79 = 454
    SigDio80 = 455
    SigDio81 = 456
    SigDio82 = 457
    SigDio83 = 458
    SigDio84 = 459
    SigDio85 = 460
    SigDio86 = 461
    SigDio87 = 462
    SigDio88 = 463
    SigDio89 = 464
    SigDio90 = 465
    SigDio91 = 466
    SigDio92 = 467
    SigDio93 = 468
    SigDio94 = 469
    SigDio95 = 470
    SigDio96 = 471
    SigDio97 = 472
    SigDio98 = 473
    SigDio99 = 474
    SigDio100 = 475
    SigDio101 = 476
    SigDio102 = 477
    SigDio103 = 478
    SigDio104 = 479
    SigDio105 = 480
    SigDio106 = 481
    SigDio107 = 482
    SigDio108 = 483
    SigDio109 = 484
    SigDio110 = 485
    SigDio111 = 486
    SigDio112 = 487
    SigDio113 = 488
    SigDio114 = 489
    SigDio115 = 490
    SigDio116 = 491
    SigDio117 = 492
    SigDio118 = 493
    SigDio119 = 494
    SigDio120 = 495
    SigDio121 = 496
    SigDio122 = 497
    SigDio123 = 498
    SigDio124 = 499
    SigDio125 = 500
    SigDio126 = 501
    SigDio127 = 502
    SigDio128 = 503
    SigDio129 = 504
    SigDio130 = 505
    SigDio131 = 506
    SigDio132 = 507
    SigDio133 = 508
    SigDio134 = 509
    SigDio135 = 510
    SigDio136 = 511
    SigDio137 = 512
    SigDio138 = 513
    SigDio139 = 514
    SigDio140 = 515
    SigDio141 = 516
    SigDio142 = 517
    SigDio143 = 518
    SigDio144 = 519
    SigDio145 = 520
    SigDio146 = 521
    SigDio147 = 522
    SigDio148 = 523
    SigDio149 = 524
    SigDio150 = 525
    SigDio151 = 526
    SigDio152 = 527
    SigDio153 = 528
    SigDio154 = 529
    SigDio155 = 530
    SigDio156 = 531
    SigDio157 = 532
    SigDio158 = 533
    SigDio159 = 534
    SigDio160 = 535
    SigDio161 = 536
    SigDio162 = 537
    SigDio163 = 538
    SigDio164 = 539
    SigDio165 = 540
    SigDio166 = 541
    SigDio167 = 542
    SigDio168 = 543
    SigDio169 = 544
    SigDio170 = 545
    SigDio171 = 546
    SigDio172 = 547
    SigDio173 = 548
    SigDio174 = 549
    SigDio175 = 550
    SigDio176 = 551
    SigDio177 = 552
    SigDio178 = 553
    SigDio179 = 554
    SigDio180 = 555
    SigDio181 = 556
    SigDio182 = 557
    SigDio183 = 558
    SigDio184 = 559
    SigDio185 = 560
    SigDio186 = 561
    SigDio187 = 562
    SigDio188 = 563
    SigDio189 = 564
    SigDio190 = 565
    SigDio191 = 566
    SigDio192 = 567
    SigDio193 = 568
    SigDio194 = 569
    SigDio195 = 570
    SigDio196 = 571
    SigDio197 = 572
    SigDio198 = 573
    SigDio199 = 574
    SigDio200 = 575
    SigDio201 = 576
    SigDio202 = 577
    SigDio203 = 578
    SigDio204 = 579
    SigDio205 = 580
    SigDio206 = 581
    SigDio207 = 582
    SigDio208 = 583
    SigDio209 = 584
    SigDio210 = 585
    SigDio211 = 586
    SigDio212 = 587
    SigDio213 = 588
    SigDio214 = 589
    SigDio215 = 590
    SigDio216 = 591
    SigDio217 = 592
    SigDio218 = 593
    SigDio219 = 594
    SigDio220 = 595
    SigDio221 = 596
    SigDio222 = 597
    SigDio223 = 598
    SigDio224 = 599
    SigDio225 = 600
    SigDio226 = 601
    SigDio227 = 602
    SigDio228 = 603
    SigDio229 = 604
    SigDio230 = 605
    SigDio231 = 606
    SigDio232 = 607
    SigDio233 = 608
    SigDio234 = 609
    SigDio235 = 610
    SigDio236 = 611
    SigDio237 = 612
    SigDio238 = 613
    SigDio239 = 614
    SigDio240 = 615
    SigDio241 = 616
    SigDio242 = 617
    SigDio243 = 618
    SigDio244 = 619
    SigDio245 = 620
    SigDio246 = 621
    SigDio247 = 622
    SigDio248 = 623
    SigDio249 = 624
    SigDio250 = 625
    SigDio251 = 626
    SigDio252 = 627
    SigDio253 = 628
    SigDio254 = 629
    SigDio255 = 630

    # Counter clock pins
    SigCntClk0 = 631
    SigCntClk1 = 632
    SigCntClk2 = 633
    SigCntClk3 = 634
    SigCntClk4 = 635
    SigCntClk5 = 636
    SigCntClk6 = 637
    SigCntClk7 = 638

    # counter gate pins
    SigCntGate0 = 639
    SigCntGate1 = 640
    SigCntGate2 = 641
    SigCntGate3 = 642
    SigCntGate4 = 643
    SigCntGate5 = 644
    SigCntGate6 = 645
    SigCntGate7 = 646

    # counter out pins
    SigCntOut0 = 647
    SigCntOut1 = 648
    SigCntOut2 = 649
    SigCntOut3 = 650
    SigCntOut4 = 651
    SigCntOut5 = 652
    SigCntOut6 = 653
    SigCntOut7 = 654

    # counter frequency out pins
    SigCntFout0 = 655
    SigCntFout1 = 656
    SigCntFout2 = 657
    SigCntFout3 = 658
    SigCntFout4 = 659
    SigCntFout5 = 660
    SigCntFout6 = 661
    SigCntFout7 = 662

    # AMSI pins
    SigAmsiPin0 = 663
    SigAmsiPin1 = 664
    SigAmsiPin2 = 665
    SigAmsiPin3 = 666
    SigAmsiPin4 = 667
    SigAmsiPin5 = 668
    SigAmsiPin6 = 669
    SigAmsiPin7 = 670
    SigAmsiPin8 = 671
    SigAmsiPin9 = 672
    SigAmsiPin10 = 673
    SigAmsiPin11 = 674
    SigAmsiPin12 = 675
    SigAmsiPin13 = 676
    SigAmsiPin14 = 677
    SigAmsiPin15 = 678
    SigAmsiPin16 = 679
    SigAmsiPin17 = 680
    SigAmsiPin18 = 681
    SigAmsiPin19 = 682

    # new clocks
    SigInternal2Hz = 683  # Device built-in clock, 2Hz
    SigInternal20Hz = 684  # Device built-in clock, 20Hz
    SigInternal200Hz = 685  # Device built-in clock, 200KHz
    SigInternal2KHz = 686  # Device built-in clock, 2KHz
    SigInternal20KHz = 687  # Device built-in clock, 20KHz
    SigInternal200KHz = 688  # Device built-in clock, 200KHz
    SigInternal2MHz = 689  # Device built-in clock, 2MHz

    # New Function pin on connector
    SigExtAnaTrigger1 = 690  # external analog trigger pin of connector 1

    # Reference clock
    SigExtDigRefClock = 691  # digital clock pin of connector
    SigInternal100MHz = 692
    SigAiConvClock = 693

    # digital trigger from master after ADC latency
    SigExtDigTrgAdcLatency = 694
    SigExtDigTrg0AdcLatency = SigExtDigTrgAdcLatency,
    SigExtDigTrg1AdcLatency = 695

    # digital trigger from master/MSDI pin after ADC latency
    SigMDSITrg0 = 696
    SigMDSITrg1 = 697

    SigMDSITrg0AdcLatency = 698
    SigMDSITrg1AdcLatency = 699

    # reference clock source from master/MDSI pin
    SigMDSIRefClock = 700
    SigMDSIClock = 701

    # clock source & trigger for Master/Slave module
    # internal clock x, as a master module
    SigIntClock0 = 702
    SigIntClock1 = 703
    SigIntClock2 = 704
    SigIntClock3 = 705

    # clock from internal clock x, as a slave module
    SigIntClk0Slv = 706
    SigIntClk1Slv = 707
    SigIntClk2Slv = 708
    SigIntClk3Slv = 709

    # Trigger x from trigger pin, as a slave module
    SigExtDigTrg0Slv = 710
    SigExtDigTrg1Slv = 711
    SigExtDigTrg2Slv = 712
    SigExtDigTrg3Slv = 713


class EventId(IntEnum):
    EvtDeviceRemoved = 0  # The device was removed from system
    EvtDeviceReconnected = 1  # The device is reconnected
    EvtPropertyChanged = 2  # Some properties of the device were changed
    # -----------------------------------------------------------------
    # AI events
    # -----------------------------------------------------------------
    EvtBufferedAiDataReady = 3
    EvtBufferedAiOverrun = 4
    EvtBufferedAiCacheOverflow = 5
    EvtBufferedAiStopped = 6

    # -----------------------------------------------------------------
    #  AO event IDs
    # -----------------------------------------------------------------
    EvtBufferedAoDataTransmitted = 7
    EvtBufferedAoUnderrun = 8
    EvtBufferedAoCacheEmptied = 9
    EvtBufferedAoTransStopped = 10
    EvtBufferedAoStopped = 11

    # -----------------------------------------------------------------
    #  DIO event IDs
    # -----------------------------------------------------------------
    EvtDiInterrupt = 12
    EvtDiintChannel000 = EvtDiInterrupt
    EvtDiintChannel001 = 13
    EvtDiintChannel002 = 14
    EvtDiintChannel003 = 15
    EvtDiintChannel004 = 16
    EvtDiintChannel005 = 17
    EvtDiintChannel006 = 18
    EvtDiintChannel007 = 19
    EvtDiintChannel008 = 20
    EvtDiintChannel009 = 21
    EvtDiintChannel010 = 22
    EvtDiintChannel011 = 23
    EvtDiintChannel012 = 24
    EvtDiintChannel013 = 25
    EvtDiintChannel014 = 26
    EvtDiintChannel015 = 27
    EvtDiintChannel016 = 28
    EvtDiintChannel017 = 29
    EvtDiintChannel018 = 30
    EvtDiintChannel019 = 31
    EvtDiintChannel020 = 32
    EvtDiintChannel021 = 33
    EvtDiintChannel022 = 34
    EvtDiintChannel023 = 35
    EvtDiintChannel024 = 36
    EvtDiintChannel025 = 37
    EvtDiintChannel026 = 38
    EvtDiintChannel027 = 39
    EvtDiintChannel028 = 40
    EvtDiintChannel029 = 41
    EvtDiintChannel030 = 42
    EvtDiintChannel031 = 43
    EvtDiintChannel032 = 44
    EvtDiintChannel033 = 45
    EvtDiintChannel034 = 46
    EvtDiintChannel035 = 47
    EvtDiintChannel036 = 48
    EvtDiintChannel037 = 49
    EvtDiintChannel038 = 50
    EvtDiintChannel039 = 51
    EvtDiintChannel040 = 52
    EvtDiintChannel041 = 53
    EvtDiintChannel042 = 54
    EvtDiintChannel043 = 55
    EvtDiintChannel044 = 56
    EvtDiintChannel045 = 57
    EvtDiintChannel046 = 58
    EvtDiintChannel047 = 59
    EvtDiintChannel048 = 60
    EvtDiintChannel049 = 61
    EvtDiintChannel050 = 62
    EvtDiintChannel051 = 63
    EvtDiintChannel052 = 64
    EvtDiintChannel053 = 65
    EvtDiintChannel054 = 66
    EvtDiintChannel055 = 67
    EvtDiintChannel056 = 68
    EvtDiintChannel057 = 69
    EvtDiintChannel058 = 70
    EvtDiintChannel059 = 71
    EvtDiintChannel060 = 72
    EvtDiintChannel061 = 73
    EvtDiintChannel062 = 74
    EvtDiintChannel063 = 75
    EvtDiintChannel064 = 76
    EvtDiintChannel065 = 77
    EvtDiintChannel066 = 78
    EvtDiintChannel067 = 79
    EvtDiintChannel068 = 80
    EvtDiintChannel069 = 81
    EvtDiintChannel070 = 82
    EvtDiintChannel071 = 83
    EvtDiintChannel072 = 84
    EvtDiintChannel073 = 85
    EvtDiintChannel074 = 86
    EvtDiintChannel075 = 87
    EvtDiintChannel076 = 88
    EvtDiintChannel077 = 89
    EvtDiintChannel078 = 90
    EvtDiintChannel079 = 91
    EvtDiintChannel080 = 92
    EvtDiintChannel081 = 93
    EvtDiintChannel082 = 94
    EvtDiintChannel083 = 95
    EvtDiintChannel084 = 96
    EvtDiintChannel085 = 97
    EvtDiintChannel086 = 98
    EvtDiintChannel087 = 99
    EvtDiintChannel088 = 100
    EvtDiintChannel089 = 101
    EvtDiintChannel090 = 102
    EvtDiintChannel091 = 103
    EvtDiintChannel092 = 104
    EvtDiintChannel093 = 105
    EvtDiintChannel094 = 106
    EvtDiintChannel095 = 107
    EvtDiintChannel096 = 108
    EvtDiintChannel097 = 109
    EvtDiintChannel098 = 110
    EvtDiintChannel099 = 111
    EvtDiintChannel100 = 112
    EvtDiintChannel101 = 113
    EvtDiintChannel102 = 114
    EvtDiintChannel103 = 115
    EvtDiintChannel104 = 116
    EvtDiintChannel105 = 117
    EvtDiintChannel106 = 118
    EvtDiintChannel107 = 119
    EvtDiintChannel108 = 120
    EvtDiintChannel109 = 121
    EvtDiintChannel110 = 122
    EvtDiintChannel111 = 123
    EvtDiintChannel112 = 124
    EvtDiintChannel113 = 125
    EvtDiintChannel114 = 126
    EvtDiintChannel115 = 127
    EvtDiintChannel116 = 128
    EvtDiintChannel117 = 129
    EvtDiintChannel118 = 130
    EvtDiintChannel119 = 131
    EvtDiintChannel120 = 132
    EvtDiintChannel121 = 133
    EvtDiintChannel122 = 134
    EvtDiintChannel123 = 135
    EvtDiintChannel124 = 136
    EvtDiintChannel125 = 137
    EvtDiintChannel126 = 138
    EvtDiintChannel127 = 139
    EvtDiintChannel128 = 140
    EvtDiintChannel129 = 141
    EvtDiintChannel130 = 142
    EvtDiintChannel131 = 143
    EvtDiintChannel132 = 144
    EvtDiintChannel133 = 145
    EvtDiintChannel134 = 146
    EvtDiintChannel135 = 147
    EvtDiintChannel136 = 148
    EvtDiintChannel137 = 149
    EvtDiintChannel138 = 150
    EvtDiintChannel139 = 151
    EvtDiintChannel140 = 152
    EvtDiintChannel141 = 153
    EvtDiintChannel142 = 154
    EvtDiintChannel143 = 155
    EvtDiintChannel144 = 156
    EvtDiintChannel145 = 157
    EvtDiintChannel146 = 158
    EvtDiintChannel147 = 159
    EvtDiintChannel148 = 160
    EvtDiintChannel149 = 161
    EvtDiintChannel150 = 162
    EvtDiintChannel151 = 163
    EvtDiintChannel152 = 164
    EvtDiintChannel153 = 165
    EvtDiintChannel154 = 166
    EvtDiintChannel155 = 167
    EvtDiintChannel156 = 168
    EvtDiintChannel157 = 169
    EvtDiintChannel158 = 170
    EvtDiintChannel159 = 171
    EvtDiintChannel160 = 172
    EvtDiintChannel161 = 173
    EvtDiintChannel162 = 174
    EvtDiintChannel163 = 175
    EvtDiintChannel164 = 176
    EvtDiintChannel165 = 177
    EvtDiintChannel166 = 178
    EvtDiintChannel167 = 179
    EvtDiintChannel168 = 180
    EvtDiintChannel169 = 181
    EvtDiintChannel170 = 182
    EvtDiintChannel171 = 183
    EvtDiintChannel172 = 184
    EvtDiintChannel173 = 185
    EvtDiintChannel174 = 186
    EvtDiintChannel175 = 187
    EvtDiintChannel176 = 188
    EvtDiintChannel177 = 189
    EvtDiintChannel178 = 190
    EvtDiintChannel179 = 191
    EvtDiintChannel180 = 192
    EvtDiintChannel181 = 193
    EvtDiintChannel182 = 194
    EvtDiintChannel183 = 195
    EvtDiintChannel184 = 196
    EvtDiintChannel185 = 197
    EvtDiintChannel186 = 198
    EvtDiintChannel187 = 199
    EvtDiintChannel188 = 200
    EvtDiintChannel189 = 201
    EvtDiintChannel190 = 202
    EvtDiintChannel191 = 203
    EvtDiintChannel192 = 204
    EvtDiintChannel193 = 205
    EvtDiintChannel194 = 206
    EvtDiintChannel195 = 207
    EvtDiintChannel196 = 208
    EvtDiintChannel197 = 209
    EvtDiintChannel198 = 210
    EvtDiintChannel199 = 211
    EvtDiintChannel200 = 212
    EvtDiintChannel201 = 213
    EvtDiintChannel202 = 214
    EvtDiintChannel203 = 215
    EvtDiintChannel204 = 216
    EvtDiintChannel205 = 217
    EvtDiintChannel206 = 218
    EvtDiintChannel207 = 219
    EvtDiintChannel208 = 220
    EvtDiintChannel209 = 221
    EvtDiintChannel210 = 222
    EvtDiintChannel211 = 223
    EvtDiintChannel212 = 224
    EvtDiintChannel213 = 225
    EvtDiintChannel214 = 226
    EvtDiintChannel215 = 227
    EvtDiintChannel216 = 228
    EvtDiintChannel217 = 229
    EvtDiintChannel218 = 230
    EvtDiintChannel219 = 231
    EvtDiintChannel220 = 232
    EvtDiintChannel221 = 233
    EvtDiintChannel222 = 234
    EvtDiintChannel223 = 235
    EvtDiintChannel224 = 236
    EvtDiintChannel225 = 237
    EvtDiintChannel226 = 238
    EvtDiintChannel227 = 239
    EvtDiintChannel228 = 240
    EvtDiintChannel229 = 241
    EvtDiintChannel230 = 242
    EvtDiintChannel231 = 243
    EvtDiintChannel232 = 244
    EvtDiintChannel233 = 245
    EvtDiintChannel234 = 246
    EvtDiintChannel235 = 247
    EvtDiintChannel236 = 248
    EvtDiintChannel237 = 249
    EvtDiintChannel238 = 250
    EvtDiintChannel239 = 251
    EvtDiintChannel240 = 252
    EvtDiintChannel241 = 253
    EvtDiintChannel242 = 254
    EvtDiintChannel243 = 255
    EvtDiintChannel244 = 256
    EvtDiintChannel245 = 257
    EvtDiintChannel246 = 258
    EvtDiintChannel247 = 259
    EvtDiintChannel248 = 260
    EvtDiintChannel249 = 261
    EvtDiintChannel250 = 262
    EvtDiintChannel251 = 263
    EvtDiintChannel252 = 264
    EvtDiintChannel253 = 265
    EvtDiintChannel254 = 266
    EvtDiintChannel255 = 267

    EvtDiStatusChange = 268
    EvtDiCosintPort000 = EvtDiStatusChange
    EvtDiCosintPort001 = 269
    EvtDiCosintPort002 = 270
    EvtDiCosintPort003 = 271
    EvtDiCosintPort004 = 272
    EvtDiCosintPort005 = 273
    EvtDiCosintPort006 = 274
    EvtDiCosintPort007 = 275
    EvtDiCosintPort008 = 276
    EvtDiCosintPort009 = 277
    EvtDiCosintPort010 = 278
    EvtDiCosintPort011 = 279
    EvtDiCosintPort012 = 280
    EvtDiCosintPort013 = 281
    EvtDiCosintPort014 = 282
    EvtDiCosintPort015 = 283
    EvtDiCosintPort016 = 284
    EvtDiCosintPort017 = 285
    EvtDiCosintPort018 = 286
    EvtDiCosintPort019 = 287
    EvtDiCosintPort020 = 288
    EvtDiCosintPort021 = 289
    EvtDiCosintPort022 = 290
    EvtDiCosintPort023 = 291
    EvtDiCosintPort024 = 292
    EvtDiCosintPort025 = 293
    EvtDiCosintPort026 = 294
    EvtDiCosintPort027 = 295
    EvtDiCosintPort028 = 296
    EvtDiCosintPort029 = 297
    EvtDiCosintPort030 = 298
    EvtDiCosintPort031 = 299

    EvtDiPatternMatch = 300
    EvtDiPmintPort000 = EvtDiPatternMatch
    EvtDiPmintPort001 = 301
    EvtDiPmintPort002 = 302
    EvtDiPmintPort003 = 303
    EvtDiPmintPort004 = 304
    EvtDiPmintPort005 = 305
    EvtDiPmintPort006 = 306
    EvtDiPmintPort007 = 307
    EvtDiPmintPort008 = 308
    EvtDiPmintPort009 = 309
    EvtDiPmintPort010 = 310
    EvtDiPmintPort011 = 311
    EvtDiPmintPort012 = 312
    EvtDiPmintPort013 = 313
    EvtDiPmintPort014 = 314
    EvtDiPmintPort015 = 315
    EvtDiPmintPort016 = 316
    EvtDiPmintPort017 = 317
    EvtDiPmintPort018 = 318
    EvtDiPmintPort019 = 319
    EvtDiPmintPort020 = 320
    EvtDiPmintPort021 = 321
    EvtDiPmintPort022 = 322
    EvtDiPmintPort023 = 323
    EvtDiPmintPort024 = 324
    EvtDiPmintPort025 = 325
    EvtDiPmintPort026 = 326
    EvtDiPmintPort027 = 327
    EvtDiPmintPort028 = 328
    EvtDiPmintPort029 = 329
    EvtDiPmintPort030 = 330
    EvtDiPmintPort031 = 331

    EvtBufferedDiDataReady = 332
    EvtBufferedDiOverrun = 333
    EvtBufferedDiCacheOverflow = 334
    EvtBufferedDiStopped = 335

    EvtBufferedDoDataTransmitted = 336
    EvtBufferedDoUnderrun = 337
    EvtBufferedDoCacheEmptied = 338
    EvtBufferedDoTransStopped = 339
    EvtBufferedDoStopped = 340

    EvtReflectWdtOccured = 341

    # -----------------------------------------------------------------
    # Counter/Timer event IDs
    # -----------------------------------------------------------------
    EvtCntTerminalCount0 = 342
    EvtCntTerminalCount1 = 343
    EvtCntTerminalCount2 = 344
    EvtCntTerminalCount3 = 345
    EvtCntTerminalCount4 = 346
    EvtCntTerminalCount5 = 347
    EvtCntTerminalCount6 = 348
    EvtCntTerminalCount7 = 349

    EvtCntOverCompare0 = 350
    EvtCntOverCompare1 = 351
    EvtCntOverCompare2 = 352
    EvtCntOverCompare3 = 353
    EvtCntOverCompare4 = 354
    EvtCntOverCompare5 = 355
    EvtCntOverCompare6 = 356
    EvtCntOverCompare7 = 357

    EvtCntUnderCompare0 = 358
    EvtCntUnderCompare1 = 359
    EvtCntUnderCompare2 = 360
    EvtCntUnderCompare3 = 361
    EvtCntUnderCompare4 = 362
    EvtCntUnderCompare5 = 363
    EvtCntUnderCompare6 = 364
    EvtCntUnderCompare7 = 365

    EvtCntEcOverCompare0 = 366
    EvtCntEcOverCompare1 = 367
    EvtCntEcOverCompare2 = 368
    EvtCntEcOverCompare3 = 369
    EvtCntEcOverCompare4 = 370
    EvtCntEcOverCompare5 = 371
    EvtCntEcOverCompare6 = 372
    EvtCntEcOverCompare7 = 373

    EvtCntEcUnderCompare0 = 374
    EvtCntEcUnderCompare1 = 375
    EvtCntEcUnderCompare2 = 376
    EvtCntEcUnderCompare3 = 377
    EvtCntEcUnderCompare4 = 378
    EvtCntEcUnderCompare5 = 379
    EvtCntEcUnderCompare6 = 380
    EvtCntEcUnderCompare7 = 381

    EvtCntOneShot0 = 382
    EvtCntOneShot1 = 383
    EvtCntOneShot2 = 384
    EvtCntOneShot3 = 385
    EvtCntOneShot4 = 386
    EvtCntOneShot5 = 387
    EvtCntOneShot6 = 388
    EvtCntOneShot7 = 389

    EvtCntTimer0 = 390
    EvtCntTimer1 = 391
    EvtCntTimer2 = 392
    EvtCntTimer3 = 393
    EvtCntTimer4 = 394
    EvtCntTimer5 = 395
    EvtCntTimer6 = 396
    EvtCntTimer7 = 397

    EvtCntPwmInOverflow0 = 398
    EvtCntPwmInOverflow1 = 399
    EvtCntPwmInOverflow2 = 400
    EvtCntPwmInOverflow3 = 401
    EvtCntPwmInOverflow4 = 402
    EvtCntPwmInOverflow5 = 403
    EvtCntPwmInOverflow6 = 404
    EvtCntPwmInOverflow7 = 405

    EvtUdIndex0 = 406
    EvtUdIndex1 = 407
    EvtUdIndex2 = 408
    EvtUdIndex3 = 409
    EvtUdIndex4 = 410
    EvtUdIndex5 = 411
    EvtUdIndex6 = 412
    EvtUdIndex7 = 413

    EvtCntPatternMatch0 = 414
    EvtCntPatternMatch1 = 415
    EvtCntPatternMatch2 = 416
    EvtCntPatternMatch3 = 417
    EvtCntPatternMatch4 = 418
    EvtCntPatternMatch5 = 419
    EvtCntPatternMatch6 = 420
    EvtCntPatternMatch7 = 421

    EvtCntCompareTableEnd0 = 422
    EvtCntCompareTableEnd1 = 423
    EvtCntCompareTableEnd2 = 424
    EvtCntCompareTableEnd3 = 425
    EvtCntCompareTableEnd4 = 426
    EvtCntCompareTableEnd5 = 427
    EvtCntCompareTableEnd6 = 428
    EvtCntCompareTableEnd7 = 429

    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # v1.1: new event of AI
    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#
    EvtBufferedAiBurnOut = 430
    EvtBufferedAiTimeStampOverrun = 431
    EvtBufferedAiTimeStampCacheOverflow = 432
    EvtBufferedAiMarkOverrun = 433
    EvtBufferedAiConvStopped = 434  # Reserved for later using

    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # v1.2: new event of Buffered Counter
    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    EvtCiDataReady = 435
    EvtCiDataReady0 = EvtCiDataReady
    EvtCiDataReady1 = 436
    EvtCiDataReady2 = 437
    EvtCiDataReady3 = 438
    EvtCiDataReady4 = 439
    EvtCiDataReady5 = 440
    EvtCiDataReady6 = 441
    EvtCiDataReady7 = 442

    EvtCiOverrun = 443
    EvtCiOverrun0 = EvtCiOverrun
    EvtCiOverrun1 = 444
    EvtCiOverrun2 = 445
    EvtCiOverrun3 = 446
    EvtCiOverrun4 = 447
    EvtCiOverrun5 = 448
    EvtCiOverrun6 = 449
    EvtCiOverrun7 = 450

    EvtCiCacheOverflow = 451
    EvtCiCacheOverflow0 = EvtCiCacheOverflow
    EvtCiCacheOverflow1 = 452
    EvtCiCacheOverflow2 = 453
    EvtCiCacheOverflow3 = 454
    EvtCiCacheOverflow4 = 455
    EvtCiCacheOverflow5 = 456
    EvtCiCacheOverflow6 = 457
    EvtCiCacheOverflow7 = 458

    EvtCoDataTransmitted = 459
    EvtCoDataTransmitted0 = EvtCoDataTransmitted
    EvtCoDataTransmitted1 = 460
    EvtCoDataTransmitted2 = 461
    EvtCoDataTransmitted3 = 462
    EvtCoDataTransmitted4 = 463
    EvtCoDataTransmitted5 = 464
    EvtCoDataTransmitted6 = 465
    EvtCoDataTransmitted7 = 466

    EvtCoUnderrun = 467
    EvtCoUnderrun0 = EvtCoUnderrun
    EvtCoUnderrun1 = 468
    EvtCoUnderrun2 = 469
    EvtCoUnderrun3 = 470
    EvtCoUnderrun4 = 471
    EvtCoUnderrun5 = 472
    EvtCoUnderrun6 = 473
    EvtCoUnderrun7 = 474

    EvtCoCacheEmptied = 475
    EvtCoCacheEmptied0 = EvtCoCacheEmptied
    EvtCoCacheEmptied1 = 476
    EvtCoCacheEmptied2 = 477
    EvtCoCacheEmptied3 = 478
    EvtCoCacheEmptied4 = 479
    EvtCoCacheEmptied5 = 480
    EvtCoCacheEmptied6 = 481
    EvtCoCacheEmptied7 = 482

    EvtCoTransStopped = 483
    EvtCoTransStopped0 = EvtCoTransStopped
    EvtCoTransStopped1 = 484
    EvtCoTransStopped2 = 485
    EvtCoTransStopped3 = 486
    EvtCoTransStopped4 = 487
    EvtCoTransStopped5 = 488
    EvtCoTransStopped6 = 489
    EvtCoTransStopped7 = 490

    EvtCntrStopped = 491
    EvtCntrStopped0 = EvtCntrStopped
    EvtCntrStopped1 = 492
    EvtCntrStopped2 = 493
    EvtCntrStopped3 = 494
    EvtCntrStopped4 = 495
    EvtCntrStopped5 = 496
    EvtCntrStopped6 = 497
    EvtCntrStopped7 = 498


class ErrorCode(Enum):
    # <summary>
    # The operation is completed successfully.
    # </summary>
    Success = 0

    # ************************************************************************
    # warning
    # ************************************************************************
    # <summary>
    # The interrupt resource is not available.
    # </summary>
    WarningIntrNotAvailable = 0xA0000000

    # <summary>
    # The parameter is out of the range.
    # </summary>
    WarningParamOutOfRange = 0xA0000001

    # <summary>
    # The property value is out of range.
    # </summary>
    WarningPropValueOutOfRange = 0xA0000002

    # <summary>
    # The property value is not supported.
    # </summary>
    WarningPropValueNotSpted = 0xA0000003

    # <summary>
    # The property value conflicts with the current state.
    # </summary>
    WarningPropValueConflict = 0xA0000004

    # <summary>
    # The value range of all channels in a group should be same,
    # such as 4~20mA of PCI-1724.
    # </summary>
    WarningVrgOfGroupNotSame = 0xA0000005

    # <summary>
    # Some properties of a property set are failed to be written into device.
    #
    # </summary>
    WarningPropPartialFailed = 0xA0000006

    # <summary>
    # The operation had been stopped.
    #
    # </summary>
    WarningFuncStopped = 0xA0000007

    # <summary>
    # The operation is time-out.
    #
    # </summary>
    WarningFuncTimeout = 0xA0000008

    # <summary>
    # The cache is over-run.
    #
    # </summary>
    WarningCacheOverflow = 0xA0000009

    # <summary>
    # The channel is burn-out.
    #
    # </summary>
    WarningBurnout = 0xA000000A

    # <summary>
    # The current data record is end.
    #
    # </summary>
    WarningRecordEnd = 0xA000000B

    # <summary>
    # The specified profile is not valid.
    #
    # </summary>
    WarningProfileNotValid = 0xA000000C

    # ***********************************************************************
    # error
    # ***********************************************************************
    # <summary>
    # The handle is NULL or its type doesn't match the required operation.
    # </summary>
    ErrorHandleNotValid = 0xE0000000

    # <summary>
    # The parameter value is out of range.
    # </summary>
    ErrorParamOutOfRange = 0xE0000001

    # <summary>
    # The parameter value is not supported.
    # </summary>
    ErrorParamNotSpted = 0xE0000002

    # <summary>
    # The parameter value format is not the expected.
    # </summary>
    ErrorParamFmtUnexpted = 0xE0000003

    # <summary>
    # Not enough memory is available to complete the operation.
    # </summary>
    ErrorMemoryNotEnough = 0xE0000004

    # <summary>
    # The data buffer is null.
    # </summary>
    ErrorBufferIsNull = 0xE0000005

    # <summary>
    # The data buffer is too small for the operation.
    # </summary>
    ErrorBufferTooSmall = 0xE0000006

    # <summary>
    # The data length exceeded the limitation.
    # </summary>
    ErrorDataLenExceedLimit = 0xE0000007

    # <summary>
    # The required function is not supported.
    # </summary>
    ErrorFuncNotSpted = 0xE0000008

    # <summary>
    # The required event is not supported.
    # </summary>
    ErrorEventNotSpted = 0xE0000009

    # <summary>
    # The required property is not supported.
    # </summary>
    ErrorPropNotSpted = 0xE000000A

    # <summary>
    # The required property is read-only.
    # </summary>
    ErrorPropReadOnly = 0xE000000B

    # <summary>
    # The specified property value conflicts with the current state.
    # </summary>
    ErrorPropValueConflict = 0xE000000C

    # <summary>
    # The specified property value is out of range.
    # </summary>
    ErrorPropValueOutOfRange = 0xE000000D

    # <summary>
    # The specified property value is not supported.
    # </summary>
    ErrorPropValueNotSpted = 0xE000000E

    # <summary>
    # The handle hasn't own the privilege of the operation the user wanted.
    # </summary>
    ErrorPrivilegeNotHeld = 0xE000000F

    # <summary>
    # The required privilege is not available because someone else had own it.
    # </summary>
    ErrorPrivilegeNotAvailable = 0xE0000010

    # <summary>
    # The driver of specified device was not found.
    # </summary>
    ErrorDriverNotFound = 0xE0000011

    # <summary>
    # The driver version of the specified device mismatched.
    # </summary>
    ErrorDriverVerMismatch = 0xE0000012

    # <summary>
    # The loaded driver count exceeded the limitation.
    # </summary>
    ErrorDriverCountExceedLimit = 0xE0000013

    # <summary>
    # The device is not opened.
    # </summary>
    ErrorDeviceNotOpened = 0xE0000014

    # <summary>
    # The required device does not exist.
    # </summary>
    ErrorDeviceNotExist = 0xE0000015

    # <summary>
    # The required device is unrecognized by driver.
    # </summary>
    ErrorDeviceUnrecognized = 0xE0000016

    # <summary>
    # The configuration data of the specified device is lost or unavailable.
    # </summary>
    ErrorConfigDataLost = 0xE0000017

    # <summary>
    # The function is not initialized and can't be started.
    # </summary>
    ErrorFuncNotInited = 0xE0000018

    # <summary>
    # The function is busy.
    # </summary>
    ErrorFuncBusy = 0xE0000019

    # <summary>
    # The interrupt resource is not available.
    # </summary>
    ErrorIntrNotAvailable = 0xE000001A

    # <summary>
    # The DMA channel is not available.
    # </summary>
    ErrorDmaNotAvailable = 0xE000001B

    # <summary>
    # Time out when reading/writing the device.
    # </summary>
    ErrorDeviceIoTimeOut = 0xE000001C

    # <summary>
    # The given signature does not match with the device current one.
    # </summary>
    ErrorSignatureNotMatch = 0xE000001D

    # <summary>
    # The function cannot be executed while the buffered AI is running.
    # </summary>
    ErrorFuncConflictWithBfdAi = 0xE000001E

    # <summary>
    # The value range is not available in single-ended mode.
    # </summary>
    ErrorVrgNotAvailableInSeMode = 0xE000001F

    # <summary>
    # The value range is not available in 50omh input impedance mode..
    # </summary>
    ErrorVrgNotAvailableIn50ohmMode = 0xE0000020

    # <summary>
    # The coupling type is not available in 50omh input impedance mode..
    # </summary>
    ErrorCouplingNotAvailableIn50ohmMode = 0xE0000021

    # <summary>
    # The coupling type is not available in IEPE mode.
    # </summary>
    ErrorCouplingNotAvailableInIEPEMode = 0xE0000022

    # <summary>
    # The Communication is failed when reading/writing the device.
    # </summary>
    ErrorDeviceCommunicationFailed = 0xE0000023

    # <summary>
    # The device's 'fix number' conflicted with other device's
    # </summary>
    ErrorFixNumberConflict = 0xE0000024

    # <summary>
    # The Trigger source conflicted with other trigger configuration
    # </summary>
    ErrorTrigSrcConflict = 0xE0000025

    # <summary>
    # All properties of a property set are failed to be written into device.
    # </summary>
    ErrorPropAllFailed = 0xE0000026

    # <summary>
    # Undefined error
    # </summary>
    ErrorUndefined = 0xE000FFFF

    @staticmethod
    def lookup(value):
        value = value & 0xFFFFFFFF
        for code in ErrorCode:
            if value == code.value:
                return code
        return ErrorCode.ErrorUndefined

    # def toInt(self):
    #     return self.value
    #
    # def toString(self):
    #     return AdxEnumToString("ErrorCode", self.value, 256)


class ProductId(IntEnum):
    BD_DEMO = 0x00  # demo board
    BD_PCL818 = 0x05  # PCL-818 board
    BD_PCL818H = 0x11  # PCL-818H
    BD_PCL818L = 0x21  # PCL-818L
    BD_PCL818HG = 0x22  # PCL-818HG
    BD_PCL818HD = 0x2b  # PCL-818HD
    BD_PCM3718 = 0x37  # PCM-3718
    BD_PCM3724 = 0x38  # PCM-3724
    BD_PCM3730 = 0x5a  # PCM-3730
    BD_PCI1750 = 0x5e  # PCI-1750
    BD_PCI1751 = 0x5f  # PCI-1751
    BD_PCI1710 = 0x60  # PCI-1710
    BD_PCI1712 = 0x61  # PCI-1712
    BD_PCI1710HG = 0x67  # PCI-1710HG
    BD_PCI1711 = 0x73  # PCI-1711
    BD_PCI1711L = 0x75  # PCI-1711L
    BD_PCI1713 = 0x68  # PCI-1713
    BD_PCI1753 = 0x69  # PCI-1753
    BD_PCI1760 = 0x6a  # PCI-1760
    BD_PCI1720 = 0x6b  # PCI-1720
    BD_PCM3718H = 0x6d  # PCM-3718H
    BD_PCM3718HG = 0x6e  # PCM-3718HG
    BD_PCI1716 = 0x74  # PCI-1716
    BD_PCI1731 = 0x75  # PCI-1731
    BD_PCI1754 = 0x7b  # PCI-1754
    BD_PCI1752 = 0x7c  # PCI-1752
    BD_PCI1756 = 0x7d  # PCI-1756
    BD_PCM3725 = 0x7f  # PCM-3725
    BD_PCI1762 = 0x80  # PCI-1762
    BD_PCI1721 = 0x81  # PCI-1721
    BD_PCI1761 = 0x82  # PCI-1761
    BD_PCI1723 = 0x83  # PCI-1723
    BD_PCI1730 = 0x87  # PCI-1730
    BD_PCI1733 = 0x88  # PCI-1733
    BD_PCI1734 = 0x89  # PCI-1734
    BD_PCI1710L = 0x90  # PCI-1710L
    BD_PCI1710HGL = 0x91  # PCI-1710HGL
    BD_PCM3712 = 0x93  # PCM-3712
    BD_PCM3723 = 0x94  # PCM-3723
    BD_PCI1780 = 0x95  # PCI-1780
    BD_MIC3756 = 0x96  # MIC-3756
    BD_PCI1755 = 0x97  # PCI-1755
    BD_PCI1714 = 0x98  # PCI-1714
    BD_PCI1757 = 0x99  # PCI-1757
    BD_MIC3716 = 0x9A  # MIC-3716
    BD_MIC3761 = 0x9B  # MIC-3761
    BD_MIC3753 = 0x9C  # MIC-3753
    BD_MIC3780 = 0x9D  # MIC-3780
    BD_PCI1724 = 0x9E  # PCI-1724
    BD_PCI1758UDI = 0xA3  # PCI-1758UDI
    BD_PCI1758UDO = 0xA4  # PCI-1758UDO
    BD_PCI1747 = 0xA5  # PCI-1747
    BD_PCM3780 = 0xA6  # PCM-3780
    BD_MIC3747 = 0xA7  # MIC-3747
    BD_PCI1758UDIO = 0xA8  # PCI-1758UDIO
    BD_PCI1712L = 0xA9  # PCI-1712L
    BD_PCI1763UP = 0xAC  # PCI-1763UP
    BD_PCI1736UP = 0xAD  # PCI-1736UP
    BD_PCI1714UL = 0xAE  # PCI-1714UL
    BD_MIC3714 = 0xAF  # MIC-3714
    BD_PCM3718HO = 0xB1  # PCM-3718HO
    BD_PCI1741U = 0xB3  # PCI-1741U
    BD_MIC3723 = 0xB4  # MIC-3723
    BD_PCI1718HDU = 0xB5  # PCI-1718HDU
    BD_MIC3758DIO = 0xB6  # MIC-3758DIO
    BD_PCI1727U = 0xB7  # PCI-1727U
    BD_PCI1718HGU = 0xB8  # PCI-1718HGU
    BD_PCI1715U = 0xB9  # PCI-1715U
    BD_PCI1716L = 0xBA  # PCI-1716L
    BD_PCI1735U = 0xBB  # PCI-1735U
    BD_USB4711 = 0xBC  # USB4711
    BD_PCI1737U = 0xBD  # PCI-1737U
    BD_PCI1739U = 0xBE  # PCI-1739U
    BD_PCI1742U = 0xC0  # PCI-1742U
    BD_USB4718 = 0xC6  # USB-4718
    BD_MIC3755 = 0xC7  # MIC3755
    BD_USB4761 = 0xC8  # USB4761
    BD_PCI1784 = 0XCC  # PCI-1784
    BD_USB4716 = 0xCD  # USB4716
    BD_PCI1752U = 0xCE  # PCI-1752U
    BD_PCI1752USO = 0xCF  # PCI-1752USO
    BD_USB4751 = 0xD0  # USB4751
    BD_USB4751L = 0xD1  # USB4751L
    BD_USB4750 = 0xD2  # USB4750
    BD_MIC3713 = 0xD3  # MIC-3713
    BD_USB4711A = 0xD8  # USB4711A
    BD_PCM3753P = 0xD9  # PCM3753P
    BD_PCM3784 = 0xDA  # PCM3784
    BD_PCM3761I = 0xDB  # PCM-3761I
    BD_MIC3751 = 0xDC  # MIC-3751
    BD_PCM3730I = 0xDD  # PCM-3730I
    BD_PCM3813I = 0xE0  # PCM-3813I
    BD_PCIE1744 = 0xE1  # PCIE-1744
    BD_PCI1730U = 0xE2  # PCI-1730U
    BD_PCI1760U = 0xE3  # PCI-1760U
    BD_MIC3720 = 0xE4  # MIC-3720
    BD_PCM3810I = 0xE9  # PCM-3810I
    BD_USB4702 = 0xEA  # USB4702
    BD_USB4704 = 0xEB  # USB4704
    BD_PCM3810I_HG = 0xEC  # PCM-3810I_HG
    BD_PCI1713U = 0xED  # PCI-1713U

    # !!!BioDAQ only Product ID starts from here!!!
    BD_PCI1706U = 0x800
    BD_PCI1706MSU = 0x801
    BD_PCI1706UL = 0x802
    BD_PCIE1752 = 0x803
    BD_PCIE1754 = 0x804
    BD_PCIE1756 = 0x805
    BD_MIC1911 = 0x806
    BD_MIC3750 = 0x807
    BD_MIC3711 = 0x808
    BD_PCIE1730 = 0x809
    BD_PCI1710_ECU = 0x80A
    BD_PCI1720_ECU = 0x80B
    BD_PCIE1760 = 0x80C
    BD_PCIE1751 = 0x80D
    BD_ECUP1706 = 0x80E
    BD_PCIE1753 = 0x80F
    BD_PCIE1810 = 0x810
    BD_ECUP1702L = 0x811
    BD_PCIE1816 = 0x812
    BD_PCM27D24DI = 0x813
    BD_PCIE1816H = 0x814
    BD_PCIE1840 = 0x815
    BD_PCL725 = 0x816
    BD_PCI176E = 0x817
    BD_PCIE1802 = 0x818
    BD_AIISE730 = 0x819
    BD_PCIE1812 = 0x81A
    BD_MIC1810 = 0x81B
    BD_PCIE1802L = 0x81C
    BD_PCIE1813 = 0x81D
    BD_PCIE1840L = 0x81E
    BD_PCIE1730H = 0x81F
    BD_PCIE1756H = 0x820
    BD_PCIERXM01 = 0x821  # PCIe-RXM01
    BD_MIC1816 = 0x822
    BD_USB5830 = 0x823
    BD_USB5850 = 0x824
    BD_USB5860 = 0x825
    BD_VPX1172 = 0x826
    BD_USB5855 = 0x827
    BD_USB5856 = 0x828
    BD_USB5862 = 0x829
    BD_PCIE1840T = 0x82A
    BD_AudioCard = 0x82B
    BD_AIIS1750 = 0x82C
    BD_PCIE1840HL = 0x82D
    BD_PCIE1765 = 0x82E
    BD_PCIE1761H = 0x82F
    BD_PCIE1762H = 0x830
    BD_PCIE1884 = 0x831
    BD_PCIE1758DIO = 0x832
    BD_PCIE1758DI = 0x833
    BD_PCIE1758DO = 0x834

    #
    BD_USB5817 = 0x835
    BD_USB5801 = 0x836
    BD_PCM2731 = 0x837
    BD_MOS1110 = 0x838
    BD_PCIE1750UH = 0x839
    BD_PCIE1750U = 0x83A
    BD_USB5820 = 0x83B

    #
    BD_THK1710R = 0x83C
    BD_PCIE1803 = 0x83D
    BD_PCIE1824 = 0x83E
    BD_PCIE1805 = 0x83F

    #
    BD_MIOE1747 = 0x840
    BD_ECUP1710 = 0x841
    BD_PCIE1824L = 0x842

    #
    BD_PCIE1763AH = 0x843
    BD_PCIE1763DH = 0x844

    #
    BD_MIC1816B = 0x845

    #
    BD_SUSIGPIO = 0x846

    #
    BD_MIC1810B = 0x847

    # iDAQ series
    BD_IDAQ731 = 0x848
    BD_IDAQ763D = 0x849
    BD_IDAQ817 = 0x84A
    BD_IDAQ821 = 0x84B

    #
    BD_EAPIGPIO = 0x84C

    # iDAQ series
    BD_IDAQ841 = 0x84D
    BD_IDAQ801 = 0x84E

    # WISE-5000 starts from here
    BD_WISE5051 = 0x901
    BD_WISE5056 = 0x902
    BD_WISE5056SO = 0x903
    BD_WISE5015 = 0x904
    BD_WISE5017 = 0x905
    BD_WISE5018 = 0x906
    BD_WISE5024 = 0x907
    BD_WISE5080 = 0x908
    BD_WISE5074 = 0x909
    BD_WISE5001 = 0x90A
    BD_WISE5052 = 0x90B
    BD_WISE5057 = 0x90C
    BD_WISE5057SO = 0x90D
    BD_WISE5017C = 0x90E
    BD_WISE5017V = 0x90F
    BD_WISE5079 = 0x910

    BD_AMAX5051 = 0x911
    BD_AMAX5056 = 0x912
    BD_AMAX5056SO = 0x913
    BD_AMAX5015 = 0x914
    BD_AMAX5017 = 0x915
    BD_AMAX5018 = 0x916
    BD_AMAX5024 = 0x917
    BD_AMAX5080 = 0x918
    BD_AMAX5074 = 0x919
    BD_AMAX5001 = 0x91A
    BD_AMAX5052 = 0x91B
    BD_AMAX5057 = 0x91C
    BD_AMAX5057SO = 0x91D
    BD_AMAX5017C = 0x91E
    BD_AMAX5017V = 0x91F
    BD_AMAX5079 = 0x920

    # Unknown productId
    BD_UNKNOWN = -1


class ControlState(IntEnum):
    Idle = 0
    Ready = 1
    Running = 2
    Stopped = 3
    Uninited = -1


class Scenario(IntEnum):
    SceInstantAi = 1 << 0
    SceBufferedAi = 1 << 1
    SceWaveformAi = 1 << 2
    SceInstantAo = 1 << 3
    SceBufferedAo = 1 << 4
    SceInstantDi = 1 << 5
    SceInstantDo = 1 << 6
    SceEventCounter = 1 << 7
    SceFreqMeter = 1 << 8
    SceOneShot = 1 << 9
    SceTimerPulse = 1 << 10
    ScePwMeter = 1 << 11
    ScePwModulator = 1 << 12
    SceUdCounter = 1 << 13
    SceBufferedEventCounter = 1 << 14
    SceBufferedPwMeter = 1 << 15
    SceBufferedPwModulator = 1 << 16
    SceBufferedUdCounter = 1 << 17
    SceEdgeSeparation = 1 << 18
    SceBufferedDi = 1 << 19
    SceBufferedDo = 1 << 20
    SceCalibration = 1 << 21


class MathInterval(Structure):
    _fields_ = [
        ('Type', c_int32),
        ('Min', c_double),
        ('Max', c_double)
    ]


class MapFuncPiece(Structure):
    _fields_ = [
        ("Size", c_int32),          # the size of structure
        ("Degree", c_int32),        # the polynomial degree
        ("UpperLimit", c_double),   # the upper limit for this scaling polynomial
        ("Coef", c_double * 2)      # variable length array for the coefficient of polynomial, in increasing degree
    ]


class DataMark(Structure):
    _fields_ = [
        ("DataIndex", c_int64),
        ("SrcId", c_int32),
        ("_reserved_", c_int32)
    ]


class DeviceInformation(Structure):
    _fields_ = [
        ("DeviceNumber", c_int32),
        ("DeviceMode", c_int32),  # AccessMode
        ("ModuleIndex", c_int32),
        ("Description", c_wchar * MAX_DEVICE_DESC_LEN)
    ]

    def __init__(self,  Description='', DeviceNumber=-1, DeviceMode=AccessMode.ModeWrite, ModuleIndex=0):
        self.DeviceNumber = DeviceNumber
        self.DeviceMode = DeviceMode
        self.ModuleIndex = ModuleIndex
        self.Description = Description


class DeviceTreeNode(Structure):
    _fields_ = [
        ("DevicIntEnumber", c_int32),
        ("ModulesIndex", c_int32 * 8),
        ("Description", c_wchar * MAX_DEVICE_DESC_LEN)
    ]


class DeviceEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32)  # EventId
    ]


class BfdAiEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
        ("MarkCount", c_int32)
    ]


class BfdAoEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32)
    ]


class DiSnapEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("SrcNum", c_int32),
        ("Length", c_int32),
        ("PortData", c_uint8 * MAX_DIO_PORT_COUNT)
    ]


class BfdDiEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
        ("MarkCount", c_int32)
    ]


class BfdDoEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32)
    ]


class CntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),   # EventId
        ("Channel", c_int32)
    ]


class UdCntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Length", c_int32),
        ("Data", c_int32 * MAX_CNTR_CH_COUNT)
    ]


class BfdCntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),   # EventId
        ("Channel", c_int32),
        ("Offset", c_int32),
        ("Count", c_int32)
    ]


class PulseWidth(Structure):
    _fields_ = [
        ("HiPeriod", c_double),
        ("LoPeriod", c_double)
    ]

