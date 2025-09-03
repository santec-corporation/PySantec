"""
Base instrument module.
"""

import inspect
from .wrapper import (
    MPM,
    TSL,
    InstrumentWrapper,
    InstrumentExceptionCode,
    to_instrument_exception_code,
)
from ..logger import get_logger


class BaseInstrument:
    """Base class for instruments."""

    def __init__(self):
        self._instrument = None
        self._status = None
        self.logger = get_logger(self._instrument.__class__.__name__)

    def instrument(self, wrapper_type: InstrumentWrapper):
        """Set the instrument wrapper type."""
        if not wrapper_type:
            return None
        return self._instrument

    def _check_restricted_method(self):
        """Check if the method is restricted to certain instrument types."""
        if not isinstance(self._instrument, (TSL, MPM)):
            stack = inspect.stack()
            caller_frame = stack[1].function
            error_string = (
                f"{self._instrument.__class__.__name__} "
                f"is not allowed to use method '{caller_frame}'."
            )
            self.logger.error(error_string)
            raise PermissionError(error_string)

    @property
    def status(self) -> str:
        """Returns the current instrument status string."""
        return self.__status

    @property
    def __status(self) -> str:
        """Returns the current instrument status string."""
        if self._status is not None:
            return self._status.name
        return InstrumentExceptionCode.Unknown.name

    @__status.setter
    def __status(self, value: InstrumentExceptionCode):
        """Set the current instrument status."""
        self.logger.debug(f"Setting instrument status: {value}")
        self._status = value

    def query(self, command: str) -> str:
        """Send a query command to the instrument
        and return the status and response."""
        """This method is restricted to TSL and MPM instruments."""
        self._check_restricted_method()
        command = command.upper()
        self.logger.debug("Query command: %s", command)

        try:
            status, response = self._instrument.Echo(command, "")
            self.__status = to_instrument_exception_code(status)
            self.logger.debug(f"Query Status: {status}. Response: {response}.")
            return response

        except Exception as e:
            error_string = f"Error while querying command {command}: {e}"
            self.logger.error(error_string)
            raise RuntimeError(error_string)

    def write(self, command: str) -> None:
        """Send a write command to the instrument and return the status."""
        """This method is restricted to TSL and MPM instruments."""
        self._check_restricted_method()
        command = command.upper()
        self.logger.debug("Write command: %s", command)

        try:
            status = self._instrument.Write(command)
            self.__status = to_instrument_exception_code(status)
            self.logger.debug(f"Write Status: {status}.")

        except Exception as e:
            error_string = f"Error while writing command {command}: {e}"
            self.logger.error(error_string)
            raise RuntimeError(error_string)

    def read(self) -> str:
        """Read data from the instrument and return the status and response."""
        """This method is restricted to TSL and MPM instruments."""
        self._check_restricted_method()
        self.logger.debug("Read command.")

        try:
            status, response = self._instrument.Read("")
            self.__status = to_instrument_exception_code(status)
            self.logger.debug(f"Read Status: {status}. Response: {response}.")
            return response

        except Exception as e:
            error_string = f"Error while reading instrument: {e}"
            self.logger.error(error_string)
            raise RuntimeError(error_string)

    @property
    def idn(self):
        """Return the identification string of the instrument."""
        idn = self.query("*IDN?")
        self.logger.debug(f"IDN string: {idn}")
        return idn

    @property
    def product_name(self):
        """Return the product name of the instrument."""
        product_name = self._instrument.Information.ProductName
        self.logger.debug(f"Product name: {product_name}")
        return product_name

    @property
    def serial_number(self):
        """Return the serial number of the instrument."""
        serial_number = self._instrument.Information.SerialNumber
        self.logger.debug(f"Serial number: {serial_number}")
        return serial_number

    @property
    def firmware_version(self):
        """Return the firmware version of the instrument."""
        firmware_version = self._instrument.Information.FWversion
        self.logger.debug(f"Firmware version: {firmware_version}")
        return firmware_version

    def _get_response(self, function_name, *args):
        """Get a response from the instrument for a given function."""
        error_code, response = getattr(self._instrument, function_name)(*args)
        self.__status = to_instrument_exception_code(error_code)
        return response

    def _get_multiple_responses(self, function_name, response_type_1, response_type_2):
        """Get multiple responses from the instrument for a given function."""
        response_1 = self._init_response(response_type_1)
        response_2 = self._init_response(response_type_2)
        error_code, response_1, response_2 = getattr(self._instrument, function_name)(
            response_1, response_2
        )
        self.__status = to_instrument_exception_code(error_code)
        return response_1, response_2

    def _set_and_get_multiple_responses(
        self, function_name, response_type_1, response_type_2, *args
    ):
        """Set values and get multiple responses
        from the instrument for a given function."""
        response_1 = self._init_response(response_type_1)
        response_2 = self._init_response(response_type_2)
        error_code, response_1, response_2 = getattr(self._instrument, function_name)(
            *args, response_1, response_2
        )
        self.__status = to_instrument_exception_code(error_code)
        return response_1, response_2

    def _get_function(self, function_name, response_type):
        """Get a response from the instrument for a given function."""
        response = self._init_response(response_type)
        return self._get_response(function_name, response)

    def _set_function(self, function_name, *args):
        """Set values on the instrument for a given function."""
        error_code = getattr(self._instrument, function_name)(*args)
        self.__status = to_instrument_exception_code(error_code)

    def _set_and_get_function(self, function_name, *args, response_type=-1):
        """Set values and get a response
        from the instrument for a given function."""
        if response_type != -1:
            response = self._init_response(response_type)
            return self._get_response(function_name, *args, response)
        return self._get_response(function_name, *args)

    @staticmethod
    def _init_response(response_type):
        """Initialize a response based on the provided type."""
        return response_type() if isinstance(response_type, type) else None

    def _get_function_enum(self, function_name, function_enum_name):
        """Get an enum value from the instrument for a given function."""
        self._check_restricted_method()
        enum_value = function_enum_name.value
        error_code, enum_value = getattr(self._instrument, function_name)(enum_value)
        self.__status = to_instrument_exception_code(error_code)
        return function_enum_name.__class__(enum_value)

    def _set_function_enum(self, function_name, function_enum_name):
        """Set an enum value on the instrument for a given function."""
        self._check_restricted_method()
        error_code = getattr(self._instrument, function_name)(function_enum_name.value)
        self.__status = to_instrument_exception_code(error_code)

    def _set_and_get_function_enum(self, function_name, enum_type, *args):
        """Set values and get an enum value
        from the instrument for a given function."""
        self._check_restricted_method()
        error_code, enum_value = getattr(self._instrument, function_name)(*args)
        self.__status = to_instrument_exception_code(error_code)
        return enum_type(enum_value)

    def disconnect(self):
        """Disconnect the instrument."""
        self.logger.info("Disconnecting instrument.")
        error_code = self._instrument.DisConnect()
        self.__status = to_instrument_exception_code(error_code)
        self.logger.info(f"Instrument disconnected. Status: {self.__status}.")
