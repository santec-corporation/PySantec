"""
SME - Single Measurement mode operation.

Supported Communication modes
GPIB and TCPIP.
"""

# Basic Imports
import time

# Imports
from ..logger import get_logger
from ..instruments import TSLInstrument, MPMInstrument, tsl_enums, mpm_enums


class SME:
    def __init__(self, tsl: TSLInstrument, mpm: MPMInstrument):
        self.logger = get_logger(self.__class__.__name__)
        self.laser = tsl
        self.power_meter = mpm
        self.logger.info("Initialized SME process.")

    def configure_tsl(
        self,
        start_wavelength: float,
        stop_wavelength: float,
        step_wavelength: float,
        output_power: float,
        scan_speed: float,
    ):
        """Configure the TSL."""
        self.logger.info("Configuring TSL parameters.")

        # Reset and basic setup
        self.laser.status_clear()
        self.laser.device_reset()

        # Sets the command set to Legacy.
        self.laser.set_command_mode(is_scpi=False)

        # Sets the command delimiter for GPIB communication.
        self.laser.set_gpib_command_delimiter(tsl_enums.GPIBDelimiter.CR)

        # Turn on output if off
        if self.laser.get_ld_status() == tsl_enums.LDStatus.OFF:
            self.laser.set_ld_status(tsl_enums.LDStatus.ON)
            while (
                self.laser.operation_query() == 0
            ):  # Queries the completion of operation.
                time.sleep(0.5)

        # Units and mode settings
        self.laser.set_power_unit(tsl_enums.PowerUnit.dBm)  # Power in dBm
        self.laser.set_wavelength_unit(tsl_enums.WavelengthUnit.nm)  # Wavelength in nm
        self.laser.set_power_mode(
            tsl_enums.PowerMode.AutoPowerControl
        )  # Auto power control
        self.laser.set_shutter_status(tsl_enums.ShutterStatus.OPEN)  # Open shutter

        # Scan settings
        self.laser.set_power(output_power)
        actual_step = self.laser.set_scan_parameters(
            start_wavelength, stop_wavelength, step_wavelength, scan_speed
        )
        self.laser.set_wavelength(start_wavelength)

        self.logger.info(f"TSL actual step value: {actual_step}")

        # Return the TSL actual step value
        return actual_step

    def configure_mpm(
        self,
        start_wavelength: float,
        stop_wavelength: float,
        step_wavelength: float,
        scan_speed: float,
        tsl_actual_step: float,
        is_mpm_215: bool = False,
    ):
        """
        Configure the MPM.

        Parameters
            tsl_actual_step: A step value in float
                             returned after setting the TSL scan parameters.
            is_mpm_215: True if using an MPM-215 module, else False.
        """
        self.logger.info("Configuring MPM parameters.")
        self.logger.info(
            f"TSL actual step value: {tsl_actual_step}. " f"Is MPM 215: {is_mpm_215}"
        )

        # Stop any ongoing measurements
        self.power_meter.stop_logging()

        # Set the mpm power unit to dBm
        self.power_meter.set_power_unit(mpm_enums.PowerUnit.dBm)

        # Set default manual dynamic range mode
        # and select SWEEP1 measurements mode
        self.power_meter.set_range_mode(mpm_enums.RangeMode.MANUAL)
        self.power_meter.set_range_value(
            1
        )  # Sets the first dynamic range value (-30 ~ +10 dBm)
        measurement_mode = mpm_enums.MeasurementMode.SWEEP1

        # If MPM-215 module is connected, select auto dynamic range mode
        # and SWEEP2 measurements mode settings
        if is_mpm_215:
            self.power_meter.set_range_mode(mpm_enums.RangeMode.AUTO)
            measurement_mode = mpm_enums.MeasurementMode.SWEEP2

        # Trigger settings
        # Enable external trigger
        self.power_meter.set_trigger_input_mode(mpm_enums.TriggerInputMode.EXTERNAL)

        # Scan settings
        self.power_meter.set_scan_parameters(
            start_wavelength,
            stop_wavelength,
            step_wavelength,
            scan_speed,
            tsl_actual_step,
            measurement_mode,
        )

        # Force set the measurements mode if not set
        while True:
            if self.power_meter.get_measurement_mode() == measurement_mode:
                break
            self.power_meter.set_measurement_mode(measurement_mode)
        print("Set Sweep mode: ", self.power_meter.get_measurement_mode())

        # Average wavelength setting
        average_wavelength = (start_wavelength + stop_wavelength) / 2
        self.power_meter.set_wavelength(average_wavelength)

        # Set the expected read data count
        data_count = int((stop_wavelength - start_wavelength) / step_wavelength + 1)
        self.power_meter.set_logging_data_point(data_count)

    def perform_scan(self, display_logging_status: bool = False):
        """Executes the wavelength sweep and triggers measurement."""
        self.logger.info(
            f"Performing Scan. Display logging status: {display_logging_status}."
        )

        # Set TSL scan status to waiting for trigger
        self.laser.set_scan_start_mode(tsl_enums.ScanStartMode.WAITING_FOR_TRIGGER)

        print("\nStarting the SME process....\n")

        # Start MPM measurements
        self.power_meter.start_logging()

        # Start TSL scan
        self.laser.start_scan()

        # Check TSL status and force set TSL to start scan if not started
        scan_status = self.laser.get_scan_status()
        while scan_status != tsl_enums.ScanStatus.STANDING_BY_TRIGGER:
            self.laser.start_scan()
            scan_status = self.laser.get_scan_status()
            time.sleep(0.2)

        # Issue software trigger to the TSL
        self.laser.soft_trigger()

        # Start timer
        start_time = time.time()

        # Wait for measurements to complete
        while (
            self.power_meter.get_logging_status()[0] == mpm_enums.LoggingStatus.LOGGING
        ):
            # Print the MPM logging status
            if display_logging_status:
                status, count = self.power_meter.get_logging_status()
                print_string = f"Logging Status: {status.name}. Data Count: {count}"
                self.logger.debug(print_string)
                print(print_string)
            time.sleep(0.2)

        # Scan end time and calculate elapsed time
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)

        status, count = self.power_meter.get_logging_status()
        print_string = f"Logging Status: {status.name}. Total Data Count: {count}"
        self.logger.info(print_string)
        print(f"\n{print_string}")

        print_string = (
            f"SME process completed. \nScan elapsed time: {elapsed_time} seconds."
        )
        self.logger.info(print_string)
        print(f"\n{print_string}")
