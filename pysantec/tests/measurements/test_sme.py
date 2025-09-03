# pysantec/tests/measurements/test_sme.py

"""
Integration test for SME mode operation.
"""

import pytest
import pysantec
from pysantec.instruments import TSLInstrument, MPMInstrument


# Define GPIB/TCPIP resource strings for the instruments
TSL_RESOURCE = "GPIB2::3::INSTR"
MPM_RESOURCE = "GPIB2::15::INSTR"


@pytest.fixture(scope="module")
def instruments():
    """Fixture to connect to instruments."""
    tsl = None
    mpm = None

    im = pysantec.InstrumentManager()

    try:
        tsl = im.connect_tsl(TSL_RESOURCE)
        mpm = im.connect_mpm(MPM_RESOURCE)

    except Exception as e:
        pytest.skip(f"Skipping test: instruments not available ({e})")

    yield tsl, mpm

    # Cleanup after tests
    if tsl:
        tsl.disconnect()

    if mpm:
        mpm.disconnect()


@pytest.mark.parametrize("power", [0.0])
@pytest.mark.parametrize("start_wavelength", [1355])
@pytest.mark.parametrize("stop_wavelength", [1455])
@pytest.mark.parametrize("speed", [20.0])
@pytest.mark.parametrize("step", [1.0])
@pytest.mark.parametrize("module_no", [1])
@pytest.mark.parametrize("channel_no", [1])
def test_sme_scan_and_fetch(instruments,
                            power, start_wavelength, stop_wavelength, speed, step,
                            module_no, channel_no):
    """Run a full SME scan and verify data is retrieved."""
    tsl, mpm = instruments
    sme = pysantec.SME(tsl, mpm)

    tsl_actual_step = sme.configure_tsl(
        start_wavelength, stop_wavelength, step, power, speed
    )
    sme.configure_mpm(
        start_wavelength, stop_wavelength, step, speed, tsl_actual_step,
        is_mpm_215=False,
    )

    # Perform scan (do not print status during test)
    sme.perform_scan(display_logging_status=False)

    # Fetch logged data and verify it
    count = mpm.get_logging_data_point()
    assert count > 0, "No logging data points found"

    data = mpm.get_channel_logging_data(module_no, channel_no)
    assert isinstance(data, list), "Data should be a list"
    assert len(data) > 0, "Expected at least one data point"

    assert len(data) == count, "Data length does not match logged data points"