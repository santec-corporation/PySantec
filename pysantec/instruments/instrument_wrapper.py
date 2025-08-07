"""
Unified wrapper for the Santec instrument DLL.
Combines TSL, MPM, DAQ, and PCU functionality into one interface.
"""

from enum import Enum
from logging import Logger

# Importing from Santec namespace
from Santec import TSL, MPM, SPU, ExceptionCode, CommunicationTerminator
from Santec.Communication import MainCommunication, CommunicationMethod, GPIBConnectType


# region Instrument Class Wrapper
class WrapperClass:
    pass

class TSLWrapper(TSL):
    pass

class MPMWrapper(MPM):
    pass

class DAQWrapper(SPU):
    pass
# endregion


# region Communication Enums
class Terminator(Enum):
    CR = CommunicationTerminator.Cr
    LF = CommunicationTerminator.Lf
    CRLF = CommunicationTerminator.CrLf

class GPIBType(Enum):
    NIVisa = GPIBConnectType.NIVisa
    NI4882 = GPIBConnectType.NI4882
    KeysightVisa = GPIBConnectType.KeysightIO

class ConnectionType(Enum):
    USB = CommunicationMethod.USB
    GPIB = CommunicationMethod.GPIB
    TCPIP = CommunicationMethod.TCPIP
    DEV = "DAQ"
    NULL = "Unknown"
# endregion


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

    @staticmethod
    def connect_gpib(instrument_instance, gpib_board: int, gpib_address: int,
                     gpib_connect_type: GPIBType, connection_type: ConnectionType, terminator: Terminator):
        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise Exception("Could not create instrument instance.")
        instrument.GPIBBoard = gpib_board
        instrument.GPIBAddress = gpib_address
        instrument.GPIBConnectType = gpib_connect_type.value
        instrument.Terminator = terminator.value
        instrument.Connect(connection_type.value)

    @staticmethod
    def connect_daq(instrument_instance, device_name: str):
        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise Exception("Could not create instrument instance.")
        instrument.DeviceName = device_name
        instrument.Connect("")


