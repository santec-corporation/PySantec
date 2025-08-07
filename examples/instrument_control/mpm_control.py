# -*- coding: utf-8 -*-
"""
PySantec
MPM instrument control example.

- Connect to an MPM instrument.
- Control the MPM instrument.
"""

# Import pysantec package
import pysantec


if __name__ == '__main__':
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Connect to the instrument by passing the respective resource name
    mpm = instrument_manager.connect_mpm('TCPIP::192.168.1.161::5000::SOCKET')

    # Prints the instrument Identification
    print(mpm.idn)

    # Gets the Power unit of the MPM
    print(mpm.get_power_unit())

    # Sets the wavelength of the MPM
    mpm.set_wavelength(value=1500)

    # Gets the wavelength of the MPM
    print(mpm.get_wavelength())

