"""
DAQ instrument module.
"""

from .wrapper import DAQ
from .base_instrument import BaseInstrument


class DAQInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = DAQ()

# region Properties
    @property
    def idn(self):
        return self._instrument.DeviceName

    @property
    def is_sampling(self):
        return self._instrument.IsSampling

    @property
    def logging_error_code(self):
        return self._instrument.Logging_Errorcode

    @property
    def is_connected(self):
        return self._instrument.IsConnected
# endregion

# region Setter & Getter Methods
    def get_devices(self):
        return list(self._get_function('Get_Device_ID', None))

    # Time Coefficient
    def get_time_coefficient(self):
        return self._instrument.Time_coefficient

    def set_time_coefficient(self, value: float):
        self._instrument.Time_coefficient = value

    # Averaging Time
    def get_averaging_time(self):
        return self._instrument.AveragingTime

    def set_averaging_time(self, value: float):
        self._instrument.AveragingTime = value

    # F Additional Time
    def get_f_additional_time(self):
        return self._instrument.F_AdditonalTime

    def set_f_additional_time(self, value: float):
        self._instrument.F_AdditonalTime = value

    # Add Time Coefficient
    def get_add_time_coefficient(self):
        return self._instrument.AddTime_coefficient

    def set_add_time_coefficient(self, value: float):
        self._instrument.AddTime_coefficient = value

    # Measurement Sampling Time
    def get_meas_sampling_time(self):
        return self._instrument.Meas_Sampling_time

    def set_meas_sampling_time(self, value: float):
        self._instrument.Meas_Sampling_time = value
# endregion

# region Scan Related Methods
    def set_sampling_parameters(self,
                                start_wavelength: float,
                                stop_wavelength: float,
                                speed: int,
                                tsl_actual_step: float
                                ):
        self._set_function('Set_Sampling_Parameter',
                           start_wavelength, stop_wavelength,
                           speed, tsl_actual_step)

    def start_sampling(self):
        self._set_function('Sampling_Start')

    def wait_for_sampling(self):
        self._set_function('Waiting_for_sampling')

    def stop_sampling(self):
        self._set_function('Sampling_Stop')

    def get_sampling_data(self):
        trigger, monitor = self._get_multiple_responses('Get_Sampling_Data', None, None)
        return trigger, monitor

    def get_sampling_raw_data(self):
        trigger, monitor = self._get_multiple_responses('Get_Sampling_Rawdata', None, None)
        return trigger, monitor
# endregion
