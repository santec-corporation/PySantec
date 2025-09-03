# pysantec/tests/connection/test_gpib_connection.py

"""
Test GPIB connection.

Supported Instruments
- TSL: 550, 570, 710, 770
- MPM: 200, 210, 210H, 220
"""

import pytest
import pysantec

# Define GPIB resource strings for the instruments
TSL_GPIB_RESOURCE = "GPIB2::3::INSTR"
MPM_GPIB_RESOURCE = "GPIB2::15::INSTR"


@pytest.fixture(scope="module")
def instrument_manager():
    """Fixture to create an InstrumentManager instance."""
    return pysantec.InstrumentManager()


def test_tsl_gpib_connection(instrument_manager):
    """Test TSL GPIB connection."""
    tsl_instrument = instrument_manager.connect_tsl(TSL_GPIB_RESOURCE)
    assert tsl_instrument is not None
    idn = tsl_instrument.idn
    print(f"TSL IDN: {idn}")
    assert "TSL" in idn


def test_mpm_gpib_connection(instrument_manager):
    """Test MPM GPIB connection."""
    mpm_instrument = instrument_manager.connect_mpm(MPM_GPIB_RESOURCE)
    assert mpm_instrument is not None
    idn = mpm_instrument.idn
    print(f"MPM IDN: {idn}")
    assert "MPM" in idn
