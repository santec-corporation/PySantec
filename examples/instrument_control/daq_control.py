# -*- coding: utf-8 -*-

"""
DAQ instrument control example.

- Connect to a DAQ instrument.
- Control the DAQ instrument.
"""

# Import pysantec package
import pysantec

if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Connect to the instrument by passing the respective device name
    daq = instrument_manager.connect_daq("Dev1")

    # Prints the instrument Device Name
    print(daq.idn)

    # Gets the sampling state of the DAQ
    print(daq.is_sampling)

    # Starts the sampling
    daq.start_sampling()

    # Gets the sampling state of the DAQ
    print(daq.is_sampling)

    # Stops the sampling
    daq.stop_sampling()
