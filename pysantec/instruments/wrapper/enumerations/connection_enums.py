"""
Santec Connection Enums.
"""

from enum import Enum

from ..santec_communication_wrapper import CommunicationMethod, GPIBConnectType
from ..santec_wrapper import CommunicationTerminator


class Terminator(Enum):
    """Communication terminators for Santec instruments."""

    CR = CommunicationTerminator.Cr
    LF = CommunicationTerminator.Lf
    CRLF = CommunicationTerminator.CrLf


class GPIBType(Enum):
    """GPIB connection types for Santec instruments."""

    NIVisa = GPIBConnectType.NIVisa
    NI4882 = GPIBConnectType.NI4882
    KeysightVisa = GPIBConnectType.KeysightIO


class ConnectionType(Enum):
    """Connection types for Santec instruments."""

    USB = CommunicationMethod.USB
    GPIB = CommunicationMethod.GPIB
    TCPIP = CommunicationMethod.TCPIP
    DEV = "DAQ"
    NULL = "Unknown"
