"""
TSL Instrument Enums.
"""

from enum import Enum
from ..santec_wrapper import TSL


class LDStatus(Enum):
    """Enum for Laser Diode (LD) Status of the TSL instrument."""

    OFF = TSL.LD_Status.LD_OFF
    ON = TSL.LD_Status.LD_ON


class ShutterStatus(Enum):
    """Enum for Shutter Status of the TSL instrument."""

    OPEN = TSL.Shutter_Status.Shutter_Open
    CLOSE = TSL.Shutter_Status.Shutter_Close


class ScanMode(Enum):
    """Enum for Scan Modes of the TSL instrument."""

    STEPPED_ONE_WAY = TSL.Sweep_Mode.Step_Oneway
    CONTINUOUS_ONE_WAY = TSL.Sweep_Mode.Continuous_Oneway
    STEPPED_TWO_WAY = TSL.Sweep_Mode.Step_Twoway
    CONTINUOUS_TWO_WAY = TSL.Sweep_Mode.Continuous_Twoway


class ScanStatus(Enum):
    """Enum for Scan Status of the TSL instrument."""

    STANDBY = TSL.Sweep_Status.Standby
    RUNNING = TSL.Sweep_Status.Running
    PAUSE = TSL.Sweep_Status.Pausing
    STANDING_BY_TRIGGER = TSL.Sweep_Status.WaitingforTrigger
    PREPARATION_FOR_SWEEP_START = TSL.Sweep_Status.Returning


class TriggerOutputMode(Enum):
    """Enum for Trigger Output Modes of the TSL instrument."""

    NONE = getattr(TSL.Trigger_Output_Mode, "None")
    STOP = TSL.Trigger_Output_Mode.Stop
    START = TSL.Trigger_Output_Mode.Start
    STEP = TSL.Trigger_Output_Mode.Step


class TriggerInputMode(Enum):
    """Enum for Trigger Input Modes of the TSL instrument."""

    DISABLE = TSL.Trigger_Input_Mode.Disable
    ENABLE = TSL.Trigger_Input_Mode.Enable


class ScanStartMode(Enum):
    """Enum for Scan Start Modes of the TSL instrument."""

    NORMAL = TSL.Sweep_Start_Mode.Normal
    WAITING_FOR_TRIGGER = TSL.Sweep_Start_Mode.WaitingforTrigger


class PowerUnit(Enum):
    """Enum for Power Units of the TSL instrument."""

    dBm = TSL.Power_Unit.dBm
    mW = TSL.Power_Unit.mW


class WavelengthUnit(Enum):
    """Enum for Wavelength Units of the TSL instrument."""

    nm = TSL.Wavelength_Unit.nm
    THz = TSL.Wavelength_Unit.THz


class PowerMode(Enum):
    """Enum for Power mode of the TSL instrument."""

    AutoCurrentControl = TSL.Power_Mode.ACC
    AutoPowerControl = TSL.Power_Mode.APC


class TriggerOutputSetting(Enum):
    """Enum for Trigger output source of the TSL instrument."""

    WAVELENGTH = TSL.TriggerOut_Source.Wavelength
    TIME = TSL.TriggerOut_Source.Time


class CoherenceControlStatus(Enum):
    """Enum for Coherence Control Status of the TSL instrument."""

    OFF = TSL.Coh_Status.Coh_OFF
    ON = TSL.Coh_Status.Coh_ON


class GPIBDelimiter(Enum):
    """Enum for GPIB Command Delimiter of the TSL instrument."""

    CR = 0
    LF = 1
    CRLF = 2
    NONE = 3
