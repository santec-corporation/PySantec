"""
TSL instrument module.
"""

from .wrapper import TSL
from .base_instrument import BaseInstrument
from .wrapper.enumerations.tsl_enums import PowerUnit, LDStatus


class TSLInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = TSL()

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