"""
MPM instrument module.
"""

from .wrapper import MPM
from .base_instrument import BaseInstrument
from .wrapper.enumerations.mpm_enums import RangeMode, PowerUnit, MeasurementMode, TriggerInputMode, LoggingStatus


class MPMInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = MPM()

    # region Get Methods
    def get_range_mode(self) -> RangeMode:
        return self._get_function_enum('Get_READ_Range_Mode', RangeMode.AUTO)

    def get_power_unit(self) -> PowerUnit:
        return self._get_function_enum('Get_Unit', PowerUnit.dBm)

    def get_measurement_mode(self) -> MeasurementMode:
        return self._get_function_enum('Get_Mode', MeasurementMode.FREERUN)

    def get_trigger_input_mode(self) -> TriggerInputMode:
        return self._get_function_enum('Get_Trigger_Input_Mode', TriggerInputMode.INTERNAL)

    def get_range_value(self) -> int:
        return self._get_function('Get_Range', int)

    def get_averaging_time(self) -> float:
        return self._get_function('Get_Averaging_Time', float)

    def get_wavelength(self) -> float:
        return self._get_function('Get_Wavelength', float)

    def get_module_measurement_mode(self, module_number: int):
        return self._set_and_get_function_enum('Get_Mode_Each_Module',
                                               MeasurementMode, module_number, MeasurementMode.FREERUN.value)

    def get_channel_range(self, module_number: int, channel_number: int):
        return self._set_and_get_function('Get_Range_Each_Channel',
                                   module_number, channel_number, response_type= int)

    def get_sweep_speed(self):
        return self._get_function('Get_Sweep_Speed', float)

    def get_logging_data_point(self):
        return self._get_function('Get_Logging_Data_Point', int)

    def get_logging_status(self):
        status, count = self._get_multiple_responses('Get_Logging_Status', int, int)
        logging_status = LoggingStatus(status)
        return logging_status, count

    def get_module_logging_data(self, module_number: int):
        return self._set_and_get_function('Get_Each_Module_Loggdata',
                                          module_number, response_type=None)

    def get_channel_logging_data(self, module_number: int, channel_number: int):
        return self._set_and_get_function('Get_Each_Channel_Logdata',
                                          module_number, channel_number, response_type=None)
    # endregion

    # region Set Methods
    def set_range_mode(self, range_mode: RangeMode):
        self._set_function_enum('Set_READ_Range_Mode', range_mode)

    def set_power_unit(self, power_unit: PowerUnit):
        self._set_function_enum('Set_Unit', power_unit)

    def set_measurement_mode(self, measurement_mode: MeasurementMode):
        self._set_function_enum('Set_Mode', measurement_mode)

    def set_trigger_input_mode(self, mode: TriggerInputMode):
        self._set_function_enum('Set_Trigger_Input_Mode', mode)

    def set_range_value(self, value: int):
        self._set_function('Set_Range', value)

    def set_averaging_time(self, value: float):
        self._set_function('Set_Averaging_Time', value)

    def set_wavelength(self, value: float):
        self._set_function('Set_Wavelength', value)

    def set_module_measurement_mode(self, module_number: int, mode: MeasurementMode):
        self._set_function('Set_Mode_Each_Module', module_number, mode.value)

    def set_channel_range(self, module_number: int, channel_number: int, range_value: int):
        self._set_function('Set_Range_Each_Channel', module_number, channel_number, range_value)

    def set_sweep_speed(self, speed: float):
        self._set_function('Set_Sweep_Speed', speed)

    def set_logging_data_point(self, data_points: int):
        self._set_function('Set_Logging_Data_Point', data_points)
    # endregion

    # region Scan Setting methods
    def set_scan_parameters(self,
                            start_wavelength: float,
                            stop_wavelength: float,
                            step_wavelength: float,
                            scan_speed: float,
                            tsl_actual_step: float,
                            mode: MeasurementMode):
        self._set_and_get_function('Set_Logging_Paremeter_for_STS',
                                   start_wavelength,
                                   stop_wavelength,
                                   step_wavelength,
                                   tsl_actual_step,
                                   scan_speed,
                                   mode.value)

    def start_logging(self):
        self._set_function('Logging_Start')

    def stop_logging(self):
        self._set_function('Logging_Stop')

    def perform_zeroing(self):
        self._set_function('Zeroing')
    # endregion
