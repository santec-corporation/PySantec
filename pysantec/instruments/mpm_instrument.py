"""
MPM instrument module.
"""

from .instrument_wrapper import MPMWrapper
from .base_instrument import BaseInstrument


class MPMInstrument(BaseInstrument):
    def __init__(self):
        super().__init__()
        self._instrument = MPMWrapper()
