"""
STS Scan Parameters.

TSL scan parameters and validation.
MPM scan parameters and validation.
"""

from typing import List, Optional
from ..instruments import TSLInstrument, tsl_enums


# TSL speeds list (for TSL-570 & TSL-770)
tsl_speed_table = [
    1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0
]

# TSL speed against minimum resolution dictionary (for TSL-570 & TSL-770)
tsl_speed_to_minimum_resolution = {
    1.0: 0.0002,
    2.0: 0.0002,
    5.0: 0.0005,
    10.0: 0.001,
    20.0: 0.001,
    50.0: 0.0025,
    100.0: 0.005,
    200.0: 0.1,
}


class TSLParameters:
    """TSL parameters."""
    start_wavelength: float = 1260    # in nm
    stop_wavelength: float = 1640      # in nm
    step_wavelength: float = 10     # in pm
    power: float = 0.0    # in dBm
    speed: float = 10.0      # in nm/sec
    cycles: int = 1
    delay: float = 0.0    # in sec

    def validate(self, tsl: TSLInstrument) -> tuple[bool, Optional[str]]:
        tsl.set_wavelength_unit(tsl_enums.WavelengthUnit.nm)
        tsl.set_power_unit(tsl_enums.PowerUnit.dBm)

        valid = True
        errors = []

        minimum_wavelength = tsl.information.MinimunWavelength
        maximum_wavelength = tsl.information.MaximumWavelength

        if not minimum_wavelength <= self.start_wavelength <= maximum_wavelength:
            valid = False
            errors.append(f"Start wavelength is out of range ({minimum_wavelength} nm ~ {maximum_wavelength} nm)")

        if not minimum_wavelength <= self.stop_wavelength <= maximum_wavelength:
            valid = False
            errors.append(f"Stop wavelength is out of range ({minimum_wavelength} nm ~ {maximum_wavelength} nm)")

        if not valid:
            error_message = "\n".join(errors) if errors else None
            return valid, error_message

        # Convert step wavelength from pm to nm
        step_wavelength = self.step_wavelength / 1000
        wavelength_span = abs(maximum_wavelength - minimum_wavelength)
        wavelength_span = round(wavelength_span, 4)

        if "570" in tsl.product_name or "770" in tsl.product_name:
            if not self.speed in tsl_speed_table:
                valid = False
                errors.append(f"Speed is out of range ({tsl_speed_table} in nm/sec)")

            minimum_step = tsl_speed_to_minimum_resolution[self.speed]
            if not minimum_step <= step_wavelength < wavelength_span:
                valid = False
                errors.append(f"Step wavelength is out range ({minimum_step} nm ~ {wavelength_span} nm)")

        minimum_speed = tsl.information.MinimumSpeed
        maximum_speed = tsl.information.MaximumSpeed

        if not minimum_speed <= self.speed <= maximum_speed:
            valid = False
            errors.append(f"Speed is out of range ({minimum_speed} nm/sec ~ {maximum_speed} nm/sec)")

        if not 0.0001 < step_wavelength < wavelength_span:
            valid = False
            errors.append(f"Step wavelength is out range (0.0001 nm ~ {wavelength_span} nm)")

        minimum_power = tsl.information.MinimumAPCPower_dBm
        maximum_power = tsl.information.MaximumAPCPower_dBm

        if not minimum_power <= self.power <= maximum_power:
            valid = False
            errors.append(f"Power is out of range ({minimum_power} dBm ~ {maximum_power} dBm)")

        error_message = "\n".join(errors) if errors else None
        return valid, error_message


# Maximum MPM configuration count
MODULE_COUNT = 5
CHANNEL_COUNT = 4
RANGE_COUNT = 5


class ModuleParameters:
    """MPM module parameters."""
    enabled: bool = False
    enabled_channels: List[bool] = [False] * CHANNEL_COUNT
    enabled_ranges: List[bool] = [False] * RANGE_COUNT

    def is_enabled(self) -> bool:
        return self.enabled

    def validate(self, channel_count: int = CHANNEL_COUNT, range_count: int = RANGE_COUNT):
        if len(self.enabled_channels) != channel_count:
            raise ValueError(f"Enabled channels must contain exactly {channel_count} booleans.")
        if len(self.enabled_ranges) != range_count:
            raise ValueError(f"Enabled ranges must contain exactly {range_count} booleans.")


class MPMParameters:
    """MPM parameters."""
    module_count = MODULE_COUNT
    modules = [ModuleParameters() for _ in range(MODULE_COUNT)]

    # TODO: Validate MPM parameters based on the number of available modules and channels.
    def validate(self) -> tuple[bool, Optional[str]]:
        valid = True
        errors = []

        if all(not module.is_enabled() for module in self.modules):
            errors.append("All modules are disabled")
            valid = False

        for idx, module in enumerate(self.modules):
            if not module.is_enabled():
                continue  # Skip validation for disabled modules

            if not module.enabled_channels or all(not ch for ch in module.enabled_channels):
                errors.append(f"Module {idx} has no enabled channels")
                valid = False

            if not module.enabled_ranges or all(not rng for rng in module.enabled_ranges):
                errors.append(f"Module {idx} has no enabled ranges")
                valid = False

        error_message = ". ".join(errors) if errors else None
        return valid, error_message


class ScanParameters:
    """Scan parameters."""
    def __init__(self,
                 tsl_parameters: TSLParameters,
                 mpm_parameters: MPMParameters
                 ):
        self.tsl_parameters = tsl_parameters
        self.mpm_parameters = mpm_parameters

    def validate(self, tsl: TSLInstrument) -> tuple[bool, Optional[str]]:
        result = self.tsl_parameters.validate(tsl)

        if not result[0]:
            return False, result[1]

        result = self.mpm_parameters.validate()

        if not result[0]:
            return False, result[1]

        return True, None
