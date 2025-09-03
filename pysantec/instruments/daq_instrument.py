"""
DAQ instrument module.
"""

from ..logger import get_logger
from .base_instrument import BaseInstrument
from .wrapper import DAQ


class DAQInstrument(BaseInstrument):
    """DAQ Instrument class for handling data acquisition operations."""

    def __init__(self):
        """Initialize the DAQ instrument."""
        super().__init__()
        self._instrument = DAQ()
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initializing DAQ Instrument...")

    # region Properties
    @property
    def idn(self):
        """Return the IDN of the instrument."""
        self.logger.info("Retrieving IDN of the DAQ Instrument...")
        return self._instrument.DeviceName

    @property
    def is_sampling(self):
        """Check if the instrument is currently sampling."""
        self.logger.debug("Checking if the DAQ Instrument is sampling...")
        return self._instrument.IsSampling

    @property
    def logging_error_code(self):
        """Return the logging error code."""
        self.logger.debug("Retrieving logging error code...")
        return self._instrument.Logging_Errorcode

    @property
    def is_connected(self):
        """Check if the instrument is connected."""
        self.logger.debug("Checking if the DAQ Instrument is connected...")
        return self._instrument.IsConnected

    # endregion

    # region Setter & Getter Methods
    def get_devices(self):
        """Get a list of connected DAQ devices."""
        device_list = list(self._get_function("Get_Device_ID", None))
        self.logger.info(f"Connected DAQ devices: {device_list}")
        return device_list

    # Time Coefficient
    def get_time_coefficient(self):
        """Get the time coefficient of the instrument."""
        time_coefficient = self._instrument.Time_coefficient
        self.logger.debug(f"Time Coefficient: {time_coefficient}")
        return time_coefficient

    def set_time_coefficient(self, value: float):
        """Set the time coefficient of the instrument."""
        self.logger.info(f"Setting Time Coefficient to {value}.")
        self._instrument.Time_coefficient = value

    # Averaging Time
    def get_averaging_time(self):
        """Get the averaging time of the instrument."""
        averaging_time = self._instrument.AveragingTime
        self.logger.debug(f"Averaging Time: {averaging_time}")
        return averaging_time

    def set_averaging_time(self, value: float):
        """Set the averaging time of the instrument."""
        self.logger.info(f"Setting Averaging Time to {value}.")
        self._instrument.AveragingTime = value

    # F Additional Time
    def get_f_additional_time(self):
        """Get the additional time factor for the instrument."""
        f_additional_time = self._instrument.F_AdditonalTime
        self.logger.debug(f"F Additional Time: {f_additional_time}")
        return f_additional_time

    def set_f_additional_time(self, value: float):
        """Set the additional time factor for the instrument."""
        self.logger.info(f"Setting Additional Time Factor to {value}.")
        self._instrument.F_AdditonalTime = value

    # Add Time Coefficient
    def get_add_time_coefficient(self):
        """Get the additional time coefficient for the instrument."""
        add_time_coefficient = self._instrument.AddTime_coefficient
        self.logger.debug(f"Add Time Coefficient: {add_time_coefficient}")
        return add_time_coefficient

    def set_add_time_coefficient(self, value: float):
        """Set the additional time coefficient for the instrument."""
        self.logger.info(f"Setting Additional Time Coefficient to {value}.")
        self._instrument.AddTime_coefficient = value

    # Measurement Sampling Time
    def get_meas_sampling_time(self):
        """Get the measurement sampling time of the instrument."""
        meas_sampling_time = self._instrument.Meas_Sampling_time
        self.logger.debug(f"Measurement Sampling Time: {meas_sampling_time}")
        return meas_sampling_time

    def set_meas_sampling_time(self, value: float):
        """Set the measurement sampling time of the instrument."""
        self.logger.info(f"Setting Measurement Sampling Time to {value}.")
        self._instrument.Meas_Sampling_time = value

    # endregion

    # region Scan Related Methods
    def set_sampling_parameters(
        self,
        start_wavelength: float,
        stop_wavelength: float,
        speed: int,
        tsl_actual_step: float,
    ):
        """Set the sampling parameters for the instrument."""
        self.logger.info(
            f"Setting Sampling Parameters: "
            f"Start Wavelength: {start_wavelength}, "
            f"Stop Wavelength: {stop_wavelength}, "
            f"Speed: {speed}, "
            f"TSL Actual Step: {tsl_actual_step}."
        )
        self._set_function(
            "Set_Sampling_Parameter",
            start_wavelength,
            stop_wavelength,
            speed,
            tsl_actual_step,
        )

    def start_sampling(self):
        """Start the sampling process."""
        self.logger.info("Starting the sampling process.")
        self._set_function("Sampling_Start")

    def wait_for_sampling(self):
        """Wait for the sampling process to complete."""
        self.logger.info("Waiting for the sampling process to complete.")
        self._set_function("Waiting_for_sampling")

    def stop_sampling(self):
        """Stop the sampling process."""
        self.logger.info("Stopping the sampling process.")
        self._set_function("Sampling_Stop")

    def get_sampling_data(self):
        """Get the sampling data from the instrument."""
        self.logger.info("Retrieving sampling data.")

        trigger, monitor = self._get_multiple_responses("Get_Sampling_Data", None, None)

        if not trigger or not monitor:
            self.logger.error("Failed to retrieve sampling data.")
            raise ValueError("No data received from the instrument.")

        if len(trigger) != len(monitor):
            self.logger.error("Mismatch in lengths of trigger and monitor data.")
            raise ValueError("Trigger and monitor data lengths do not match.")

        self.logger.info(
            f"Retrieved {len(trigger)} trigger "
            f"and {len(monitor)} monitor data points."
        )

        return trigger, monitor

    def get_sampling_raw_data(self):
        """Get the raw sampling data from the instrument."""
        self.logger.info("Retrieving raw sampling data...")

        trigger, monitor = self._get_multiple_responses(
            "Get_Sampling_Rawdata", None, None
        )

        if not trigger or not monitor:
            self.logger.error("Failed to retrieve raw sampling data.")
            raise ValueError("No raw data received from the instrument.")

        if len(trigger) != len(monitor):
            self.logger.error("Mismatch in lengths of trigger and monitor raw data.")
            raise ValueError("Trigger and monitor raw data lengths do not match.")

        self.logger.info(
            f"Retrieved {len(trigger)} trigger "
            f"and {len(monitor)} monitor raw data points."
        )

        return trigger, monitor

    # endregion
