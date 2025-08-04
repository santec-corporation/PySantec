"""
Unified wrapper for the Santec instrument DLL.
Combines TSL, MPM, DAQ, and PCU functionality into one interface.
"""

from logging import Logger
from dataclasses import dataclass

# Importing from Santec namespace
from Santec import TSL, MPM, SPU, PCU, ExceptionCode, CommunicationTerminator
from Santec.Communication import MainCommunication, CommunicationMethod, GPIBConnectType


@dataclass
class ConnectionField:
    gpib_board: str
    gpib_address: str
    gpib_connect_type: GPIBConnectType
    usb_device_id: int
    ip_address: str
    port_number: str
    daq_device_name: str


class InstrumentWrapper:
    def __init__(self, logger: Logger):
        self.logger = logger.manager.getLogger(__class__.__name__)
        self._main_comm = MainCommunication()
        self._spu = SPU()

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

