"""
MPM instrument module.
"""

from .wrapper import MPM
from ..logger import get_logger
from .base_instrument import BaseInstrument
from .wrapper.enumerations.mpm_enums import RangeMode, PowerUnit, MeasurementMode, TriggerInputMode, LoggingStatus


class MPMInstrument(BaseInstrument):
    """MPM Instrument class for controlling and monitoring the MPM device."""
    def __init__(self):
        """Initialize the MPM instrument."""
        super().__init__()
        self._instrument = MPM()
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initializing MPM Instrument...")

    # region Get Methods
    def get_range_mode(self) -> RangeMode:
        """Get the current range mode of the MPM instrument."""
        return self._get_function_enum('Get_READ_Range_Mode', RangeMode.AUTO)

    def get_power_unit(self) -> PowerUnit:
        """Get the current power unit setting of the MPM instrument."""
        return self._get_function_enum('Get_Unit', PowerUnit.dBm)

    def get_measurement_mode(self) -> MeasurementMode:
        """Get the current measurement mode of the MPM instrument."""
        return self._get_function_enum('Get_Mode', MeasurementMode.FREERUN)

    def get_trigger_input_mode(self) -> TriggerInputMode:
        """Get the current trigger input mode of the MPM instrument."""
        return self._get_function_enum('Get_Trigger_Input_Mode', TriggerInputMode.INTERNAL)

    def get_range_value(self) -> int:
        """Get the current dynamic range value of the MPM instrument."""
        return self._get_function('Get_Range', int)

    def get_averaging_time(self) -> float:
        """Get the current averaging time setting of the MPM instrument."""
        return self._get_function('Get_Averaging_Time', float)

    def get_wavelength(self) -> float:
        """Get the current wavelength setting of the MPM instrument."""
        return self._get_function('Get_Wavelength', float)

    def get_module_measurement_mode(self, module_number: int):
        """Get the measurement mode for a specific module."""
        return self._set_and_get_function_enum('Get_Mode_Each_Module',
                                               MeasurementMode, module_number, MeasurementMode.FREERUN.value)

    def get_channel_range(self, module_number: int, channel_number: int):
        """Get the range value for a specific channel in a module."""
        return self._set_and_get_function('Get_Range_Each_Channel',
                                   module_number, channel_number, response_type= int)

    def get_sweep_speed(self):
        """Get the current sweep speed setting of the MPM instrument."""
        return self._get_function('Get_Sweep_Speed', float)

    def get_logging_data_point(self):
        """Get the number of logging data points configured in the MPM instrument."""
        return self._get_function('Get_Logging_Data_Point', int)

    def get_logging_status(self):
        """Get the current logging status of the MPM instrument."""
        status, count = self._get_multiple_responses('Get_Logging_Status', int, int)
        logging_status = LoggingStatus(status)
        if logging_status == LoggingStatus.COMPLETED:
            self.logger.info("Logging is completed.")
        elif logging_status == LoggingStatus.STOPPED:
            self.logger.info("Logging is stopped.")
        elif logging_status == LoggingStatus.LOGGING:
            self.logger.info(f"Logging is running with {count} data points.")
        self.logger.debug(f"Logging status: {logging_status}, Count: {count}")
        return logging_status, count

    def get_module_logging_data(self, module_number: int):
        """Get the logging data for a specific module."""
        return self._set_and_get_function('Get_Each_Module_Loggdata',
                                          module_number, response_type=None)

    def get_channel_logging_data(self, module_number: int, channel_number: int):
        """Get the logging data for a specific channel in a module."""
        return self._set_and_get_function('Get_Each_Channel_Logdata',
                                          module_number, channel_number, response_type=None)
    # endregion

    # region Set Methods
    def set_range_mode(self, range_mode: RangeMode):
        """Set the dynamic range mode of the MPM instrument."""
        self.logger.info(f"Setting range mode to: {range_mode.name}")
        self._set_function_enum('Set_READ_Range_Mode', range_mode)

    def set_power_unit(self, power_unit: PowerUnit):
        """Set the power unit for the MPM instrument."""
        self.logger.info(f"Setting power unit to: {power_unit.name}")
        self._set_function_enum('Set_Unit', power_unit)

    def set_measurement_mode(self, measurement_mode: MeasurementMode):
        """Set the measurement mode of the MPM instrument."""
        self.logger.info(f"Setting measurement mode to: {measurement_mode.name}")
        self._set_function_enum('Set_Mode', measurement_mode)

    def set_trigger_input_mode(self, mode: TriggerInputMode):
        """Set the trigger input mode of the MPM instrument."""
        self.logger.info(f"Setting trigger input mode to: {mode.name}")
        self._set_function_enum('Set_Trigger_Input_Mode', mode)

    def set_range_value(self, value: int):
        """Set the dynamic range value of the MPM instrument."""
        self.logger.info(f"Setting range value to: {value}")
        if value < 0:
            self.logger.error("Range value must be a non-negative integer.")
            raise ValueError("Range value must be a non-negative integer.")
        elif value > 5:
            self.logger.error("Range value must be less than or equal to 5.")
            raise ValueError("Range value must be less than or equal to 5.")
        self._set_function('Set_Range', value)

    def set_averaging_time(self, value: float):
        """Set the averaging time for the MPM instrument."""
        self.logger.info(f"Setting averaging time to: {value} seconds")
        if value < 0.0:
            self.logger.error("Averaging time must be a non-negative float.")
            raise ValueError("Averaging time must be a non-negative float.")
        elif value > 100.0:
            self.logger.error("Averaging time must be less than or equal to 100 seconds.")
            raise ValueError("Averaging time must be less than or equal to 100 seconds.")
        self._set_function('Set_Averaging_Time', value)

    def set_wavelength(self, value: float):
        """Set the wavelength for the MPM instrument."""
        self.logger.info(f"Setting wavelength to: {value} nm")
        self._set_function('Set_Wavelength', value)

    def set_module_measurement_mode(self, module_number: int, mode: MeasurementMode):
        """Set the measurement mode for a specific module."""
        self.logger.info(f"Setting measurement mode for module {module_number} to: {mode.name}")
        self._set_function('Set_Mode_Each_Module', module_number, mode.value)

    def set_channel_range(self, module_number: int, channel_number: int, range_value: int):
        """Set the range value for a specific channel in a module."""
        self.logger.info(f"Setting range for module {module_number}, channel {channel_number}")
        self._set_function('Set_Range_Each_Channel', module_number, channel_number, range_value)

    def set_sweep_speed(self, speed: float):
        """Set the sweep speed for the MPM instrument."""
        self.logger.info(f"Setting sweep speed to: {speed} nm/s")
        self._set_function('Set_Sweep_Speed', speed)

    def set_logging_data_point(self, data_points: int):
        """Set the number of logging data points for the MPM instrument."""
        self.logger.info(f"Setting logging data points to: {data_points}")
        if data_points < 1:
            self.logger.error("Logging data points must be a positive integer.")
            raise ValueError("Logging data points must be a positive integer.")
        elif data_points > 1000001:
            self.logger.error("Logging data points must be less than or equal to 1000001.")
            raise ValueError("Logging data points must be less than or equal to 1000001.")
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
        """Set the scan parameters for the MPM instrument."""
        self.logger.info(f"Setting scan parameters: Start Wavelength: {start_wavelength} nm, "
                         f"Stop Wavelength: {stop_wavelength} nm, "
                         f"Step Wavelength: {step_wavelength} nm, "
                         f"Scan Speed: {scan_speed} nm/s, "
                         f"TSL Actual Step: {tsl_actual_step} nm, "
                         f"Mode: {mode.name}")
        self._set_function('Set_Logging_Paremeter_for_STS',
                                   start_wavelength,
                                   stop_wavelength,
                                   step_wavelength,
                                   tsl_actual_step,
                                   scan_speed,
                                   mode.value)

    def start_logging(self):
        """Start the logging process on the MPM instrument."""
        self.logger.info("Starting logging process.")
        self._set_function('Logging_Start')

    def stop_logging(self):
        """Stop the logging process on the MPM instrument."""
        self.logger.info("Stopping logging process.")
        self._set_function('Logging_Stop')

    def perform_zeroing(self):
        """Perform zeroing on the MPM instrument."""
        self.logger.info("Performing zeroing on the MPM instrument.")
        self._set_function('Zeroing')
    # endregion
