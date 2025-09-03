# pysantec/tests/instrument_logging/test_mpm_module_logging.py

"""
Integration test for MPM module logging data.
"""

import pytest
import pysantec
from pysantec.instruments import MPMInstrument


# Default GPIB/TCPIP resource string
MPM_RESOURCE = "GPIB2::15::INSTR"
MPM_MODULE_NUMBER = 1


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


def test_mpm_module_logging_data(mpm: MPMInstrument):
    """Verify MPM module logging data is retrieved correctly."""
    count = mpm.get_logging_data_point()
    assert count > 0, "Expected at least one logging data point"

    result = mpm.get_module_logging_data(MPM_MODULE_NUMBER)
    assert isinstance(result, (list, tuple)), "Result must be a list or tuple"
    assert len(result) > 0, "Expected non-empty result from module logging data"

    first_channel_data = result[0]
    assert isinstance(
        first_channel_data, (list, tuple)
    ), "Channel data must be list or tuple"
    assert len(first_channel_data) > 0, "Expected at least one data point in channel"

    assert (
        len(first_channel_data) == count
    ), "Data length should match logging data points"
