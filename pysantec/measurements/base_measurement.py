"""
Base Measurement.
"""

import time
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

from ..logger import get_logger
from .scan_parameters import ScanParameters
from .wrapper.sts_wrapper import ReferenceInfo, MeasurementInfo, PDL_STS
from ..instruments import (TSLInstrument, MPMInstrument, DAQInstrument,
                           tsl_enums, mpm_enums)


@dataclass
class ScanData:
    mpm: MPMInstrument
    module: int
    channel: int
    dynamic_range: int
    scan_count: int
    mpm_data: List[float]
    power_monitor_data: List[float]
    sop: int = -1


@dataclass
class ILData(ScanData):
    il_data: List[float] = field(default_factory=list)


@dataclass
class ScanResult:
    error_message: str = ""
    wavelength: List[float] = field(default_factory=list)
    scan_data: List[List[ScanData]] = field(default_factory=list)


@dataclass
class ILResult(ScanResult):
    pass


@dataclass
class MeasurementData:
    # Scan Parameters
    scan_parameters: ScanParameters

    # Scan Information
    reference_info: List[ReferenceInfo]
    measurement_info: List[MeasurementInfo]

    # Properties
    tsl_actual_step: float = 0.0
    use_mpm_monitor: bool = False
    use_power_monitor: bool = False
    use_mpm_220_reference: bool = False
    is_repeat_process: bool = False

    sts: PDL_STS = PDL_STS()


class Measurement(ABC, MeasurementData):
    def __init__(self,
                 tsl: TSLInstrument,
                 mpm: MPMInstrument,
                 scan_parameters: ScanParameters,
                 daq: DAQInstrument = None,
                 use_mpm_monitor: bool = False,
                 use_power_monitor: bool = False,
                 use_mpm_220_reference: bool = False
                 ):
        self.logger = get_logger(self.__class__.__name__)
        self.tsl = tsl
        self.mpm = mpm
        self.daq = daq
        self.scan_parameters = scan_parameters
        self.use_mpm_monitor = use_mpm_monitor
        self.use_power_monitor = use_power_monitor
        self.use_mpm_220_reference = use_mpm_220_reference

    def _clear_reference_data(self):
        self.reference_info.clear()

    def _clear_measurement_data(self):
        self.measurement_info.clear()

    def _set_tsl_scan_parameters(self):
        tsl = self.tsl
        tsl_parameters = self.scan_parameters.tsl_parameters

        tsl.set_power(tsl_parameters.power)
        self.tsl_actual_step = tsl.set_scan_parameters(start_wavelength=tsl_parameters.start_wavelength,
                                                       stop_wavelength=tsl_parameters.stop_wavelength,
                                                       step_wavelength=tsl_parameters.step_wavelength,
                                                       scan_speed=tsl_parameters.speed)
        tsl.set_scan_cycles(tsl_parameters.cycles)
        tsl.set_scan_delay(tsl_parameters.delay)

    def _set_mpm_scan_parameters(self):
        pass

    def _set_daq_scan_parameters(self):
        pass

    def validate_parameters(self, parameters: ScanParameters):
        tsl_parameters = parameters.tsl_parameters
        mpm_parameters = parameters.mpm_parameters

        validation_bool, validation_errors = tsl_parameters.validate(self.tsl)
        if not validation_bool:
            for error in validation_errors:
                raise Exception(f"{error}")

        validation_bool, validation_errors = mpm_parameters.validate()
        if not validation_bool:
            for error in validation_errors:
                raise Exception(f"{error}")

    def _set_parameters(self):
        self._set_tsl_scan_parameters()
        self._set_mpm_scan_parameters()
        if self.daq:
            self._set_daq_scan_parameters()

    @abstractmethod
    def reference_scan(self):
        pass

    @abstractmethod
    def measurement_scan(self):
        pass

    def _scan_process(self):
        tsl_parameters = self.scan_parameters.tsl_parameters
        scan_time = (1100 * abs(tsl_parameters.stop_wavelength - tsl_parameters.start_wavelength)
                     / tsl_parameters.speed)
        wait_time = scan_time if scan_time > 5000 else 5000

        # Start TSL scan
        self.tsl.start_scan()

        if "770" in self.tsl.product_name:
            time.sleep(0.3)

        # Start the MPM logging
        self.mpm.start_logging()

        # Wait until the TSL is set to "Waiting for trigger" status
        self.tsl.wait_for_scan_status(3000,
                                          tsl_enums.ScanStatus.STANDING_BY_TRIGGER)

        # Start DAQ sampling
        if self.daq:
            self.daq.start_sampling()

        if "770" in self.tsl.product_name:
            time.sleep(0.3)

        self.tsl.soft_trigger()
        self.tsl.wait_for_scan_status(wait_time, tsl_enums.ScanStatus.STANDBY)

        status = mpm_enums.LoggingStatus.LOGGING
        while status != mpm_enums.LoggingStatus.COMPLETED:
            status = self.mpm.get_logging_status()[0]

        self.mpm.stop_logging()

        self.tsl.wait_for_scan_status(3000, tsl_enums.ScanStatus.STANDBY)
        self.tsl.start_scan()

    def _machine_stop_process(self):
        if self.daq.is_sampling:
            self.daq.stop_sampling()

        if not self.is_repeat_process:
            self._stop_tsl()

        self.mpm.stop_logging()


    def _stop_tsl(self):
        status = self.tsl.get_scan_status()
        if status != tsl_enums.ScanStatus.STANDBY:
            self.tsl.stop_scan()

    def load_scan_parameters(self):
        pass

    def export_scan_parameters(self):
        pass

    def import_reference_data(self):
        pass

    def export_reference_data(self):
        pass

    def export_measurement_data(self):
        pass

    def _get_reference_sampling_data(self):
        pass

    def disconnect(self):
        self.tsl.disconnect()
        self.mpm.disconnect()

        if self.daq:
            self.daq.disconnect()


