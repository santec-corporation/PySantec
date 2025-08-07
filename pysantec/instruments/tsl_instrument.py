"""
TSL instrument module.
"""

from enum import Enum
from .instrument_wrapper import TSLWrapper
from .base_instrument import BaseInstrument

# region TSL Enums
class LDStatus(Enum):
    OFF = TSLWrapper.LD_Status.LD_OFF
    ON = TSLWrapper.LD_Status.LD_ON

class ShutterStatus(Enum):
    OPEN = TSLWrapper.Shutter_Status.Shutter_Open
    CLOSE = TSLWrapper.Shutter_Status.Shutter_Close

class SweepMode(Enum):
    STEPPED_ONE_WAY = TSLWrapper.Sweep_Mode.Step_Oneway
    CONTINUOUS_ONE_WAY = TSLWrapper.Sweep_Mode.Continuous_Oneway
    STEPPED_TWO_WAY = TSLWrapper.Sweep_Mode.Step_Twoway
    CONTINUOUS_TWO_WAY = TSLWrapper.Sweep_Mode.Continuous_Twoway

class SweepStatus(Enum):
    STANDBY = TSLWrapper.Sweep_Status.Standby
    RUNNING = TSLWrapper.Sweep_Status.Running
    PAUSE = TSLWrapper.Sweep_Status.Pausing
    STANDING_BY_TRIGGER = TSLWrapper.Sweep_Status.WaitingforTrigger
    PREPARATION_FOR_SWEEP_START = TSLWrapper.Sweep_Status.Returning

class TriggerOutputMode(Enum):
    NONE = getattr(TSLWrapper.Trigger_Output_Mode, 'None')
    STOP = TSLWrapper.Trigger_Output_Mode.Stop
    START = TSLWrapper.Trigger_Output_Mode.Start
    STEP = TSLWrapper.Trigger_Output_Mode.Step

class TriggerInputMode(Enum):
    DISABLE = TSLWrapper.Trigger_Input_Mode.Disable
    ENABLE = TSLWrapper.Trigger_Input_Mode.Enable

class Sweep_Start_Mode(Enum):
    NORMAL = TSLWrapper.Sweep_Start_Mode.Normal
    WAITING_FOR_TRIGGER = TSLWrapper.Sweep_Start_Mode.WaitingforTrigger

class PowerUnit(Enum):
    dBm = TSLWrapper.Power_Unit.dBm
    mW = TSLWrapper.Power_Unit.mW
# endregion


class TSLInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = TSLWrapper()

    # region Private methods
    def _set_power_unit(self):
        _ = self._instrument.Set_Power_Unit(PowerUnit.dBm.value)
        self._set_function_enum('Set_Power_Unit', PowerUnit.dBm)
    # endregion

    # region Get methods
    def get_power_unit(self):
        power_unit = self._get_function_enum('Get_Power_Unit', PowerUnit.dBm)
        return power_unit.name

    def get_ld_status(self):
        ld_status = self._get_function_enum('Get_LD_Status', LDStatus.OFF)
        return ld_status.name

    def get_power(self):
        value = self._get_function('Get_Setting_Power_dBm', float)
        return value

    def get_wavelength(self):
        value = self._get_function('Get_Wavelength', float)
        return value
    # endregion

    # region Set methods
    def set_ld_status(self, status: LDStatus):
        self._set_function_enum('Set_LD_Status', status)

    def set_power(self, value: float):
        self._set_function('Set_APC_Power_dBm', value)

    def set_wavelength(self, value: float):
        self._set_function('Set_Wavelength', value)
    # endregion