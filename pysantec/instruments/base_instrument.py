"""
Base instrument module.
"""

import inspect
from .wrapper import InstrumentWrapper, TSL, MPM


class BaseInstrument:
    def __init__(self):
        self._instrument = None

    def instrument(self, wrapper_type: InstrumentWrapper):
        if not wrapper_type:
            return None
        return self._instrument

    def _check_restricted_method(self):
        if not isinstance(self._instrument, (TSL, MPM)):
            stack = inspect.stack()
            caller_frame = stack[1].function
            raise PermissionError(
                f"{self._instrument.__class__.__name__} is not allowed to use method '{caller_frame}'."
            )

    def query(self, command: str) -> tuple[int, str]:
        self._check_restricted_method()
        command = command.upper()
        try:
            status, response = self._instrument.Echo(command, "")
            return status, response
        except Exception as e:
            raise RuntimeError(f"Error while querying command {command}: {e}")

    def write(self, command: str) -> int:
        self._check_restricted_method()
        command = command.upper()
        try:
            status = self._instrument.Write(command)
            return status
        except Exception as e:
            raise RuntimeError(f"Error while writing command {command}: {e}")

    def read(self) -> tuple[int, str]:
        self._check_restricted_method()
        try:
            status, response = self._instrument.Read("")
            return status, response
        except Exception as e:
            raise RuntimeError(f"Error while reading instrument: {e}")

    @property
    def idn(self):
        _, idn = self.query('*IDN?')
        return idn

    @property
    def product_name(self):
        return self._instrument.Information.ProductName

    @property
    def serial_number(self):
        return self._instrument.Information.SerialNumber

    @property
    def firmware_version(self):
        return self._instrument.Information.FWversion

    def _get_response(self, function_name, *args):
        _, response = getattr(self._instrument, function_name)(*args)
        return response

    def _get_multiple_responses(self, function_name, response_type_1, response_type_2):
        response_1 = self._init_response(response_type_1)
        response_2 = self._init_response(response_type_2)
        _, response_1, response_2 = getattr(self._instrument, function_name)(response_1, response_2)
        return response_1, response_2

    def _set_and_get_multiple_responses(self, function_name, response_type_1, response_type_2, *args):
        response_1 = self._init_response(response_type_1)
        response_2 = self._init_response(response_type_2)
        _, response_1, response_2 = getattr(self._instrument, function_name)(*args, response_1, response_2)
        return response_1, response_2

    def _get_function(self, function_name, response_type):
        response = self._init_response(response_type)
        return self._get_response(function_name, response)

    def _set_function(self, function_name, *args):
        getattr(self._instrument, function_name)(*args)

    def _set_and_get_function(self, function_name, *args, response_type = -1):
        if response_type is not -1:
            response = self._init_response(response_type)
            return self._get_response(function_name, *args, response)
        return self._get_response(function_name, *args)

    @staticmethod
    def _init_response(response_type):
        return response_type() if isinstance(response_type, type) else None

    def _get_function_enum(self, function_name, function_enum_name):
        self._check_restricted_method()
        enum_value = function_enum_name.value
        _, enum_value = getattr(self._instrument, function_name)(enum_value)
        return function_enum_name.__class__(enum_value)

    def _set_function_enum(self, function_name, function_enum_name):
        self._check_restricted_method()
        _ = getattr(self._instrument, function_name)(function_enum_name.value)

    def _set_and_get_function_enum(self, function_name, enum_type, *args):
        self._check_restricted_method()
        _, enum_value = getattr(self._instrument, function_name)(*args)
        return enum_type(enum_value)

    def disconnect(self):
        _ = self._instrument.DisConnect()
