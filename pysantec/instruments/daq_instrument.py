"""
DAQ instrument module.
"""

from .instrument_wrapper import DAQWrapper, InstrumentWrapper


class DAQInstrument:
    def __init__(self):
        super().__init__()
        self._instrument = DAQWrapper()

    def instrument(self, wrapper_type: InstrumentWrapper):
        if not wrapper_type:
            return None
        return self._instrument

    @property
    def device_name(self):
        return self._instrument.DeviceName
