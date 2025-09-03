"""
This module defines custom exceptions for the Pysantec library.
"""

from enum import IntEnum


class InstrumentExceptionCode(IntEnum):
    Unknown = -(2**31)  # int.MinValue in C#
    InUseError = -40
    ParameterError = -30
    DeviceError = -20
    CommunicationFailure = -14
    UnauthorizedAccess = -13
    IOException = -12
    NotConnected = -11
    Uninitialized = -10
    TimeOut = -2
    Failure = -1
    CountMismatch = -5
    MonitorError = -6
    Succeed = 0
    AlreadyConnected = 11
    Stopped = 10


def to_instrument_exception_code(status: int) -> InstrumentExceptionCode:
    try:
        return InstrumentExceptionCode(status)
    except ValueError:
        return InstrumentExceptionCode.Unknown


class PysantecError(Exception):
    """Base exception for all Pysantec errors."""

    def __init__(self, message: str, error_code: int | str = None):
        super().__init__(message)
        self.error_code = error_code


class InstrumentConnectionError(PysantecError):
    """Raised when a connection to an instrument fails."""

    pass


class InstrumentOperationError(PysantecError):
    """Raised when there's an error with instrument operations."""

    pass
