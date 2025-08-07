"""
TSL Instrument Enums.
"""

from enum import Enum
from ..santec_wrapper import TSL


class LDStatus(Enum):
    OFF = TSL.LD_Status.LD_OFF
    ON = TSL.LD_Status.LD_ON


class ShutterStatus(Enum):
    OPEN = TSL.Shutter_Status.Shutter_Open
    CLOSE = TSL.Shutter_Status.Shutter_Close


class SweepMode(Enum):
    STEPPED_ONE_WAY = TSL.Sweep_Mode.Step_Oneway
    CONTINUOUS_ONE_WAY = TSL.Sweep_Mode.Continuous_Oneway
    STEPPED_TWO_WAY = TSL.Sweep_Mode.Step_Twoway
    CONTINUOUS_TWO_WAY = TSL.Sweep_Mode.Continuous_Twoway


class SweepStatus(Enum):
    STANDBY = TSL.Sweep_Status.Standby
    RUNNING = TSL.Sweep_Status.Running
    PAUSE = TSL.Sweep_Status.Pausing
    STANDING_BY_TRIGGER = TSL.Sweep_Status.WaitingforTrigger
    PREPARATION_FOR_SWEEP_START = TSL.Sweep_Status.Returning


class TriggerOutputMode(Enum):
    NONE = getattr(TSL.Trigger_Output_Mode, 'None')
    STOP = TSL.Trigger_Output_Mode.Stop
    START = TSL.Trigger_Output_Mode.Start
    STEP = TSL.Trigger_Output_Mode.Step


class TriggerInputMode(Enum):
    DISABLE = TSL.Trigger_Input_Mode.Disable
    ENABLE = TSL.Trigger_Input_Mode.Enable


class SweepStartMode(Enum):
    NORMAL = TSL.Sweep_Start_Mode.Normal
    WAITING_FOR_TRIGGER = TSL.Sweep_Start_Mode.WaitingforTrigger


class PowerUnit(Enum):
    dBm = TSL.Power_Unit.dBm
    mW = TSL.Power_Unit.mW
