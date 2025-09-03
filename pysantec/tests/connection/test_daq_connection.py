# pysantec/tests/connection/test_daq_connection.py

"""
Test DAQ connection.

Supported Instruments
- DAQ: NI DAQ devices
"""

import pytest
import pysantec

DAQ_DEVICE_NAME = "Dev1"  # Replace with your actual DAQ device name


@pytest.fixture(scope="module")
def instrument_manager():
    """Fixture to create an InstrumentManager instance."""
    return pysantec.InstrumentManager()


def test_daq_connection(instrument_manager):
    """Test DAQ connection."""
    daq_instrument = instrument_manager.connect_daq(DAQ_DEVICE_NAME)
    assert daq_instrument is not None
    idn = daq_instrument.idn
    print(f"DAQ IDN: {idn}")
    assert "Dev" in idn