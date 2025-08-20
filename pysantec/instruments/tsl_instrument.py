"""
TSL instrument module.
"""

from .wrapper import TSL
from ..logger import get_logger
from .base_instrument import BaseInstrument
from .wrapper.enumerations.tsl_enums import PowerUnit, LDStatus, SweepStatus


class TSLInstrument(BaseInstrument):
    """TSL Instrument class for controlling TSL devices."""
    def __init__(self):
        """Initialize the TSL Instrument."""
        super().__init__()
        self._instrument = TSL()
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initializing TSL Instrument...")

        self._initialize_instrument()

    def _initialize_instrument(self):
        """Initialize the TSL instrument with default settings."""
        # Set default power unit to dBm
        self.logger.info("Setting default power unit to dBm.")
        self.set_power_unit(PowerUnit.dBm)

    # region Get methods
    def get_system_error(self):
        """Get the system error from the TSL instrument."""
        return self._get_function('Get_System_Error', "")

    def get_power_unit(self) -> PowerUnit:
        """Get the current power unit setting."""
        return self._get_function_enum('Get_Power_Unit', PowerUnit.dBm)

    def get_ld_status(self) -> LDStatus:
        """Get the current status of the laser diode."""
        return self._get_function_enum('Get_LD_Status', LDStatus.OFF)

    def get_sweep_status(self) -> SweepStatus:
        """Get the current sweep status of the TSL instrument."""
        return self._get_function_enum('Get_Sweep_Status', SweepStatus.PAUSE)

    def get_power(self) -> float:
        """Get the current power setting in dBm."""
        return self._get_function('Get_Setting_Power_dBm', float)

    def get_wavelength(self) -> float:
        """Get the current wavelength setting in nm."""
        return self._get_function('Get_Wavelength', float)

    # region Logging Data Related methods
    def get_logging_data_points(self) -> int:
        """Get the number of data points available in the logging data."""
        _, data_points = self.query(':READ:POIN?')
        if data_points is None:
            self.logger.error("Failed to retrieve data points.")
            return 0
        data_points = int(data_points)
        self.logger.info(f"Retrieved data points: {data_points}")
        return data_points

    def get_wavelength_logging_data(self):
        """Get the wavelength logging data."""
        data_points, data = self._get_multiple_responses('Get_Logging_Data',
                                                 int, None)
        if data_points is None or data is None:
            self.logger.error("Failed to retrieve wavelength logging data.")
            return 0, None
        self.logger.info(f"Retrieved {data_points} wavelength data points.")
        return data_points, data

    def get_power_monitor_data(self, speed: float, step_wavelength: float):
        """Get the power monitor data for the TSL instrument."""
        data_points, data = self._set_and_get_multiple_responses('Get_Logging_Data_Power_for_STS',
                                                                int, None,
                                                                speed, step_wavelength)
        if data_points is None or data is None:
            self.logger.error("Failed to retrieve power monitor data.")
            return 0, None
        self.logger.info(f"Retrieved {data_points} power monitor data points.")
        return data_points, data
    # endregion
    # endregion

    # region Set methods
    def set_power_unit(self, unit: PowerUnit):
        """Set the power unit for the TSL instrument."""
        self.logger.info(f"Setting power unit to {unit.name}.")
        self._set_function_enum('Set_Power_Unit', unit)

    def set_ld_status(self, status: LDStatus):
        """Set the laser diode status."""
        self.logger.info(f"Setting LD status to {status.name}.")
        self._set_function_enum('Set_LD_Status', status)

    def set_power(self, value: float):
        """Set the power in dBm."""
        self.logger.info(f"Setting power to {value} dBm.")
        self._set_function('Set_APC_Power_dBm', value)

    def set_wavelength(self, value: float):
        """Set the wavelength in nm."""
        self.logger.info(f"Setting wavelength to {value} nm.")
        self._set_function('Set_Wavelength', value)

    # region Scan Related methods
    def set_scan_parameters(self,
                            start_wavelength: float,
                            stop_wavelength: float,
                            step_wavelength: float,
                            scan_speed: float
                            ) -> float:
        """Set the scan parameters for the TSL instrument and return the actual step wavelength."""
        self.logger.info(f"Setting scan parameters: "
                         f"Start Wavelength: {start_wavelength} nm, "
                         f"Stop Wavelength: {stop_wavelength} nm, "
                         f"Step Wavelength: {step_wavelength} nm, "
                         f"Scan Speed: {scan_speed} nm/s.")
        actual_step = self._set_and_get_function('Set_Sweep_Parameter_for_STS',
                                   start_wavelength,
                                   stop_wavelength,
                                   scan_speed,
                                   step_wavelength,
                                   0.0)
        return actual_step

    def start_scan(self):
        """Start the scan on the TSL instrument."""
        self.logger.info("Starting scan.")
        self._set_function('Sweep_Start')

    def stop_scan(self):
        """Stop the scan on the TSL instrument."""
        self.logger.info("Stopping scan.")
        self._set_function('Sweep_Stop')

    def soft_trigger(self):
        """Send a software trigger to the TSL instrument."""
        self.logger.info("Sending software trigger.")
        self._set_function('Set_Software_Trigger')

    def wait_for_sweep_status(self, wait_time: int, sweep_status: SweepStatus):
        """Wait for the sweep status to change to the specified status."""
        self.logger.info(f"Waiting for sweep status: {sweep_status.name} "
                         f"for {wait_time} seconds.")
        self._set_function('Waiting_For_Sweep_Status',
                           wait_time, sweep_status.value)

    def pause_scan(self):
        """Pause the scan on the TSL instrument."""
        self.logger.info("Pausing scan.")
        self._set_function('Sweep_Pause')

    def restart_scan(self):
        """Restart the scan on the TSL instrument."""
        self.logger.info("Restarting scan.")
        self._set_function('Sweep_Restart')
    # endregion
    # endregion

    def tsl_busy_check(self, wait_time: int):
        """Check if the TSL instrument is busy and wait for it to become available."""
        self.logger.info(f"Checking if TSL is busy, waiting for {wait_time} seconds.")
        # This function will wait for the TSL instrument to become available
        self._set_function('TSL_Busy_Check', wait_time)