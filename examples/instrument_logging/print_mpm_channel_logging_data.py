"""
MPM channel logging data example.

- Connect to an MPM instrument.
- Prints the MPM logging data points.
- Prints the MPM channel logging data.
"""

# Import pysantec package
import pysantec


if __name__ == "__main__":
    # Create an instance of the Instrument manager class
    instrument_manager = pysantec.InstrumentManager()

    # Connect to the instrument by passing the respective resource name
    mpm = instrument_manager.connect_mpm("GPIB2::15::INSTR")

    # Print the number of mpm logging data points
    print(mpm.get_logging_data_point())

    # Print the channel logging data
    data = mpm.get_channel_logging_data(1, 1)
    # print(data)
    print(len(data))
