"""
TSL instrument module.
"""

from ..logger import get_logger
from .base_instrument import BaseInstrument
from .wrapper import TSL
from .wrapper.enumerations.tsl_enums import (
    LDStatus,
    PowerUnit,
    ScanStatus,
    ScanStartMode,
    ScanMode,
    WavelengthUnit,
    PowerMode,
    ShutterStatus,
    GPIBDelimiter,
    TriggerOutputSetting,
    TriggerOutputMode,
    TriggerInputMode,
)


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
        self.logger.debug("Setting default power unit to dBm.")
        self.set_power_unit(PowerUnit.dBm)

    # region Get methods
    def get_system_error(self):
        """Get the system error from the TSL instrument."""
        system_error = self._get_function("Get_System_Error", "")
        self.logger.debug(f"System error: {system_error}")
        return system_error

    def get_power_unit(self) -> PowerUnit:
        """Get the current power unit setting."""
        power_unit = self._get_function_enum("Get_Power_Unit", PowerUnit.dBm)
        self.logger.debug(f"Current power unit: {power_unit}.")
        return power_unit

    def get_wavelength_unit(self) -> WavelengthUnit:
        """Get the current wavelength unit setting."""
        wavelength_unit = self._get_function_enum(
            "Get_Wavelength_Unit", WavelengthUnit.nm
        )
        self.logger.debug(f"Current wavelength unit: {wavelength_unit}.")
        return wavelength_unit

    def get_power_mode(self) -> PowerMode:
        """Get the current power mode setting."""
        power_mode = self._get_function_enum(
            "Get_Power_Mode", PowerMode.AutoCurrentControl
        )
        self.logger.debug(f"Current power mode: {power_mode}.")
        return power_mode

    def get_ld_status(self) -> LDStatus:
        """Get the current status of the laser diode."""
        ld_status = self._get_function_enum("Get_LD_Status", LDStatus.OFF)
        self.logger.debug(f"Current LD status: {ld_status}.")
        return ld_status

    def get_scan_start_mode(self) -> ScanStartMode:
        """Get the current scan start mode."""
        scan_start_mode = self._get_function_enum(
            "Get_Sweep_Start_Mode", ScanStartMode.NORMAL
        )
        self.logger.debug(f"Current scan start mode: {scan_start_mode}.")
        return scan_start_mode

    def get_scan_status(self) -> ScanStatus:
        """Get the current scan status of the TSL instrument."""
        scan_status = self._get_function_enum("Get_Sweep_Status", ScanStatus.PAUSE)
        self.logger.debug(f"Current sweep status: {scan_status}.")
        return scan_status

    def get_scan_mode(self) -> ScanMode:
        """Get the current scan mode."""
        scan_mode = self._get_function_enum("Get_Sweep_Mode", ScanMode.STEPPED_ONE_WAY)
        self.logger.debug(f"Current scan mode: {scan_mode}.")
        return scan_mode

    def get_shutter_status(self) -> ShutterStatus:
        """Get the current shutter status."""
        shutter_status = self._get_function_enum(
            "Get_Shutter_Status", ShutterStatus.OPEN
        )
        self.logger.debug(f"Current shutter status: {shutter_status}.")
        return shutter_status

    def get_power(self) -> float:
        """Get the current power setting in dBm."""
        power_value = self._get_function("Get_Setting_Power_dBm", float)
        self.logger.debug(f"Current power setting: {power_value} dBm.")
        return power_value

    def get_wavelength(self) -> float:
        """Get the current wavelength setting in nm."""
        wavelength_value = self._get_function("Get_Wavelength", float)
        self.logger.debug(f"Current wavelength setting: {wavelength_value} nm.")
        return wavelength_value

    def get_speed(self) -> float:
        """Get the current speed setting in nm/sec."""
        speed_value = self._get_function("Get_Sweep_Speed", float)
        self.logger.debug(f"Current speed setting: {speed_value} nm/sec.")
        return speed_value

    def get_step_wavelength(self) -> float:
        """Get the current step wavelength setting in nm."""
        step_wavelength = self._get_function("Get_Wavelength_Step", float)
        self.logger.debug(f"Current step wavelength setting: {step_wavelength} nm.")
        return step_wavelength

    # region Logging Data Related methods
    def get_logging_data_points(self) -> int:
        """Get the number of data points available in the logging data."""
        self.logger.info("Fetch logging data points.")
        data_points = self.query(":READ:POIN?")

        if data_points is None:
            self.logger.error(
                f"Failed to retrieve data points." f" Status: {self.status}"
            )
            return 0

        data_points = int(data_points)
        self.logger.info(f"Retrieved data points: {data_points}")

        return data_points

    def _fetch_logging_data(self, fetch_dll_func, *args):
        """Generic helper to fetch logging data with a scan lifecycle."""
        self.tsl_busy_check(2)  # Ensure TSL is not busy

        data_points = self.get_logging_data_points()

        if data_points <= 0:
            self.logger.error("No data points found.")
            return 0, None

        # Initialize data list
        data = [0.0] * data_points

        self.tsl_busy_check(2)  # Ensure TSL is not busy

        # Set the TSL start scan mode to waiting for trigger
        self.set_scan_start_mode(ScanStartMode.WAITING_FOR_TRIGGER)
        self.start_scan()

        try:
            result = getattr(self._instrument, fetch_dll_func)(*args, 0, data)

        finally:
            self.stop_scan()  # Stop TSL process
            pass

        if not result or any(r is None for r in result if r is not None):
            self.logger.error("Failed to retrieve logging data.")
            return 0, None

        status, data_points, data = result

        if data_points:
            self.logger.info(
                f"Retrieved logging data points: {data_points}."
                f" Status: {self.status}."
                f" Received data length: {len(data)}."
            )

        if not isinstance(data, list):
            data = list(data)

        return data

    def get_wavelength_logging_data(self):
        """Get the wavelength logging data."""
        self.logger.info("Fetch the wavelength logging data.")

        return self._fetch_logging_data("Get_Logging_Data")

    def get_power_logging_data(
        self, speed: float = None, step_wavelength: float = None
    ):
        """
        Get the power monitor data.

        Speed in nm/sec.
        Step wavelength in nm.
        """
        self.logger.info(f"Fetch power logging data.")

        if not speed:
            speed = self.get_speed()

        if not step_wavelength:
            step_wavelength = self.get_step_wavelength()

        self.logger.info(f"Speed value: {speed}. Step wavelength: {step_wavelength}")

        return self._fetch_logging_data(
            "Get_Logging_Data_Power_for_STS",
            speed,
            step_wavelength,
        )

    # endregion
    # endregion

    # region Set methods
    def set_power_unit(self, unit: PowerUnit):
        """Set the power unit for the TSL instrument."""
        self.logger.info(f"Setting power unit to {unit.name}.")
        self._set_function_enum("Set_Power_Unit", unit)

    def set_wavelength_unit(self, unit: WavelengthUnit):
        """Set the wavelength unit for the TSL instrument."""
        self.logger.info(f"Setting wavelength unit to {unit.name}.")
        self._set_function_enum("Set_Wavelength_Unit", unit)

    def set_power_mode(self, unit: PowerMode):
        """Set the power mode for the TSL instrument."""
        self.logger.info(f"Setting power mode to {unit.name}.")
        self._set_function_enum("Set_Power_Mode", unit)

    def set_ld_status(self, status: LDStatus):
        """Set the laser diode status."""
        self.logger.info(f"Setting LD status to {status.name}.")
        self._set_function_enum("Set_LD_Status", status)

    def set_scan_start_mode(self, mode: ScanStartMode):
        """Set the scan start mode."""
        self.logger.info(f"Setting Sweep Start Mode to {mode.name}.")
        self._set_function_enum("Set_Sweep_Start_Mode", mode)

    def set_trigger_output_setting(self, mode: TriggerOutputSetting):
        """Set the trigger output setting."""
        self.logger.info(f"Setting Trigger Output Setting to {mode.name}.")
        self._set_function_enum("Set_TriggerOutput_Source", mode)

    def set_trigger_input_mode(self, mode: TriggerInputMode):
        """
        Set the external trigger input setting.
        Enables / Disables external trigger input.
        """
        self.logger.info(f"Setting Trigger Input Mode to {mode.name}.")
        self._set_function_enum("Set_Input_Trigger_Mode", mode)

    def set_trigger_output_mode(self, mode: TriggerOutputMode):
        """
        Set the trigger output setting.
        Sets the timing of the trigger signal output.
        """
        self.logger.info(f"Setting Trigger Output Mode to {mode.name}.")
        self._set_function_enum("Set_Trigger_Output_Mode", mode)

    def set_scan_mode(self, mode: ScanMode):
        """Set the scan mode."""
        self.logger.info(f"Setting Sweep Mode to {mode.name}.")
        self._set_function_enum("Set_Sweep_Mode", mode)

    def set_shutter_status(self, mode: ShutterStatus):
        """Set the shutter status."""
        self.logger.info(f"Setting Shutter Status to {mode.name}.")
        self._set_function_enum("Set_Shutter_Status", mode)

    def set_power(self, value: float):
        """Set the power in dBm."""
        self.logger.info(f"Setting power to {value} dBm.")
        self._set_function("Set_APC_Power_dBm", value)

    def set_wavelength(self, value: float):
        """Set the wavelength in nm."""
        self.logger.info(f"Setting wavelength to {value} nm.")
        self._set_function("Set_Wavelength", value)

    def set_speed(self, value: float):
        """Set the speed in nm/sec."""
        self.logger.info(f"Setting speed to {value} nm/sec.")
        self._set_function("Set_Sweep_Speed", value)

    def set_step_wavelength(self, value: float):
        """Set the step wavelength in nm."""
        self.logger.info(f"Setting step wavelength to {value} nm.")
        self._set_function("Set_Wavelength_Step", value)

    # region Scan Related methods
    def set_scan_parameters(
        self,
        start_wavelength: float,
        stop_wavelength: float,
        step_wavelength: float,
        scan_speed: float,
    ) -> float:
        """Set the scan parameters for the TSL instrument
        and return the actual step wavelength."""
        self.logger.info(
            f"Setting scan parameters: "
            f"Start Wavelength: {start_wavelength} nm, "
            f"Stop Wavelength: {stop_wavelength} nm, "
            f"Step Wavelength: {step_wavelength} nm, "
            f"Scan Speed: {scan_speed} nm/s."
        )
        actual_step = self._set_and_get_function(
            "Set_Sweep_Parameter_for_STS",
            start_wavelength,
            stop_wavelength,
            scan_speed,
            step_wavelength,
            0.0,
        )
        self.logger.info(
            f"Scan parameters set successfully. TSL actual step: {actual_step} nm."
        )
        return actual_step

    def start_scan(self):
        """Start the scan on the TSL instrument."""
        self.logger.info("Starting scan.")
        self._set_function("Sweep_Start")

    def stop_scan(self):
        """Stop the scan on the TSL instrument."""
        self.logger.info("Stopping scan.")
        self._set_function("Sweep_Stop")

    def soft_trigger(self):
        """Send a software trigger to the TSL instrument."""
        self.logger.info("Sending software trigger.")
        self._set_function("Set_Software_Trigger")

    def wait_for_scan_status(self, wait_time: int, scan_status: ScanStatus):
        """Wait for the scan status to change to the specified status."""
        self.logger.info(
            f"Waiting for scan status: {scan_status.name} " f"for {wait_time} seconds."
        )
        self._set_function("Waiting_For_Sweep_Status", wait_time, scan_status.value)

    def pause_scan(self):
        """Pause the scan on the TSL instrument."""
        self.logger.info("Pausing scan.")
        self._set_function("Sweep_Pause")

    def restart_scan(self):
        """Restart the scan on the TSL instrument."""
        self.logger.info("Restarting scan.")
        self._set_function("Sweep_Restart")

    # endregion
    # endregion

    # region TSL specific methods
    def tsl_busy_check(self, wait_time: int):
        """Check if the TSL instrument is busy
        and wait for it to become available."""
        self.logger.info(f"Checking if TSL is busy, waiting for {wait_time} seconds.")
        # This function will wait for the TSL instrument to become available
        self._set_function("TSL_Busy_Check", wait_time)

    def status_clear(self):
        """Status clear."""
        self.logger.info("Clearing status.")
        self.write("*CLS")  # Status Clear

    def device_reset(self):
        """Device reset."""
        self.logger.info("Resetting device.")
        self.write("*RST")  # Device Reset

    def operation_query(self):
        """Queries the completion of operation."""
        operation_query = self.query("*OPC?")
        self.logger.info(f"Operation query result: {operation_query}")
        return operation_query

    def set_command_mode(self, is_scpi: bool = False):
        """Sets command mode to Legacy / SCPI."""
        if is_scpi:
            self.logger.info(f"Setting command mode to SCPI.")
            self.write("SYST:COMM:COD 1")  # Sets the command set to SCPI.
        else:
            self.logger.info(f"Setting command mode to Legacy.")
            self.write("SYST:COMM:COD 0")  # Sets the command set to Legacy.

    def set_gpib_command_delimiter(self, delimiter: GPIBDelimiter):
        """Sets the GPIB command delimiter."""
        delimiter_value = delimiter.value
        self.logger.info(f"Setting GPIB command delimiter to {delimiter}.")
        self.write(f"SYST:COMM:GPIB:DEL {delimiter_value}")

    # endregion
