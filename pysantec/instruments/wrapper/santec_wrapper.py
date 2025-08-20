"""
Santec Instrument DLL Wrapper.
"""

import Santec

# Santec Communication Terminator Enum class
CommunicationTerminator = Santec.CommunicationTerminator


class TSL(Santec.TSL):
    """Wrapper for the Santec TSL instrument."""

    pass


class MPM(Santec.MPM):
    """Wrapper for the Santec MPM instrument."""

    pass


class DAQ(Santec.SPU):
    """Wrapper for the Santec DAQ (SPU Class) instrument."""

    pass
