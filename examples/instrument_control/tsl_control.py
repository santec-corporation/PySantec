# -*- coding: utf-8 -*-
"""
PySantec
TSL instrument control example.

- Connect to a TSL instrument.
- Control the TSL instrument.
"""

# Import pysantec package
import pysantec


if __name__ == '__main__':
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Connect to the instrument by passing the respective resource name
    tsl = instrument_manager.connect_tsl('GPIB2::1::INSTR')

    # Prints the instrument Identification
    print(tsl.idn)

    # Gets the Power unit of the TSL
    print(tsl.get_power_unit())

    # Sets the Wavelength of the TSL
    tsl.set_wavelength(value=1300)

    # Gets the Wavelength of the TSL
    print(tsl.get_wavelength())

