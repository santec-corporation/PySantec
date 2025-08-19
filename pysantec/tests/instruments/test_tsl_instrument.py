"""
TSL instrument tests.
"""

import time
import pytest
import pysantec
from pysantec.instruments.wrapper.enumerations.tsl_enums import PowerUnit, LDStatus, SweepStatus


# Define the resource name for the TSL instrument
TSL_RESOURCE_NAME = 'GPIB1::3::INSTR'


# TSL Model Type Boolean
O_BAND = False
ES_BAND = True
SCL_BAND = False

if O_BAND:
    WAVELENGTHS = [1260, 1285, 1300, 1360]
elif ES_BAND:
    WAVELENGTHS = [1355, 1400, 1455, 1485]
elif SCL_BAND:
    WAVELENGTHS = [1480, 1500, 1550, 1600, 1640]
else:
    WAVELENGTHS = [1500, 1550]


@pytest.fixture(scope="module")
def tsl():
    """Fixture to create a TSL instrument instance."""
    tsl = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective resource name
        tsl = instrument_manager.connect_tsl(TSL_RESOURCE_NAME)
    except Exception as e:
        pytest.skip(f"Cannot connect to TSL: {e}")
    yield tsl


def test_idn(tsl):
    """Test the IDN of the TSL instrument."""
    idn = tsl.idn
    print(f"TSL IDN: {idn}")
    assert "TSL" in idn


@pytest.mark.parametrize("status", [LDStatus.ON, LDStatus.OFF])
def test_ld_status(tsl, status):
    """Test the LD status of the TSL instrument."""
    tsl.set_ld_status(status)
    time.sleep(0.2)
    ld_status = tsl.get_ld_status()
    print(f"Set LD Status: {status}, Get: {ld_status}")
    assert ld_status == status


@pytest.mark.parametrize("unit", [PowerUnit.dBm, PowerUnit.mW])
def test_power_unit(tsl, unit):
    """Test the power unit setting and retrieval of the TSL"""
    tsl.set_power_unit(unit)
    time.sleep(0.2)
    power_unit = tsl.get_power_unit()
    print(f"Set Power Unit: {unit}, Get: {power_unit}")
    assert power_unit == unit


def test_get_sweep_status(tsl):
    """Test the sweep status retrieval of the TSL instrument."""
    sweep_status = tsl.get_sweep_status()
    print(f"Sweep Status: {sweep_status}")
    assert sweep_status in [SweepStatus.STANDBY, SweepStatus.RUNNING, SweepStatus.PAUSE,
                                    SweepStatus.STANDING_BY_TRIGGER, SweepStatus.PREPARATION_FOR_SWEEP_START]


@pytest.mark.parametrize("power", [-5, 0, 2, 5])
def test_power(tsl, power):
    """Test the power setting and retrieval of the TSL instrument."""
    tsl.set_power(power)
    time.sleep(0.2)
    get_power = tsl.get_power()
    print(f"Set Power: {power}, Get: {get_power}")
    assert get_power == power


@pytest.mark.parametrize("wavelength", WAVELENGTHS)
def test_wavelength(tsl, wavelength):
    """Test the wavelength setting and retrieval of the TSL"""
    tsl.set_wavelength(wavelength)
    time.sleep(0.2)
    get_wavelength = tsl.get_wavelength()
    print(f"Set Wavelength: {wavelength}, Get: {get_wavelength}")
    assert get_wavelength == wavelength


def test_wavelength_logging_data(tsl):
    """Test the wavelength logging data retrieval of the TSL instrument."""
    data_points, data = tsl.get_wavelength_logging_data()
    if not data:
        pytest.fail("Wavelength Data is empty.")
    print(f"Data Points: {data_points}, Data: {len(data)}")
    assert data_points == len(data)


@pytest.mark.parametrize("scan_params", [
    {
        'start_wavelength': WAVELENGTHS[0],
        'stop_wavelength': WAVELENGTHS[-1],
        'step_wavelength': 0.1,
        'scan_speed': 1.0
    },
    {
        'start_wavelength': WAVELENGTHS[0],
        'stop_wavelength': WAVELENGTHS[-1],
        'step_wavelength': 0.05,
        'scan_speed': 50.0
    }
])
def test_scan_parameters(tsl, scan_params):
    """Test the scan parameters setting of the TSL instrument."""
    actual_step = tsl.set_scan_parameters(**scan_params)
    print(f"Set Scan Parameters: {scan_params}, Actual Step: {actual_step}")
    assert actual_step > 0


@pytest.mark.parametrize("wait_time,expected_status", [
    (1, SweepStatus.STANDBY),
    (2, SweepStatus.RUNNING)
])
def test_wait_for_sweep_status(tsl, wait_time, expected_status):
    """Test waiting for a specific sweep status."""
    tsl.wait_for_sweep_status(wait_time, expected_status)
    status = tsl.get_sweep_status()
    print(f"Wait time: {wait_time}, Expected: {expected_status}, Got: {status}")
    assert status in [SweepStatus.STANDBY, SweepStatus.RUNNING, SweepStatus.PAUSE]


def test_tsl_busy_check(tsl):
    """Test the TSL busy check functionality."""
    tsl.tsl_busy_check(1)
    status = tsl.get_sweep_status()
    print(f"Status after busy check: {status}")
    assert status in [SweepStatus.STANDBY, SweepStatus.RUNNING, SweepStatus.PAUSE]


def test_system_error(tsl):
    """Test the system error retrieval functionality."""
    error = tsl.get_system_error()
    print(f"System error: {error}")
    assert isinstance(error, str)


@pytest.mark.parametrize("speed,step_wavelength", [
    (0.5, 0.1),
    (1.0, 0.05)
])
def test_power_monitor_data(tsl, speed, step_wavelength):
    """Test the power monitor data retrieval functionality."""
    data_points, data = tsl.get_power_monitor_data(speed, step_wavelength)
    print(f"Power monitor data points: {data_points}")
    assert data_points >= 0
    if data_points > 0:
        assert len(data) == data_points