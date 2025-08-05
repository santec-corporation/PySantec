"""
Base instrument module.
"""

from abc import ABC
from enum import Enum
from .instrument_wrapper import WrapperClass, InstrumentWrapper


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

    def query(self, command: str) -> tuple[int, str]:
        command = command.upper()
        try:
            status, response = self._instrument.Echo(command, "")
            return status, response
        except Exception as e:
            raise RuntimeError(f"Error while querying command {command}: {e}")

    def write(self, command: str) -> int:
        command = command.upper()
        try:
            status = self._instrument.Write(command)
            return status
        except Exception as e:
            raise RuntimeError(f"Error while writing command {command}: {e}")

    def read(self) -> tuple[int, str]:
        try:
            status, response = self._instrument.Read("")
            return status, response
        except Exception as e:
            raise RuntimeError(f"Error while reading instrument: {e}")

    @property
    def idn(self):
        _, idn = self.query('*IDN?')
        return idn
