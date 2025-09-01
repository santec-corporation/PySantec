"""
SME - Single Measurement mode operation
with Auto Dynamic range.

Instruments
TSL series and MPM series (with MPM-215 modules).

Communication modes
GPIB and TCPIP.
"""

# Basic Imports
import time

# Import the PySantec package
from pysantec.instruments import TSLInstrument, MPMInstrument, tsl_enums, mpm_enums


def configure_tsl(tsl: TSLInstrument,
                  start_wavelength: float,
                  stop_wavelength: float,
                  step_wavelength: float,
                  output_power: float,
                  scan_speed: float):
    """Configure the TSL."""
    # Reset and basic setup
    tsl.write('*CLS')       # Status Clear
    tsl.write('*RST')       # Device Reset
    tsl.write('SYST:COMM:GPIB:DEL 0')   # Sets the command delimiter for GPIB communication.
    tsl.write('SYST:COMM:COD 0')    # Sets the command set to Legacy.

    # Turn on output if off
    if tsl.get_ld_status() == tsl_enums.LDStatus.OFF:
        tsl.set_ld_status(tsl_enums.LDStatus.ON)
        while tsl.query('*OPC?') == '0':        # Queries the completion of operation.
            time.sleep(0.5)

    # Units and mode settings
    tsl.set_power_unit(tsl_enums.PowerUnit.dBm)     # Power in dBm
    tsl.set_wavelength_unit(tsl_enums.WavelengthUnit.nm)    # Wavelength in nm
    tsl.set_power_mode(tsl_enums.PowerMode.AutoPowerControl)      # Auto power control
    tsl.set_shutter_status(tsl_enums.ShutterStatus.OPEN)  # Open shutter

    # Scan settings
    tsl.set_power(output_power)
    actual_step = tsl.set_scan_parameters(start_wavelength,
                            stop_wavelength,
                            step_wavelength,
                            scan_speed)
    tsl.set_wavelength(start_wavelength)

    return actual_step


def configure_mpm(mpm: MPMInstrument,
                  start_wavelength: float,
                  stop_wavelength: float,
                  step_wavelength: float,
                  scan_speed: float,
                  tsl_actual_step: float):
    """Configure the MPM."""
    mpm.stop_logging()  # Stop any ongoing measurement

    mpm.set_power_unit(mpm_enums.PowerUnit.dBm)

    # Dynamic range settings
    mpm.set_range_mode(mpm_enums.RangeMode.AUTO)

    # Trigger settings
    mpm.set_trigger_input_mode(mpm_enums.TriggerInputMode.EXTERNAL)    # Enable external trigger

    # Scan settings
    mpm.set_scan_parameters(start_wavelength,
                            stop_wavelength,
                            step_wavelength,
                            scan_speed,
                            tsl_actual_step,
                            mpm_enums.MeasurementMode.SWEEP2)
    while True:
        if mpm.get_measurement_mode() == mpm_enums.MeasurementMode.SWEEP2:
            break
        mpm.set_measurement_mode(mpm_enums.MeasurementMode.SWEEP2)
    print("Set Sweep mode: ", mpm.get_measurement_mode())

    # Average wavelength setting
    average_wavelength = (start_wavelength + stop_wavelength) / 2
    mpm.set_wavelength(average_wavelength)

    # Set the expected read data count
    data_count = int((stop_wavelength - start_wavelength) / step_wavelength + 1)
    mpm.set_logging_data_point(data_count)


def perform_scan(tsl: TSLInstrument,
                 mpm: MPMInstrument):
    """Executes the wavelength sweep and triggers measurement."""
    tsl.set_scan_start_mode(tsl_enums.SweepStartMode.WAITING_FOR_TRIGGER)

    input("\nPress any key to start to the scan process.")

    print("\nStarting the SME process....")

    mpm.start_logging()     # Start MPM measurement

    tsl.start_scan()

    scan_status = tsl.get_sweep_status()
    while scan_status != tsl_enums.SweepStatus.STANDING_BY_TRIGGER:
        # tsl.start_scan()
        scan_status = tsl.get_sweep_status()
        time.sleep(0.2)
    tsl.soft_trigger()

    # Scan start time
    start_time = time.time()

    # Wait for measurement to complete
    while mpm.get_logging_status()[0] == mpm_enums.LoggingStatus.LOGGING:
        # print(mpm.get_logging_status())
        time.sleep(0.2)

    # Scan end time and calculate elapsed time
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"\nSME process completed. \nScan elapsed time: {elapsed_time} seconds.")


def fetch_scan_data(mpm: MPMInstrument,
                    module_no: int,
                    channel_no: int):
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


def main(tsl: TSLInstrument,
         mpm: MPMInstrument):
    """Main workflow to initialize, configure, and perform the sweep."""
    if not tsl or not mpm:
        print("Error: Instruments not connected.")
        return

    # Collect user inputs
    power = float(input("Input output power: "))
    start_wavelength = float(input("Input start wavelength: "))
    stop_wavelength = float(input("Input stop wavelength: "))
    speed = float(input("Input scan speed: "))
    step = float(input("Input step wavelength: "))

    # Configure instruments
    tsl_actual_step = configure_tsl(tsl, start_wavelength, stop_wavelength, step, power, speed)
    configure_mpm(mpm, start_wavelength, stop_wavelength, step, speed, tsl_actual_step)

    # Perform sweep
    perform_scan(tsl, mpm)

    # Fetch the MPM channel logging data
    # Prompt user for module and channel numbers
    user_input = input("\nEnter the module and channel number to fetch data from (e.g., 0,1): ")
    module_no, channel_no = map(int, user_input.split(','))

    data = fetch_scan_data(mpm, module_no, channel_no)
    # print(data)
    print("Scan data length: ", len(data))


if __name__ == '__main__':
    import pysantec

    im = pysantec.InstrumentManager()
    # print(im.list_resources())

    tsl_instrument = im.connect_tsl("GPIB2::3::INSTR")
    mpm_instrument = im.connect_mpm("GPIB2::15::INSTR")

    main(tsl_instrument, mpm_instrument)
