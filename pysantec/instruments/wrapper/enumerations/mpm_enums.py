"""
MPM Instrument Enums.
"""

from enum import Enum, IntEnum
from ..santec_wrapper import MPM


class RangeMode(Enum):
    MANUAL = MPM.READ_Range_Mode.Manual
    AUTO = MPM.READ_Range_Mode.Auto


class PowerUnit(Enum):
    dBm = MPM.Power_Unit.dBm
    mW = MPM.Power_Unit.mW
    dBmA = MPM.Power_Unit.dBmA
    mA = MPM.Power_Unit.mA


class MeasurementMode(Enum):
    CONST1 = MPM.Measurement_Mode.ManualRangeConstant
    CONST2 = MPM.Measurement_Mode.AutoRangeConstant
    SWEEP1 = MPM.Measurement_Mode.ManualRangeSweep
    SWEEP2 = MPM.Measurement_Mode.AutoRangeSweep
    FREERUN = MPM.Measurement_Mode.Freerun


class TriggerInputMode(Enum):
    INTERNAL = MPM.Trigger_Input_Mode.Internal
    EXTERNAL = MPM.Trigger_Input_Mode.Extarnal


class LoggingStatus(IntEnum):
    STOPPED = -1
    LOGGING = 0
    COMPLETED = 1
