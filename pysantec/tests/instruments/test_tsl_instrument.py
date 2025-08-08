"""
TSL instrument tests.
"""
import time
import pytest
import pysantec
from pysantec.instruments.wrapper.enumerations.tsl_enums import PowerUnit, LDStatus, SweepStatus


# TSL Model Type Boolean
O_BAND = True
ES_BAND = False
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
    tsl = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective resource name
        tsl = instrument_manager.connect_tsl('GPIB2::1::INSTR')
    except Exception as e:
        pytest.skip(f"Cannot connect to TSL: {e}")
    yield tsl


def test_idn(tsl):
    idn = tsl.idn
    print(f"TSL IDN: {idn}")
    assert "TSL" in idn


@pytest.mark.parametrize("status", [LDStatus.ON, LDStatus.OFF])
def test_ld_status(tsl, status):
    tsl.set_ld_status(status)
    time.sleep(0.5)
    ld_status = tsl.get_ld_status()
    print(f"Set LD Status: {status}, Get: {ld_status}")
    assert ld_status == status


def test_get_power_unit(tsl):
    power_unit = tsl.get_power_unit()
    print(f"Power Unit: {power_unit}")
    assert power_unit in [PowerUnit.dBm, PowerUnit.mW]


def test_get_sweep_status(tsl):
    sweep_status = tsl.get_sweep_status()
    print(f"Sweep Status: {sweep_status}")
    assert sweep_status in [SweepStatus.STANDBY, SweepStatus.RUNNING, SweepStatus.PAUSE,
                                    SweepStatus.STANDING_BY_TRIGGER, SweepStatus.PREPARATION_FOR_SWEEP_START]


@pytest.mark.parametrize("power", [-5, 0, 2, 5])
def test_power(tsl, power):
    tsl.set_power(power)
    time.sleep(0.5)
    get_power = tsl.get_power()
    print(f"Set Power: {power}, Get: {get_power}")
    assert get_power == power


@pytest.mark.parametrize("wavelength", WAVELENGTHS)
def test_wavelength(tsl, wavelength):
    tsl.set_wavelength(wavelength)
    time.sleep(0.5)
    get_wavelength = tsl.get_wavelength()
    print(f"Set Wavelength: {wavelength}, Get: {get_wavelength}")
    assert get_wavelength == wavelength


def test_wavelength_logging_data(tsl):
    data_points, data = tsl.get_wavelength_logging_data()
    if not data:
        pytest.fail("Wavelength Data is empty.")
    print(f"Data Points: {data_points}, Data: {len(data)}")
    assert data_points == len(data)
