# -*- coding: utf-8 -*-
# pysantec/tests/instruments/test_daq_instrument.py

"""
DAQ instrument tests.
"""

import time

import pytest

import pysantec

# This is a pytest fixture that sets up the DAQ instrument for testing.
DAQ_DEVICE_NAME = "Dev1"  # Replace with your actual DAQ device name


@pytest.fixture(scope="module")
def daq():
    """Fixture to create and yield a DAQ instrument instance."""
    daq = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective device name
        daq = instrument_manager.connect_daq(DAQ_DEVICE_NAME)
    except Exception as e:
        pytest.skip(f"Cannot connect to DAQ: {e}")
    yield daq


def test_idn(daq):
    """Test the IDN property of the DAQ instrument."""
    idn = daq.idn
    print(f"DAQ IDN: {idn}")
    assert "Dev" in idn


def test_is_sampling(daq):
    """Test the is_sampling property of the DAQ instrument."""
    is_sampling = daq.is_sampling
    assert isinstance(is_sampling, bool)


def test_device_id(daq):
    """Test the get_devices method of the DAQ instrument."""
    devices = daq.get_devices()
    print(f"DAQ Devices: {devices}")
    assert devices is not None


def test_logging_error_code(daq):
    """Test the logging_error_code property of the DAQ instrument."""
    error_code = daq.logging_error_code
    print(f"Logging Error Code: {error_code}")
    assert isinstance(error_code, int)


def test_is_connected(daq):
    """Test the is_connected property of the DAQ instrument."""
    is_connected = daq.is_connected
    assert isinstance(is_connected, bool)
    # assert is_connected is True


@pytest.mark.parametrize("value", [1.05, 2, 2.5])
def test_time_coefficient(daq, value):
    """Test setting and getting the time coefficient."""
    daq.set_time_coefficient(value)
    result = daq.get_time_coefficient()
    print(f"Time Coefficient - Set: {value}, Get: {result}")
    assert result == value


@pytest.mark.parametrize("value", [1, 5, 10])
def test_averaging_time(daq, value):
    """Test setting and getting the averaging time."""
    daq.set_averaging_time(value)
    result = daq.get_averaging_time()
    print(f"Averaging Time - Set: {value}, Get: {result}")
    assert result == value


@pytest.mark.parametrize("value", [1.0, 2.0, 5.0])
def test_add_time_coefficient(daq, value):
    """Test setting and getting the Add Time Coefficient."""
    daq.set_add_time_coefficient(value)
    result = daq.get_add_time_coefficient()
    print(f"Add Time Coefficient - Set: {value}, Get: {result}")
    assert result == value


@pytest.mark.parametrize("value", [2, 5, 10])
def test_meas_sampling_time(daq, value):
    """Test setting and getting the Measurement Sampling Time."""
    daq.set_meas_sampling_time(value)
    result = daq.get_meas_sampling_time()
    print(f"Measurement Sampling Time - Set: {value}, Get: {result}")
    assert result == value


def test_set_sampling_parameters(daq):
    """Test the set_sampling_parameters method of the DAQ instrument."""
    # Test sampling parameters
    params = {
        "start_wavelength": 1260.0,
        "stop_wavelength": 1360.0,
        "speed": 1,
        "tsl_actual_step": 0.1,
    }
    daq.set_sampling_parameters(**params)
    time.sleep(0.5)  # Allow time for parameters to be set


# def test_get_sampling_data(daq):
#     """Test the sampling data retrieval method of the DAQ instrument."""
#     trigger, monitor = daq.get_sampling_data()
#     print(f"Sampling Data - Trigger points: {len(trigger)}, "
#           f"Monitor points: {len(monitor)}")
#     assert isinstance(trigger, (list, tuple))
#     assert isinstance(monitor, (list, tuple))
#
#
# def test_get_sampling_raw_data(daq):
#     """Test the sampling raw data retrieval method of the DAQ instrument."""
#     raw_trigger, raw_monitor = daq.get_sampling_raw_data()
#     print(f"Raw Sampling Data - Trigger points: {len(raw_trigger)}, "
#           f"Monitor points: {len(raw_monitor)}")
#     assert isinstance(raw_trigger, (list, tuple))
#     assert isinstance(raw_monitor, (list, tuple))
