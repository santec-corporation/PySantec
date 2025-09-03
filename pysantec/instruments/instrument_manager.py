"""
Instrument Manager module.
"""

from typing import Dict
from ..logger import get_logger
from .base_instrument import BaseInstrument
from .daq_instrument import DAQInstrument
from .mpm_instrument import MPMInstrument
from .tsl_instrument import TSLInstrument
from .wrapper import InstrumentWrapper
from .wrapper.enumerations.connection_enums import ConnectionType, GPIBType, Terminator


class InstrumentManager:
    """Main instrument manager for device detection and connection"""

    def __init__(self):
        """Initializes the InstrumentManager."""
        self._resources = []
        self.logger = get_logger(self.__class__.__name__)
        self._instrument_wrapper = InstrumentWrapper(self.logger)
        self._instrument: BaseInstrument | None = None
        self._connected_instruments: Dict[str, BaseInstrument] = {}
        self._resources_listed: bool = False
        self.logger.info("Initializing Instrument Manager...")

    # region Private methods
    def _list_resources(self):
        """Lists all available resources."""
        if not self._resources_listed:
            self.logger.info("Listing all available resources...")
            self._resources.clear()
            try:
                self._list_gpib_resources()
                self._list_usb_resources()
                self._list_daq_resources()

                self._resources_listed = True

            except Exception as e:
                error_string = f"Error while listing resources: {e}"
                self.logger.error(error_string)
                raise Exception(error_string)

    def _list_gpib_resources(self):
        """Lists GPIB resources."""
        self.logger.info("Listing VISA GPIB resources...")

        try:
            gpib_resources = self._instrument_wrapper.get_gpib_resources()
            if gpib_resources:
                self._resources.extend(gpib_resources)

        except Exception as e:
            self.logger.error(f"Error listing VISA GPIB resources: {e}")

    def _list_usb_resources(self):
        """Lists FTDI USB resources."""
        self.logger.info("Listing FTDI USB resources...")
        try:
            usb_resources = self._instrument_wrapper.get_usb_resources()
            if usb_resources:
                self._resources.extend(usb_resources)
        except Exception as e:
            self.logger.error(f"Error listing FTDI USB resources: {e}")

    def _list_daq_resources(self):
        """Lists NI DAQ devices."""
        self.logger.info("Listing NI DAQ resources...")
        try:
            daq_devices = self._instrument_wrapper.get_daq_devices()
            if daq_devices:
                self._resources.extend(daq_devices)
        except Exception as e:
            self.logger.error(f"Error listing NI DAQ resources: {e}")

    def _list_serial_port_resources(self):
        """Lists Serial Port devices."""
        self.logger.info("Listing Serial Port resources...")
        try:
            serial_port_devices = self._instrument_wrapper.get_serial_ports()
            if serial_port_devices:
                self._resources.extend(serial_port_devices)
        except Exception as e:
            self.logger.error(f"Error listing Serial Port resources: {e}")

    def _connect(self, resource_name, terminator: Terminator = Terminator.CRLF):
        """Connects to the specified resource."""
        connection_type = None
        if resource_name in self._connected_instruments.keys():
            raise Exception(f"Resource {resource_name} already connected.")

        if "TCPIP" in resource_name.upper():
            connection_type = ConnectionType.TCPIP
            self._resources.append(resource_name)

        if len(self._resources) < 1:
            raise Exception(f"No resources available: {len(self._resources)}")

        if resource_name not in self._resources:
            self.logger.error(f"Try to connect invalid resource: {resource_name}")
            raise Exception(f"Invalid resource: {resource_name}")

        if not connection_type:
            connection_type = self._get_connection_type(resource_name)

        self._establish_connection(resource_name, connection_type, terminator)
        if not self._instrument:
            raise Exception(f"Failed to connect: {resource_name}")

        self._connected_instruments[resource_name] = self._instrument

        return self._instrument

    def _establish_connection(
        self,
        resource_name: str,
        connection_type: ConnectionType,
        terminator: Terminator,
    ):
        """Establishes a connection to the specified resource."""
        self.logger.info(
            f"Establishing connection to {resource_name} "
            f"of type {connection_type.name}..."
        )
        match connection_type:
            case ConnectionType.GPIB:
                self._gpib_connection(resource_name, terminator)
            case ConnectionType.USB:
                self._usb_connection(resource_name)
            case ConnectionType.TCPIP:
                self._tcpip_connection(resource_name, terminator)
            case ConnectionType.DEV:
                self._dev_connection(resource_name)
            case ConnectionType.NULL:
                raise Exception(f"Invalid connection type: {connection_type}")

    def _gpib_connection(self, resource_name, terminator):
        """Establishes a GPIB connection."""
        self.logger.info(f"Connecting to GPIB resource: {resource_name}")
        gpib_board, gpib_address, _ = resource_name.split("::")  # GPIB0::10::INSTR
        gpib_board = gpib_board[-1]
        self._instrument_wrapper.connect_gpib(
            self._instrument,
            int(gpib_board),
            int(gpib_address),
            GPIBType.NI4882,
            terminator,
        )

    def _usb_connection(self, resource_name):
        """Establishes a USB connection."""
        self.logger.info(f"Connecting to USB resource: {resource_name}")
        # usb_device_id = 1  # TODO: Refactor the usb device ID assignment
        raise NotImplementedError("USB connection is yet to be implemented.")

    def _tcpip_connection(self, resource_name, terminator):
        """Establishes a TCPIP connection."""
        self.logger.info(f"Connecting to TCPIP resource: {resource_name}")
        _, ip_address, port_number, _ = resource_name.split(
            "::"
        )  # TCPIP0::192.168.10.101::5000::SOCKET
        self._instrument_wrapper.connect_tcpip(
            self._instrument, str(ip_address), int(port_number), terminator
        )

    def _dev_connection(self, resource_name):
        """Establishes a connection to a NI DAQ device."""
        self.logger.info(f"Connecting to NI DAQ resource: {resource_name}")
        self._instrument_wrapper.connect_daq(self._instrument, resource_name)  # Dev1

    @staticmethod
    def _get_connection_type(resource_name):
        """Determines the connection type based on the resource name."""
        resource_name = resource_name.upper()
        if "GPIB" in resource_name:
            return ConnectionType.GPIB
        elif "TSL" in resource_name:
            return ConnectionType.USB
        elif "DEV" in resource_name:
            return ConnectionType.DEV
        return ConnectionType.NULL

    # endregion

    def list_resources(self) -> list:
        """
        List all available devices.

        :return: List of GPIB, FTDI USB & NI DAQ resources.
        """
        self._list_resources()
        resources = self._resources
        if len(resources) < 1:
            self.logger.debug(f"No resources available: {len(resources)}")
            return []

        self.logger.info(f"Found {len(resources)} resources")
        return resources

    def connect_tsl(self, resource_name: str) -> TSLInstrument | BaseInstrument:
        """Connects to a TSL instrument."""
        self._list_resources()
        if not resource_name:
            raise ValueError("Resource name cannot be empty.")
        self.logger.info(f"Connecting to TSL resource: {resource_name}")
        terminator = Terminator.CR
        self._instrument = TSLInstrument()
        return self._connect(resource_name, terminator)

    def connect_mpm(self, resource_name: str) -> MPMInstrument | BaseInstrument:
        """Connects to an MPM instrument."""
        self._list_resources()
        if not resource_name:
            raise ValueError("Resource name cannot be empty.")
        self.logger.info(f"Connecting to MPM resource: {resource_name}")
        terminator = Terminator.LF
        self._instrument = MPMInstrument()
        return self._connect(resource_name, terminator)

    def connect_daq(self, device_name: str) -> DAQInstrument | BaseInstrument:
        """Connects to a NI DAQ device."""
        self._list_resources()
        if not device_name:
            raise ValueError("Device name cannot be empty.")
        self.logger.info(f"Connecting to NI DAQ device: {device_name}")
        self._instrument = DAQInstrument()
        return self._connect(device_name)
