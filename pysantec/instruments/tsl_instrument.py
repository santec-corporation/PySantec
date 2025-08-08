"""
TSL instrument module.
"""

from .wrapper import TSL
from .base_instrument import BaseInstrument
from .wrapper.enumerations.tsl_enums import PowerUnit, LDStatus, SweepStatus


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
    def get_system_error(self):
        return self._get_function('Get_System_Error', "")

    def get_power_unit(self) -> PowerUnit:
        return self._get_function_enum('Get_Power_Unit', PowerUnit.dBm)

    def get_ld_status(self) -> LDStatus:
        return self._get_function_enum('Get_LD_Status', LDStatus.OFF)

    def get_sweep_status(self) -> SweepStatus:
        return self._get_function_enum('Get_Sweep_Status', SweepStatus.PAUSE)

    def get_power(self) -> float:
        return self._get_function('Get_Setting_Power_dBm', float)

    def get_wavelength(self) -> float:
        return self._get_function('Get_Wavelength', float)

    # region Logging Data Related methods
    def get_logging_data_points(self) -> int:
        _, data_points = self.query(':READ:POIN?')
        return int(data_points)

    def get_wavelength_logging_data(self):
        data_points, data = self._get_multiple_responses('Get_Logging_Data',
                                                 int, None)
        return data_points, data

    def get_power_monitor_data(self, speed: float, step_wavelength: float):
        data_points, data = self._set_and_get_multiple_responses('Get_Logging_Data_Power_for_STS',
                                                                int, None,
                                                                speed, step_wavelength)
        return data_points, data
    # endregion
    # endregion

    # region Set methods
    def set_ld_status(self, status: LDStatus):
        self._set_function_enum('Set_LD_Status', status)

    def set_power(self, value: float):
        self._set_function('Set_APC_Power_dBm', value)

    def set_wavelength(self, value: float):
        self._set_function('Set_Wavelength', value)

    # region Scan Related methods
    def set_scan_parameters(self,
                            start_wavelength: float,
                            stop_wavelength: float,
                            step_wavelength: float,
                            scan_speed: float
                            ) -> float:
        actual_step = self._set_and_get_function('Set_Sweep_Parameter_for_STS',
                                   start_wavelength,
                                   stop_wavelength,
                                   scan_speed,
                                   step_wavelength,
                                   0.0)
        return actual_step

    def start_scan(self):
        self._set_function('Sweep_Start')

    def stop_scan(self):
        self._set_function('Sweep_Stop')

    def soft_trigger(self):
        self._set_function('Set_Software_Trigger')

    def wait_for_sweep_status(self, wait_time: float, sweep_status: SweepStatus):
        self._set_function('Waiting_For_Sweep_Status',
                           wait_time, sweep_status)

    def pause_scan(self):
        self._set_function('Sweep_Pause')

    def restart_scan(self):
        self._set_function('Sweep_Restart')
    # endregion
    # endregion