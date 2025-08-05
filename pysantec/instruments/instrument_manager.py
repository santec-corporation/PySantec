"""
Instrument Manager module.
"""

from typing import Dict
from ..logger import get_logger
from .tsl_instrument import TSLInstrument
from .mpm_instrument import MPMInstrument
from .daq_instrument import DAQInstrument
from .base_instrument import BaseInstrument, InstrumentType
from .instrument_wrapper import InstrumentWrapper, ConnectionType, GPIBType, Terminator


class InstrumentManager:
    """Main instrument manager for device detection and connection"""
    def __init__(self):
        self._resources = []
        self.logger = get_logger(self.__class__.__name__)
        self._instrument_wrapper = InstrumentWrapper(self.logger)
        self._instrument: BaseInstrument | DAQInstrument | None = None
        self._connected_instruments: Dict[str, BaseInstrument | DAQInstrument] = {}

        self._list_resources()

    # region Private methods
    def _list_resources(self):
        try:
            self._list_gpib_resources()
            self._list_usb_resources()
            self._list_daq_resources()

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

    def _connect(self, resource_name, instrument_type):
        connection_type = None
        if resource_name in self._connected_instruments.keys():
            raise Exception(f"Resource {resource_name} already connected.")
        if "TCPIP" in resource_name.upper():
            connection_type = ConnectionType.TCPIP
            self._resources.extend(resource_name)
        if len(self._resources) < 1:
            raise Exception(f"No resources available: {len(self._resources)}")
        if resource_name not in self._resources:
            self.logger.error(f"Try to connect invalid resource: {resource_name}")
            raise Exception(f"Invalid resource: {resource_name}")

        if not connection_type:
            connection_type = self._get_connection_type(resource_name)

        self._establish_connection(resource_name, instrument_type, connection_type)
        if not self._instrument:
            raise Exception(f"Failed to connect: {resource_name}")
        self._connected_instruments[resource_name] = self._instrument
        return self._instrument

    def _establish_connection(self,
                              resource_name: str,
                              instrument_type: InstrumentType,
                              connection_type: ConnectionType
                              ):
        terminator = Terminator.CRLF

        match instrument_type:
            case InstrumentType.TSL:
                self._instrument = TSLInstrument()
                terminator = Terminator.CR
            case InstrumentType.MPM:
                self._instrument = MPMInstrument()
                terminator = Terminator.LF
            case InstrumentType.DAQ:
                self._instrument = DAQInstrument()

        if not self._instrument:
            raise Exception(f"Invalid instrument type: {instrument_type}")

        match connection_type:
            case ConnectionType.GPIB:
                self._gpib_connection(resource_name, terminator)
            case ConnectionType.USB:
                self._usb_connection(resource_name)
            case ConnectionType.TCPIP:
                self._tcpip_connection(resource_name)
            case ConnectionType.DEV:
                self._dev_connection(resource_name)
            case ConnectionType.NULL:
                raise Exception(f"Invalid connection type: {connection_type}")

    def _gpib_connection(self, resource_name, terminator):
        gpib_board, gpib_address, _ = resource_name.split('::')   # GPIB0::10::INSTR
        gpib_board = gpib_board[-1]
        self._instrument_wrapper.connect_gpib(self._instrument, int(gpib_board), int(gpib_address), GPIBType.NI4882,
                                              ConnectionType.GPIB, terminator)

    def _usb_connection(self, resource_name):
        usb_device_id = 1  # TODO: Refactor the usb device ID assignment
        raise NotImplementedError("USB connection is yet to be implemented.")

    def _tcpip_connection(self, resource_name):
        _, ip_address, port_number, _ = resource_name.split('::')     # TCPIP0::192.168.10.101::5000::SOCKET
        raise NotImplementedError("TCPIP connection is yet to be implemented.")

    def _dev_connection(self, resource_name):
        self._instrument_wrapper.connect_daq(self._instrument, resource_name)

    @staticmethod
    def _get_connection_type(resource_name):
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
        resources = self._resources
        if len(resources) < 1:
            self.logger.debug(f"No resources available: {len(resources)}")
            return []

        self.logger.info(f"Found {len(resources)} resources")
        return resources

    def connect_tsl(self, resource_name: str):
        return self._connect(resource_name, InstrumentType.TSL)

    def connect_mpm(self, resource_name: str):
        return self._connect(resource_name, InstrumentType.MPM)

    def connect_daq(self, device_name: str) -> DAQInstrument:
        return self._connect(device_name, InstrumentType.DAQ)
