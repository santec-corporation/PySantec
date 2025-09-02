# pysantec/tests/instruments/test_mpm_instrument.py

"""
MPM instrument tests.
"""

import time

import pytest

import pysantec
from pysantec.instruments.wrapper.enumerations.mpm_enums import (
    LoggingStatus, MeasurementMode, PowerUnit, RangeMode, TriggerInputMode)

# Define the resource name for the MPM instrument
MPM_RESOURCE_NAME = "GPIB1::17::INSTR"

# Define the module number for the MPM instrument
MODULE_NUMBER = 0

# Define the channel numbers for the MPM instrument
CHANNEL_NUMBER_1 = 1
CHANNEL_NUMBER_2 = 2


@pytest.fixture(scope="module")
def mpm():
    """Fixture to create and yield an MPM instrument instance."""
    mpm = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective resource name
        mpm = instrument_manager.connect_mpm(MPM_RESOURCE_NAME)
    except Exception as e:
        pytest.skip(f"Cannot connect to MPM: {e}")
    yield mpm


def test_idn(mpm):
    """Test the IDN of the MPM instrument."""
    idn = mpm.idn
    print(f"MPM IDN: {idn}")
    assert "MPM" in idn


@pytest.mark.parametrize(
    "unit", [PowerUnit.dBm, PowerUnit.mW, PowerUnit.dBmA, PowerUnit.mA]
)
def test_power_unit(mpm, unit):
    """Test setting and getting power unit."""
    mpm.set_power_unit(unit)
    power_unit = mpm.get_power_unit()
    print(f"Set Power Unit: {unit}, Get: {power_unit}")
    assert power_unit == unit


@pytest.mark.parametrize("mode", [RangeMode.AUTO, RangeMode.MANUAL])
def test_range_mode(mpm, mode):
    """Test setting and getting range mode."""
    mpm.set_range_mode(mode)
    range_mode = mpm.get_range_mode()
    print(f"Set Range Mode: {mode}, Get: {range_mode}")
    assert range_mode == mode


@pytest.mark.parametrize(
    "mode",
    [
        MeasurementMode.CONST1,
        MeasurementMode.CONST2,
        MeasurementMode.SWEEP1,
        MeasurementMode.SWEEP2,
        MeasurementMode.FREERUN,
    ],
)
def test_measurement_mode(mpm, mode):
    """Test setting and getting measurement mode."""
    mpm.set_measurement_mode(mode)
    measurement_mode = mpm.get_measurement_mode()
    print(f"Set Measurement Mode: {mode}, Get: {measurement_mode}")
    assert measurement_mode == mode


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_range_value(mpm, value):
    """Test setting and getting range value."""
    mpm.set_range_value(value)
    range_value = mpm.get_range_value()
    print(f"Set Range Value: {value}, Get: {range_value}")
    assert range_value == value


@pytest.mark.parametrize("value", [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2])
def test_averaging_time(mpm, value):
    """Test setting and getting averaging time."""
    mpm.set_averaging_time(value)
    averaging_time = mpm.get_averaging_time()
    print(f"Set Averaging Time: {value}, Get: {averaging_time}")
    assert averaging_time == value


@pytest.mark.parametrize(
    "wavelength", [1260, 1360, 1485, 1500, 1550, 1600, 1640]
)
def test_wavelength(mpm, wavelength):
    """Test setting and getting wavelength."""
    mpm.set_wavelength(wavelength)
    get_wavelength = mpm.get_wavelength()
    print(f"Set Wavelength: {wavelength}, Get: {get_wavelength}")
    assert get_wavelength == wavelength


@pytest.mark.parametrize("data_points", [1, 101, 1001, 10001, 100001])
def test_logging_data_points(mpm, data_points):
    """Test setting and getting logging data points."""
    mpm.set_logging_data_point(data_points)
    get_data_points = mpm.get_logging_data_point()
    print(f"Set Data Points: {data_points}, Get: {get_data_points}")
    assert get_data_points == data_points


