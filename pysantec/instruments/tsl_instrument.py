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

        self._set_power_unit()

    # region Private methods
    def _set_power_unit(self):
        _ = self._instrument.Set_Power_Unit(PowerUnit.dBm.value)
        self._set_function_enum('Set_Power_Unit', PowerUnit.dBm)
    # endregion

    # region Get methods
    def get_power_unit(self) -> PowerUnit:
        return self._get_function_enum('Get_Power_Unit', PowerUnit.dBm).name

    def get_ld_status(self) -> LDStatus:
        return self._get_function_enum('Get_LD_Status', LDStatus.OFF).name

    def get_power(self) -> float:
        return self._get_function('Get_Setting_Power_dBm', float)

    def get_wavelength(self) -> float:
        return self._get_function('Get_Wavelength', float)
    # endregion

    # region Set methods
    def set_ld_status(self, status: LDStatus):
        self._set_function_enum('Set_LD_Status', status)

    def set_power(self, value: float):
        self._set_function('Set_APC_Power_dBm', value)

    def set_wavelength(self, value: float):
        self._set_function('Set_Wavelength', value)
    # endregion