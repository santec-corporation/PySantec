# pysantec/tests/instrument_logging/test_mpm_channel_logging.py

"""
Integration test for MPM channel logging data.
"""

import pytest
import pysantec
from pysantec.instruments import MPMInstrument


# Default GPIB/TCPIP resource string
MPM_RESOURCE = "GPIB2::15::INSTR"
MPM_MODULE_NUMBER = 1
MPM_CHANNEL_NUMBER = 1


@pytest.fixture(scope="module")
def mpm():
    """Fixture to connect to an MPM instrument."""
    mpm = None

    im = pysantec.InstrumentManager()

    try:
        mpm = im.connect_mpm(MPM_RESOURCE)
    except Exception as e:
        pytest.skip(f"Skipping test: MPM not available ({e})")

    yield mpm

    # Cleanup after test
    if mpm:
        mpm.disconnect()


def test_mpm_channel_logging_data(mpm: MPMInstrument):
    """Verify MPM channel logging data is retrieved correctly."""
    count = mpm.get_logging_data_point()
    assert count > 0, "Expected at least one logging data point"

    data = mpm.get_channel_logging_data(MPM_MODULE_NUMBER, MPM_CHANNEL_NUMBER)
    assert isinstance(data, (list, tuple)), "Channel data must be a list or tuple"
    assert len(data) > 0, "Expected at least one data point from channel logging"

    assert len(data) == count, "Data length should match logging data points"
