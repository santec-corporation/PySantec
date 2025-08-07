"""
Unified wrapper for the Santec Instrument DLL.
"""

from logging import Logger
from .santec_wrapper import DAQ
from .santec_communication_wrapper import MainCommunication
from .enumerations.connection_enums import ConnectionType, Terminator, GPIBType


class InstrumentWrapper:
    def __init__(self, logger: Logger):
        self.logger = logger.manager.getLogger(__class__.__name__)
        self._main_comm = MainCommunication()
        self._spu = DAQ()

    def get_usb_resources(self):
        resources = list(self._main_comm.Get_USB_Resouce())
        self.logger.debug(f"USB resources: {len(resources)}")
        return resources

    def get_gpib_resources(self):
        resources = list(self._main_comm.Get_GPIB_Resources())
        self.logger.debug(f"GPIB resources: {len(resources)}")
        return resources

    def get_serial_ports(self):
        resources = list(self._main_comm.Get_Serial_Port())
        self.logger.debug(f"Serial port resources: {len(resources)}")
        return resources

    def get_daq_devices(self):
        response = self._spu.Get_Device_ID(None)
        error_code, devices = response[0], list(response[1])
        self.logger.debug(f"DAQ devices: {len(devices)}")
        if error_code == -11:
            self.logger.debug("No DAQ devices connected.")
            return None
        if error_code != 0:
            self.logger.error("Error while getting DAQ devices.")
        return devices

    def connect_gpib(self, instrument_instance, gpib_board: int, gpib_address: int,
                     gpib_connect_type: GPIBType, terminator: Terminator):

        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise Exception("Could not create instrument instance.")

        instrument.GPIBBoard = gpib_board
        instrument.GPIBAddress = gpib_address
        instrument.GPIBConnectType = gpib_connect_type.value
        instrument.Terminator = terminator.value

        try:
            error_code = instrument.Connect(ConnectionType.GPIB.value)
            if error_code != 0:
                self.logger.error(f"Error while establishing GPIB connection with GPIB{gpib_board}::{gpib_address}.")

        except Exception as e:
            raise RuntimeError(f"Error while establishing GPIB connection with GPIB{gpib_board}::{gpib_address}: {e}")

    def connect_tcpip(self, instrument_instance, ip_address: str, port_number: int, terminator: Terminator):

        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise Exception("Could not create instrument instance.")

        instrument.IPAddress = ip_address
        instrument.Port = port_number
        instrument.TimeOut = 5000
        instrument.Terminator = terminator.value

        try:
            error_code = instrument.Connect(ConnectionType.TCPIP.value)
            if error_code != 0:
                self.logger.error(f"Error while establishing LAN connection with {ip_address}::{port_number}.")

        except Exception as e:
            raise RuntimeError(f"Error while establishing LAN connection with {ip_address}::{port_number}: {e}")

    def connect_daq(self, instrument_instance, device_name: str):

        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise Exception("Could not create instrument instance.")

        instrument.DeviceName = device_name

        try:
            error_code = instrument.Connect("")
            if error_code != 0:
                self.logger.error(f"Error while establishing DAQ connection with {device_name}.")

        except Exception as e:
            raise RuntimeError(f"Error while establishing DAQ connection with {device_name}: {e}")