class ILMeasurement(Measurement):
    def __init__(self,
                 tsl: TSLInstrument,
                 mpm: MPMInstrument,
                 scan_parameters: ScanParameters,
                 daq: DAQInstrument = None,
                 use_mpm_monitor: bool = False,
                 use_power_monitor: bool = False,
                 use_mpm_220_reference: bool = False
                 ):
        super().__init__(tsl, mpm, scan_parameters, daq,
                         use_mpm_monitor, use_power_monitor, use_mpm_220_reference)

    def reference_scan(self):
        self.validate_parameters(self.scan_parameters)

        wavelength = []
        scan_result: ILResult = ILResult(wavelength=wavelength)

        self._scan_process()

        self._get_reference_sampling_data()

        # _sts.Cal_RefData_Rescaling();

        reference_info = list(self.reference_info)
        first_reference_info = reference_info[0]

        raw_reference_data = []
        power_monitor_data = []
        #   (rawReferenceData, powerMonitorData)
        #   = _sts.Get_Ref_RawData(sts.MPM, sts.Slot, sts.Channel, sts.Range, sts.SOP, sts.SweepCount);

        raw_data: List[ILData] = [
            ILData(mpm=first_reference_info.mpm, module=0, channel=1, dynamic_range=1, scan_count=1,
                   mpm_data=raw_reference_data, power_monitor_data=power_monitor_data)]

        for sts_data in self.reference_info[1:]:
            #   (rawReferenceData, powerMonitorData)
            #   = _sts.Get_Ref_RawData(sts.MPM, sts.Slot, sts.Channel, sts.Range, sts.SOP, sts.SweepCount)
            raw_data.append(ILData(mpm=first_reference_info.mpm, module=0, channel=1, dynamic_range=1, scan_count=1,
                   mpm_data=raw_reference_data, power_monitor_data=power_monitor_data))

        scan_result.scan_data = [raw_data]
        self._machine_stop_process()
        return scan_result

    def measurement_scan(self):
        pass

