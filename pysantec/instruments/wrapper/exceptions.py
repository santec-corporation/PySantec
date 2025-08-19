"""
This module defines custom exceptions for the Pysantec library.
"""

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