"""
Validate STS Scan Parameters Example.

Instruments
    TSL series.
    MPM series.
"""

import pysantec
from pysantec.measurements import TSLParameters, ModuleParameters, MPMParameters, ScanParameters

instrument_manager = pysantec.InstrumentManager()

tsl = instrument_manager.connect_tsl("GPIB0::2::INSTR")

tsl_parameters = TSLParameters()
tsl_parameters.start_wavelength = 1550.0
tsl_parameters.stop_wavelength = 1600.0
tsl_parameters.speed = 50.0
tsl_parameters.step_wavelength = 100

# print(tsl_parameters.validate(tsl))

module_parameters_1 = ModuleParameters()
module_parameters_1.enabled = True
module_parameters_1.enabled_channels = [False, True, False, False]
module_parameters_1.enabled_ranges = [False, False, True, False, False]

module_parameters_2 = ModuleParameters()
module_parameters_2.enabled = True
module_parameters_2.enabled_channels = [False, False, True, False]
module_parameters_2.enabled_ranges = [False, False, False, False, True]

mpm_parameters = MPMParameters()
mpm_parameters.modules[0] = module_parameters_1
mpm_parameters.modules[2] = module_parameters_2

# print(mpm_parameters.validate())

scan_parameters = ScanParameters(tsl_parameters, mpm_parameters)
print(scan_parameters.validate(tsl))