# pysantec/__about__.py

"""
This module contains metadata about the pysantec package.
"""

import datetime
from importlib.metadata import PackageNotFoundError, version

# Project name
__project_name__ = "pysantec"

# Get the project version
__version__ = "unknown"
try:
    __version__ = version(__project_name__)
except PackageNotFoundError:
    pass

# Project metadata
__author__ = "Santec Holdings Corporation"
__license__ = "MIT"
__organization__ = "Santec Holdings Corporation"
__description__ = (
    "Python Package for Santec Insertion Loss "
    "and Polarization Dependent Loss Swept Test System"
)
__url__ = f"https://github.com/santec-corporation/{__project_name__}"

# Date and copyright
current_year = datetime.date.today().year
__date__ = datetime.date.today().isoformat()
__copyright__ = f"Copyright 2025-{current_year}, {__organization__}"
