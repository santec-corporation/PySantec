"""
Unified wrapper for the Santec Instrument DLL.
"""

from logging import Logger
from typing import Any, List, Optional

from .enumerations.connection_enums import ConnectionType, GPIBType, Terminator
from .exceptions import InstrumentConnectionError, InstrumentOperationError
from .santec_communication_wrapper import MainCommunication
from .santec_wrapper import DAQ


class InstrumentWrapper:
    """Unified wrapper for the Santec Instrument DLL."""

    def __init__(self, logger: Logger):
        """Initialize the wrapper with logging capability.

        Args:
            logger: Logger instance for tracking operations
        """
        self.logger = logger.manager.getLogger(__class__.__name__)
        self._main_comm = MainCommunication()
        self._spu = DAQ()

    def get_usb_resources(self) -> List[str]:
        """Get available USB resources.

        Returns:
            List of USB resource identifiers
        """
        resources = list(self._main_comm.Get_USB_Resouce())
        self.logger.debug(f"USB resources found: {len(resources)}")
        return resources

    def get_gpib_resources(self) -> List[str]:
        """Get available GPIB resources.

        Returns:
            List of GPIB resource identifiers
        """
        resources = list(self._main_comm.Get_GPIB_Resources())
        self.logger.debug(f"GPIB resources found: {len(resources)}")
        return resources

    def get_serial_ports(self) -> List[str]:
        """Get available serial ports.

        Returns:
            List of serial port identifiers
        """
        resources = list(self._main_comm.Get_Serial_Port())
        self.logger.debug(f"Serial port resources found: {len(resources)}")
        return resources

    def get_daq_devices(self) -> Optional[List[str]]:
        """Get available DAQ devices.

        Returns:
            List of DAQ device identifiers or None if no devices found

        Raises:
            DeviceError: If there's an error getting DAQ devices
        """
        response = self._spu.Get_Device_ID(None)
        error_code, devices = response[0], list(response[1])

        self.logger.debug(f"DAQ devices found: {len(devices)}")

        if error_code == -11:
            self.logger.debug("No DAQ devices connected")
            return None
        if error_code != 0:
            raise InstrumentOperationError(
                "Error while getting DAQ devices", error_code
            )

        return devices

    @staticmethod
    def _create_instrument(instrument_instance: Any) -> Any:
        """Create and validate instrument instance.

        Args:
            instrument_instance: Instance to create instrument from

        Returns:
            Created instrument

        Raises:
            ConnectionError: If instrument creation fails
        """
        instrument = instrument_instance.instrument(InstrumentWrapper)
        if not instrument:
            raise InstrumentConnectionError("Could not create instrument instance")
        return instrument

    def connect_gpib(
        self,
        instrument_instance: Any,
        gpib_board: int,
        gpib_address: int,
        gpib_connect_type: GPIBType,
        terminator: Terminator,
    ) -> None:
        """Connect to instrument via GPIB.

        Args:
            instrument_instance: Instance to connect to
            gpib_board: GPIB board number
            gpib_address: GPIB address
            gpib_connect_type: Type of GPIB connection
            terminator: Message terminator type

        Raises:
            ConnectionError: If connection fails
        """
        instrument = self._create_instrument(instrument_instance)

        instrument.GPIBBoard = gpib_board
        instrument.GPIBAddress = gpib_address
        instrument.GPIBConnectType = gpib_connect_type.value
        instrument.Terminator = terminator.value

        try:
            error_code = instrument.Connect(ConnectionType.GPIB.value)
            if error_code != 0:
                raise InstrumentConnectionError(
                    f"Failed to establish GPIB connection "
                    f"with GPIB{gpib_board}::{gpib_address}",
                    error_code,
                )
        except Exception as e:
            raise InstrumentConnectionError(
                f"Error connecting to GPIB{gpib_board}::{gpib_address}",
                str(e),
            )

    def connect_tcpip(
        self,
        instrument_instance: Any,
        ip_address: str,
        port_number: int,
        terminator: Terminator,
    ) -> None:
        """Connect to instrument via TCP/IP.

        Args:
            instrument_instance: Instance to connect to
            ip_address: IP address of the instrument
            port_number: Port number
            terminator: Message terminator type

        Raises:
            ConnectionError: If connection fails
        """
        instrument = self._create_instrument(instrument_instance)

        instrument.IPAddress = ip_address
        instrument.Port = port_number
        instrument.TimeOut = 5000
        instrument.Terminator = terminator.value

        try:
            error_code = instrument.Connect(ConnectionType.TCPIP.value)
            if error_code != 0:
                raise InstrumentConnectionError(
                    f"Failed to establish LAN connection "
                    f"with {ip_address}::{port_number}",
                    error_code,
                )
        except Exception as e:
            raise InstrumentConnectionError(
                f"Error connecting to {ip_address}::{port_number}", str(e)
            )

    def connect_daq(self, instrument_instance: Any, device_name: str) -> None:
        """Connect to DAQ device.

        Args:
            instrument_instance: Instance to connect to
            device_name: Name of the DAQ device

        Raises:
            ConnectionError: If connection fails
        """
        instrument = self._create_instrument(instrument_instance)
        instrument.DeviceName = device_name

        try:
            error_code, device = instrument.Connect("")
            if error_code != 0:
                raise InstrumentConnectionError(
                    f"Failed to establish DAQ connection with {device_name}",
                    error_code,
                )
        except Exception as e:
            raise InstrumentConnectionError(
                f"Error connecting to DAQ {device_name}", str(e)
            )
