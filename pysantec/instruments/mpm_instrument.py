"""
MPM instrument module.
"""

from enum import Enum
from .instrument_wrapper import MPMWrapper
from .base_instrument import BaseInstrument


# region MPM Enums
class RangeMode(Enum):
    MANUAL = MPMWrapper.READ_Range_Mode.Manual
    AUTO = MPMWrapper.READ_Range_Mode.Auto

class PowerUnit(Enum):
    dBm = MPMWrapper.Power_Unit.dBm
    mW = MPMWrapper.Power_Unit.mW
    dBmA = MPMWrapper.Power_Unit.dBmA
    mA = MPMWrapper.Power_Unit.mA

class MeasurementMode(Enum):
    CONST1 = MPMWrapper.Measurement_Mode.ManualRangeConstant
    CONST2 = MPMWrapper.Measurement_Mode.AutoRangeConstant
    SWEEP1 = MPMWrapper.Measurement_Mode.ManualRangeSweep
    SWEEP2 = MPMWrapper.Measurement_Mode.AutoRangeSweep
    FREERUN = MPMWrapper.Measurement_Mode.Freerun

class TriggerInputMode(Enum):
    INTERNAL = MPMWrapper.Trigger_Input_Mode.Internal
    EXTERNAL = MPMWrapper.Trigger_Input_Mode.Extarnal
# endregion


class MPMInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = MPMWrapper()

    # region Get Methods
    def get_range_mode(self):
        range_mode = self._get_function_enum('Get_READ_Range_Mode', RangeMode.AUTO)
        return range_mode.name

    def get_power_unit(self):
        power_unit = self._get_function_enum('Get_Unit', PowerUnit.dBm)
        return power_unit.name

    def get_measurement_mode(self):
        measurement_mode = self._get_function_enum('Get_Mode', MeasurementMode.FREERUN)
        return measurement_mode.name

    def get_range_value(self):
        range_value = self._get_function('Get_Range', int)
        return range_value

    def get_averaging_time(self):
        averaging_time = self._get_function('Get_Averaging_Time', float)
        return averaging_time

    def get_wavelength(self):
        wavelength = self._get_function('Get_Wavelength', float)
        return wavelength
    # endregion

    # region Set Methods
    def set_range_mode(self, range_mode: RangeMode):
        self._set_function_enum('Set_READ_Range_Mode', range_mode)

    def set_power_unit(self, power_unit: PowerUnit):
        self._set_function_enum('Set_Unit', power_unit)

    def set_measurement_mode(self, measurement_mode: MeasurementMode):
        self._set_function_enum('Set_Mode', measurement_mode)

    def set_range_value(self, value: int):
        self._set_function('Set_Range', value)

    def set_averaging_time(self, value: float):
        self._set_function('Set_Averaging_Time', value)

    def set_wavelength(self, value: float):
        self._set_function('Set_Wavelength', value)
    # endregion
