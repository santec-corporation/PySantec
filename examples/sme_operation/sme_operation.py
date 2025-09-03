"""
SME - Single Measurement mode operation.

Supported Instruments
TSL series and MPM series.

Supported Communication modes
GPIB and TCPIP.
"""

# Import the PySantec package
import pysantec
from pysantec.instruments import TSLInstrument, MPMInstrument


def fetch_scan_data(mpm: MPMInstrument, module_no: int, channel_no: int):
    """Fetches and returns logged data from the MPM."""
    try:
        count = mpm.get_logging_data_point()
        print("\nLogging Data Points: ", count)

        # Fetch the channel logging data
        data = mpm.get_channel_logging_data(module_no, channel_no)
        return data

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []


def main(tsl: TSLInstrument, mpm: MPMInstrument):
    """Main workflow to initialize, configure, and perform the sweep."""
    # Create an instance and initialize SME class
    sme = pysantec.SME(tsl, mpm)

    # Collect user inputs
    power = float(input("Input output power: "))
    start_wavelength = float(input("Input start wavelength: "))
    stop_wavelength = float(input("Input stop wavelength: "))
    speed = float(input("Input scan speed: "))
    step = float(input("Input step wavelength: "))

    # Configure TSL and MPM parameters
    tsl_actual_step = sme.configure_tsl(
        start_wavelength, stop_wavelength, step, power, speed
    )
    sme.configure_mpm(
        start_wavelength,
        stop_wavelength,
        step,
        speed,
        tsl_actual_step,
        is_mpm_215=False,
    )  # Set is_mpm_215 to True if using MPM-215 module

    input("\nPress any key to start to the scan process.")

    # Perform sweep
    # Set display_logging_status True to print the MPM logging status
    sme.perform_scan(display_logging_status=False)

    # Fetch the MPM channel logging data
    # Prompt user for module and channel numbers
    user_input = input(
        "\nEnter the module and channel number to fetch data from (e.g., 0,1): "
    )
    module_no, channel_no = map(int, user_input.split(","))

    data = fetch_scan_data(mpm, module_no, channel_no)
    # print(data)
    print("Scan data length: ", len(data))


if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    im = pysantec.InstrumentManager()
    # print(im.list_resources())

    # Connect to the TSL and MPM instruments
    tsl_instrument = im.connect_tsl("GPIB2::3::INSTR")
    mpm_instrument = im.connect_mpm("GPIB2::15::INSTR")

    # Execute the main function
    main(tsl_instrument, mpm_instrument)
