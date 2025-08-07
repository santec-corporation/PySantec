"""
DAQ instrument module.
"""

from .base_instrument import BaseInstrument
from .instrument_wrapper import DAQWrapper, InstrumentWrapper


class DAQInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = DAQWrapper()

    def instrument(self, wrapper_type: InstrumentWrapper):
        if not wrapper_type:
            return None
        return self._instrument

    @property
    def idn(self):
        return self._instrument.DeviceName

    @property
    def is_sampling(self):
        return self._instrument.IsSampling
