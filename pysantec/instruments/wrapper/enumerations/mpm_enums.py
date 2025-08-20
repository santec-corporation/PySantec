"""
MPM Instrument Enums.
"""

from enum import Enum, IntEnum

from ..santec_wrapper import MPM


class RangeMode(Enum):
    """Enumeration for the dynamic range mode of the MPM instrument."""

    MANUAL = MPM.READ_Range_Mode.Manual
    AUTO = MPM.READ_Range_Mode.Auto


class PowerUnit(Enum):
    """Enumeration for the power unit used in the MPM instrument."""

    dBm = MPM.Power_Unit.dBm
    mW = MPM.Power_Unit.mW
    dBmA = MPM.Power_Unit.dBmA
    mA = MPM.Power_Unit.mA


class MeasurementMode(Enum):
    """Enumeration for the measurement mode of the MPM instrument."""

    CONST1 = MPM.Measurement_Mode.ManualRangeConstant
    CONST2 = MPM.Measurement_Mode.AutoRangeConstant
    SWEEP1 = MPM.Measurement_Mode.ManualRangeSweep
    SWEEP2 = MPM.Measurement_Mode.AutoRangeSweep
    FREERUN = MPM.Measurement_Mode.Freerun


class TriggerInputMode(Enum):
    """Enumeration for the trigger input mode of the MPM instrument."""

    INTERNAL = MPM.Trigger_Input_Mode.Internal
    EXTERNAL = MPM.Trigger_Input_Mode.Extarnal


class LoggingStatus(IntEnum):
    """Enumeration for the logging status of the MPM instrument."""

    STOPPED = -1
    LOGGING = 0
    COMPLETED = 1
