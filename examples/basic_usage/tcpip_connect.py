"""
TCPIP connection example.

- Connect to a TSL instrument via Ethernet / LAN.
"""

# Import pysantec package
import pysantec

if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Define the resource details
    ip_address = "192.168.10.101"
    port_number = "5000"
    tcpip_resource_address = f"TCPIP::{ip_address}::{port_number}::SOCKET"

    # Connect to the instrument
    tsl = instrument_manager.connect_tsl(tcpip_resource_address)

    # Prints the instrument Identification
    print(tsl.idn)
