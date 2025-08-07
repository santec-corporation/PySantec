"""
DAQ instrument module.
"""

from .wrapper import DAQ
from .base_instrument import BaseInstrument


class DAQInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = DAQ()

    @property
    def idn(self):
        return self._instrument.DeviceName

    @property
    def is_sampling(self):
        return self._instrument.IsSampling
