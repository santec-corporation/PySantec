"""
STS Wrapper.
"""

from typing import List
from dataclasses import dataclass

from Santec import TSL, MPM, SPU
from Santec.STSProcess import (ILSTS, PDLSTS,
                               STSDataStruct, STSDataStructForMerge,
                               RescalingMode, Module_Type)


class ReferenceInfo:
    """Reference Scan Information."""
    mpm: MPM
    sts_reference_struct: STSDataStruct
    head_power: float


class MeasurementInfo:
    """Measurement Scan Information"""
    mpm: MPM
    sts_measurement_struct: STSDataStruct


@dataclass
class IL_Data:
    target_wavelengths: List[float]


class IL_STS(ILSTS, IL_Data):
    def __init__(self):
        self._ilsts = ILSTS()

    def clear_reference_data(self):
        self._ilsts.Clear_Refdata()

    def clear_measurement_data(self):
        self._ilsts.Clear_Measdata()

    def set_freerun_spu_rescaling_setting(self, mpm_averaging_time):
        self._ilsts.Set_Rescaling_Setting(RescalingMode.Freerun_SPU,
                                          mpm_averaging_time,
                                          True)

    def set_freerun_tsl_monitor_rescaling_setting(self, mpm_averaging_time):
        self._ilsts.Set_Rescaling_Setting(RescalingMode.Freerun_TSLMonitor,
                                          mpm_averaging_time,
                                          True)

    def create_sts_wavelength_tables(self, start_wavelength, stop_wavelength, actual_step):
        self._create_sweep_wavelength_table(start_wavelength, stop_wavelength, actual_step)
        self._create_target_wavelength_table(start_wavelength, stop_wavelength, actual_step)

    def _create_sweep_wavelength_table(self, start_wavelength, stop_wavelength, actual_step):
        self._ilsts.Make_Sweep_Wavelength_Table(start_wavelength, stop_wavelength, actual_step)

    def _create_target_wavelength_table(self, start_wavelength, stop_wavelength, actual_step):
        self._ilsts.Make_Target_Wavelength_Table(start_wavelength, stop_wavelength, actual_step)

        _, self.target_wavelengths = self._ilsts.Get_Target_Wavelength_Table(None)

    def get_target_wavelength_table(self):
        return self.target_wavelengths


class PDL_STS(PDLSTS, IL_STS):
    pass
