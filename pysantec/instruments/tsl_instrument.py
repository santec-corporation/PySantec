"""
TSL instrument module.
"""

from .instrument_wrapper import TSLWrapper
from .base_instrument import BaseInstrument


class TSLInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = TSLWrapper()
