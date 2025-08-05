# -*- coding: utf-8 -*-
"""
PySantec
Instrument connection example.

- Connect to a TSL instrument.
- Connect to an MPM instrument.
- Connect to a DAQ instrument/device.
"""

# Import pysantec package
import pysantec


if __name__ == '__main__':
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Call the instrument respective connect by passing the resource names/addresses
    tsl = instrument_manager.connect_tsl('GPIB1::3::INSTR')
    mpm = instrument_manager.connect_mpm('GPIB1::17::INSTR')
    daq = instrument_manager.connect_daq('Dev1')    # Pass the DAQ device name

    # Prints the instrument Identification
    print(tsl.idn)
    print(mpm.idn)
    print(daq.device_name)      # Prints the DAQ device name