@pytest.mark.parametrize(
    "mode", [TriggerInputMode.INTERNAL, TriggerInputMode.EXTERNAL]
)
def test_trigger_input_mode(mpm, mode):
    """Test setting and getting trigger input mode."""
    mpm.set_trigger_input_mode(mode)
    trigger_mode = mpm.get_trigger_input_mode()
    print(f"Set Trigger Input Mode: {mode}, Get: {trigger_mode}")
    assert trigger_mode == mode


@pytest.mark.parametrize(
    "module_number,mode",
    [
        (MODULE_NUMBER, MeasurementMode.CONST1),
        (MODULE_NUMBER, MeasurementMode.SWEEP1),
        (MODULE_NUMBER, MeasurementMode.CONST2),
        (MODULE_NUMBER, MeasurementMode.SWEEP2),
    ],
)
def test_module_measurement_mode(mpm, module_number, mode):
    """Test setting and getting measurement mode for specific modules."""
    mpm.set_module_measurement_mode(module_number, mode)
    measurement_mode = mpm.get_module_measurement_mode(module_number)
    print(
        f"Module {module_number} - Set Mode: {mode}, Get: {measurement_mode}"
    )
    assert measurement_mode == mode


@pytest.mark.parametrize(
    "module_number,channel_number,range_value",
    [
        (MODULE_NUMBER, CHANNEL_NUMBER_1, 1),
        (MODULE_NUMBER, CHANNEL_NUMBER_1, 2),
        (MODULE_NUMBER, CHANNEL_NUMBER_1, 3),
        (MODULE_NUMBER, CHANNEL_NUMBER_1, 4),
        (MODULE_NUMBER, CHANNEL_NUMBER_1, 5),
    ],
)
def test_channel_range(mpm, module_number, channel_number, range_value):
    """Test setting and getting channel range."""
    mpm.set_channel_range(module_number, channel_number, range_value)
    get_range = mpm.get_channel_range(module_number, channel_number)
    print(
        f"Module {module_number}, Channel {channel_number}"
        f" - Set Range: {range_value}, Get: {get_range}"
    )
    assert get_range == range_value


@pytest.mark.parametrize("speed", [0.1, 0.5, 1.0, 2.0, 5.0])
def test_sweep_speed(mpm, speed):
    """Test setting and getting sweep speed."""
    mpm.set_scan_speed(speed)
    get_speed = mpm.get_scan_speed()
    print(f"Set Sweep Speed: {speed}, Get: {get_speed}")
    assert get_speed == speed


def test_scan_parameters(mpm):
    params = {
        "start_wavelength": 1260.0,
        "stop_wavelength": 1360.0,
        "step_wavelength": 0.1,
        "scan_speed": 1.0,
        "tsl_actual_step": 0.1,
        "mode": MeasurementMode.SWEEP1,
    }
    mpm.set_scan_parameters(**params)
    time.sleep(2)  # Allow time for the parameters to be set
    # Note: There's no direct get method for scan parameters,
    # so we only test if the function executes without errors


def test_logging_control(mpm):
    """Test logging control methods: start, stop, and status."""
    mpm.start_logging()
    time.sleep(0.5)  # Allow some time for logging to start
    status, count = mpm.get_logging_status()
    assert status in LoggingStatus
    time.sleep(2)  # Allow some time for logging to collect data
    mpm.stop_logging()
    status, count = mpm.get_logging_status()
    assert status in LoggingStatus


@pytest.mark.parametrize(
    "module_number,channel_number",
    [(MODULE_NUMBER, CHANNEL_NUMBER_1), (MODULE_NUMBER, CHANNEL_NUMBER_2)],
)
def test_logging_data(mpm, module_number, channel_number):
    """Test logging data retrieval for modules and channels."""
    # Test module logging data
    module_data = mpm.get_module_logging_data(module_number)
    assert module_data is not None

    time.sleep(2)

    # Test channel logging data
    channel_data = mpm.get_channel_logging_data(module_number, channel_number)
    assert channel_data is not None


def test_zeroing(mpm):
    """Test zeroing functionality."""
    mpm.perform_zeroing()
    time.sleep(5)  # Wait for zeroing to complete
