"""
Instrument Manager module.
"""

from ..logger import get_logger
from .instrument_wrapper import InstrumentWrapper


class InstrumentManager:
    """Main instrument manager for device detection and connection"""

    def __init__(self):
        self._resources = []
        self.logger = get_logger(self.__class__.__name__)
        self._instrument_wrapper = InstrumentWrapper(self.logger)

    def list_resources(self) -> list:
        """
        List all available devices.

        :return: List of GPIB, FTDI USB & NI DAQ resources.
        """
        try:
            self._list_gpib_resources()
            self._list_usb_resources()
            self._list_daq_resources()

            resources = self._resources
            if len(resources) < 1:
                self.logger.debug(f"Failed to list resources: {resources}")
                return []

            self.logger.info(f"Found {len(resources)} resources")
            return resources

        except Exception as e:
            self.logger.error(f"Error while listing resources: {e}")
            raise Exception(f"Error while listing resources: {e}")


    def _list_gpib_resources(self):
        """Lists GPIB resources."""
        try:
            gpib_resources = self._instrument_wrapper.get_gpib_resources()
            if gpib_resources:
                self._resources.extend(gpib_resources)
        except Exception as e:
            self.logger.error(f"Error listing VISA GPIB resources: {e}")

    def _list_usb_resources(self):
        """Lists FTDI USB resources."""
        try:
            usb_resources = self._instrument_wrapper.get_usb_resources()
            if usb_resources:
                self._resources.extend(usb_resources)
        except Exception as e:
            self.logger.error(f"Error listing FTDI USB resources: {e}")

    def _list_daq_resources(self):
        """Lists NI DAQ devices."""
        try:
            daq_devices = self._instrument_wrapper.get_daq_devices()
            if daq_devices:
                self._resources.extend(daq_devices)
        except Exception as e:
            self.logger.error(f"Error listing NI DAQ resources: {e}")

    def _list_serial_port_resources(self):
        """Lists Serial Port devices."""
        try:
            serial_port_devices = self._instrument_wrapper.get_serial_ports()
            if serial_port_devices:
                self._resources.extend(serial_port_devices)
        except Exception as e:
            self.logger.error(f"Error listing Serial Port resources: {e}")
