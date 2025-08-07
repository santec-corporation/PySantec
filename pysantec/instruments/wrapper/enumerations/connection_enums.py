"""
Santec Connection Enums.
"""

from enum import Enum
from..santec_wrapper import CommunicationTerminator
from ..santec_communication_wrapper import CommunicationMethod, GPIBConnectType


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


