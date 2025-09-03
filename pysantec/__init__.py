# pysantec/__init__.py

"""
PySantec - Python Package for Santec Insertion Loss
and Polarization Dependent Loss Swept Test System.
"""

from .logger import get_logger
from .drivers import load_dlls

logger = get_logger(__name__)

try:
    # Initialize and Load the Santec DLLs
    setup_dlls_result = load_dlls()
    logger.info("Santec DLLs loaded successfully.")
except Exception as e:
    logger.error("Error while Santec DLLs: ", str(e))
    raise


from .instruments.instrument_manager import InstrumentManager
from .measurements.single_measurement_operation import SME


__all__ = [
    "InstrumentManager",
    "SME"
]
