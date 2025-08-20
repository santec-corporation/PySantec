# pysantec/__init__.py

"""
PySantec - Python Package for Santec Insertion Loss
and Polarization Dependent Loss Swept Test System.
"""

from .drivers.dll_manager import setup_dlls
from .instruments.instrument_manager import InstrumentManager

# Initialize and Load the Santec DLLs
setup_dlls_result = setup_dlls()


__all__ = [
    "InstrumentManager",
]
