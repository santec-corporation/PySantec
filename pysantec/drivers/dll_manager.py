"""
DLL Manager.

- Load the Santec DLLs from the default STS application path.
- Load the Santec DLLs from the user AppData path.
"""

import os
import clr
from pathlib import Path
from ..config import DEV_MODE

# DLL Paths
SYSTEM_DLL_PATH = r"C:\\Program Files\\santec\\Swept Test System IL And PDL"
APPDATA_DLL_PATH = Path(os.getenv("APPDATA")) / "santec" / "pysantec" / "dlls"

# DLL Names
DLL_NAMES = [
    "InstrumentDLL.dll",
    "STSProcess.dll"
]

# Check if DLLs exist
def dlls_exist(folder_path):
    """Checks if the DLLs are present in the provided folder path."""
    return all((Path(folder_path) / dll).exists() for dll in DLL_NAMES)

def setup_dlls():
    """Gets the path where the DLLs exist."""
    if dlls_exist(SYSTEM_DLL_PATH):
        dll_path = SYSTEM_DLL_PATH
        if DEV_MODE:
            print(f"Found DLLs in: {dll_path}")

    elif dlls_exist(APPDATA_DLL_PATH):
        dll_path = APPDATA_DLL_PATH
        if DEV_MODE:
            print(f"Found DLLs in AppData: {dll_path}")
    else:
        raise RuntimeError("DLLs not found.")

    return load_dlls(dll_path)


def load_dlls(dll_path, dlls = None):
    """
    Loads the DLLs from the given path.

    :param dll_path: The path from which the dlls have to loaded.
    :param dlls: The list of dlls to be loaded.

    :return: True if all the DLLs were loaded, else False.
    """
    dlls = DLL_NAMES
    for dll in dlls:
        try:
            full_path = os.path.join(dll_path, dll)
            if DEV_MODE:
                print(f"Loading DLL: {full_path}")

            # Attempt to load the DLL
            clr.AddReference(full_path)

            if DEV_MODE:
                print(f"DLL Loaded: {dll}")

        except Exception as e:
            if DEV_MODE:
                print(f"Error loading DLL '{dll}': {e}")
            return False  # Stop on first failure
    return True  # Only returns True if all DLLs are loaded successfully
