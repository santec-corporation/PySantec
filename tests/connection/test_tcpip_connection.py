# pysantec/tests/connection/test_tcpip_connection.py

"""
Test TCPIP connection.

Supported Instruments
- TSL: 570, 770
- MPM: 200, 210, 210H, 220
"""

import pytest
import pysantec

# Define TCPIP resource strings for the instruments
TSL_TCPIP_RESOURCE = "GPIB2::3::INSTR"
MPM_TCPIP_RESOURCE = "GPIB2::15::INSTR"


@pytest.fixture(scope="module")
def instrument_manager():
    """Fixture to create an InstrumentManager instance."""
    return pysantec.InstrumentManager()


def test_tsl_tcpip_connection(instrument_manager):
    """Test TSL TCPIP connection."""
    tsl_instrument = instrument_manager.connect_tsl(TSL_TCPIP_RESOURCE)
    assert tsl_instrument is not None
    idn = tsl_instrument.idn
    print(f"TSL IDN: {idn}")
    assert "TSL" in idn


def test_mpm_tcpip_connection(instrument_manager):
    """Test MPM TCPIP connection."""
    mpm_instrument = instrument_manager.connect_mpm(MPM_TCPIP_RESOURCE)
    assert mpm_instrument is not None
    idn = mpm_instrument.idn
    print(f"MPM IDN: {idn}")
    assert "MPM" in idn