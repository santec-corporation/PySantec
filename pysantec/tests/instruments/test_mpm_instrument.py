"""
TSL instrument tests.
"""
import time
import pytest
import pysantec
from pysantec.instruments.wrapper.enumerations.mpm_enums import PowerUnit, RangeMode, MeasurementMode


@pytest.fixture(scope="module")
def mpm():
    mpm = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective resource name
        mpm = instrument_manager.connect_mpm('TCPIP::192.168.1.161::5000::SOCKET')
    except Exception as e:
        pytest.skip(f"Cannot connect to MPM: {e}")
    yield mpm


def test_idn(mpm):
    idn = mpm.idn
    print(f"MPM IDN: {idn}")
    assert "MPM" in idn


@pytest.mark.parametrize("unit", [PowerUnit.dBm, PowerUnit.mW, PowerUnit.dBmA, PowerUnit.mA])
def test_power_unit(mpm, unit):
    mpm.set_power_unit(unit)
    power_unit = mpm.get_power_unit()
    print(f"Set Power Unit: {unit}, Get: {power_unit}")
    assert power_unit == unit


@pytest.mark.parametrize("mode", [RangeMode.AUTO, RangeMode.MANUAL])
def test_range_mode(mpm, mode):
    mpm.set_range_mode(mode)
    range_mode = mpm.get_range_mode()
    print(f"Set Range Mode: {mode}, Get: {range_mode}")
    assert range_mode == mode


@pytest.mark.parametrize("mode", [MeasurementMode.CONST1, MeasurementMode.CONST2,
                                  MeasurementMode.SWEEP1, MeasurementMode.SWEEP2, MeasurementMode.FREERUN])
def test_measurement_mode(mpm, mode):
    mpm.set_measurement_mode(mode)
    measurement_mode = mpm.get_measurement_mode()
    print(f"Set Measurement Mode: {mode}, Get: {measurement_mode}")
    assert measurement_mode == mode


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_range_value(mpm, value):
    mpm.set_range_value(value)
    range_value = mpm.get_range_value()
    print(f"Set Range Value: {value}, Get: {range_value}")
    assert range_value == value


@pytest.mark.parametrize("value", [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2])
def test_averaging_time(mpm, value):
    mpm.set_averaging_time(value)
    averaging_time = mpm.get_averaging_time()
    print(f"Set Averaging Time: {value}, Get: {averaging_time}")
    assert averaging_time == value


@pytest.mark.parametrize("wavelength", [1260, 1360, 1485, 1500, 1550, 1600, 1640])
def test_wavelength(mpm, wavelength):
    mpm.set_wavelength(wavelength)
    get_wavelength = mpm.get_wavelength()
    print(f"Set Wavelength: {wavelength}, Get: {get_wavelength}")
    assert get_wavelength == wavelength

