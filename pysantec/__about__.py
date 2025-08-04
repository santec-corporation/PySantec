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

# Project about
__author__ = "Santec Holdings Corporation"
__license__ = "MIT"
__organization__ = "Santec Holdings Corporation"
__description__ = "Python Package for Santec Insertion Loss and Polarization Dependent Loss Swept Test System"
__url__ = f"https://github.com/santec-corporation/{__project_name__}"
__date__ = datetime.date.today().isoformat()  # Date format: "2025-08-04"
__copyright__ = f"Copyright 2025-{datetime.date.today().year}, {__organization__}"
