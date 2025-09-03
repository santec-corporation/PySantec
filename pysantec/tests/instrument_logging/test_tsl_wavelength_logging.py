# pysantec/tests/instrument_logging/test_tsl_wavelength_logging.py

"""
Integration test for TSL wavelength logging data.
"""

import time
import pytest
import pysantec
from pysantec.instruments import TSLInstrument


# Default GPIB/TCPIP resource string
TSL_RESOURCE = "GPIB2::3::INSTR"


@pytest.fixture(scope="module")
def tsl():
    """Fixture to connect to a TSL instrument."""
    tsl = None

    im = pysantec.InstrumentManager()

    try:
        tsl = im.connect_tsl(TSL_RESOURCE)
    except Exception as e:
        pytest.skip(f"Skipping test: TSL not available ({e})")

    yield tsl

    # Cleanup after test
    if tsl:
        tsl.disconnect()


def test_tsl_wavelength_logging_data(tsl: TSLInstrument):
    """Verify TSL wavelength logging returns valid data."""
    count = tsl.get_logging_data_points()
    assert count > 0, "Expected at least one logging data point"

    time.sleep(1)

    data = tsl.get_wavelength_logging_data()
    assert data is not None, "Expected data from wavelength logging"
    assert isinstance(data, list), "Data must be a list or tuple"
    assert len(data) > 0, "Wavelength logging data should not be empty"

    assert len(data) == count, "Data length should match logging data points"
