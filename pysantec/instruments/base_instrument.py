"""
Base instrument module.
"""

import inspect
from abc import ABC
from enum import Enum
from .instrument_wrapper import WrapperClass, InstrumentWrapper, TSLWrapper, MPMWrapper


class InstrumentType(Enum):
    TSL = 0
    MPM = 1
    DAQ = 2


class BaseInstrument(ABC, WrapperClass):
    def __init__(self):
        self._instrument = None

    def instrument(self, wrapper_type: InstrumentWrapper):
        if not wrapper_type:
            return None
        return self._instrument

    def _check_restricted_method(self):
        if not isinstance(self._instrument, (TSLWrapper, MPMWrapper)):
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
        self._check_restricted_method()
        _, idn = self.query('*IDN?')
        return idn

    def _get_function(self, function_name, response_type = None):
        response = None
        if isinstance(response_type, type):
            response = response_type()
        _, response = getattr(self._instrument, function_name)(response)
        return response

    def _set_function(self, function_name, value):
        _ = getattr(self._instrument, function_name)(value)

    def _get_function_enum(self, function_name, function_enum_name):
        self._check_restricted_method()
        enum_value = function_enum_name.value
        _, enum_value = getattr(self._instrument, function_name)(enum_value)
        return function_enum_name.__class__[enum_value.ToString()]

    def _set_function_enum(self, function_name, function_enum_name):
        self._check_restricted_method()
        _ = getattr(self._instrument, function_name)(function_enum_name.value)

    def disconnect(self):
        _ = self._instrument.DisConnect()
