"""
Santec Instrument DLL Wrapper.
"""

import Santec


CommunicationTerminator = Santec.CommunicationTerminator


class TSL(Santec.TSL):
    pass


class MPM(Santec.MPM):
    pass


class DAQ(Santec.SPU):
    pass
