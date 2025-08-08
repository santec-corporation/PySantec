"""
DAQ instrument tests.
"""

import pytest
import pysantec


@pytest.fixture(scope="module")
def daq():
    daq = None
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()
    try:
        # Connect to the instrument by passing the respective device name
        daq = instrument_manager.connect_daq('Dev1')
    except Exception as e:
        pytest.skip(f"Cannot connect to DAQ: {e}")
    yield daq


def test_idn(daq):
    idn = daq.idn
    print(f"DAQ IDN: {idn}")
    assert "Dev" in idn


def test_is_sampling(daq):
    is_sampling = daq.is_sampling
    assert isinstance(is_sampling, bool)

