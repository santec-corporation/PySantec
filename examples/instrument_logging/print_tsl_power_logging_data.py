"""
TSL power logging data example.

- Connect to a TSL instrument.
- Prints the TSL logging data points.
- Prints the TSL power logging data.
"""

# Import pysantec package
import pysantec


if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Connect to the instrument by passing the respective resource name
    tsl = instrument_manager.connect_tsl("GPIB2::3::INSTR")

    # Print the TSL logging data points
    print(tsl.get_logging_data_points())

    # Fetch the power monitor data
    data = tsl.get_power_logging_data()
    # print(data)
    print(len(data))
