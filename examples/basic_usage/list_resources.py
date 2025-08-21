# -*- coding: utf-8 -*-

"""
List resources example.

- Lists all GPIB, USB, & DAQ instruments.
"""

# Import pysantec package
import pysantec

if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Call and print the list_resources() function
    print(instrument_manager.list_resources())
