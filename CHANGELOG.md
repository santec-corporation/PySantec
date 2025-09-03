# Changelog

All notable changes to **PySantec** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [0.2.0] — 2025-09-03

### Added

- More TSL functions to the `TSLInstrument` class.  
- TCPIP connection example.  
- Connection tests.  
- SME (Single Measurement Mode) implementation using TSL + MPM instruments.  
- SME tests.  
- TSL data logging tests.  
- MPM data logging tests.  

### Changed

- Refactored TSL wavelength data logging function.  
- Refactored TSL power data logging function.  
- Refactored MPM module data logging function.  
- Refactored MPM channel data logging function.  
- Exposed instrument class names in `pysantec.instruments`.  
- Moved `tests/` directory outside the `pysantec` package to the main project root.  
- Updated examples directory documentation.  
- Updated DLL load error message.  
- Updated project README documentation.  

### Fixed

- Handling of instrument exception codes.  

### Removed

- Removed unnecessary mention of `# -*- coding: utf-8 -*-`.  

---

## [0.1.1] — 2025-08-21

### Fixed
- Bug while loading Santec DLLs (commit: 8507e21)  
  - Corrected DLL path resolution logic and improved error handling when DLLs are missing.

### Changed
- Improved Santec DLL initialization (commit: [8507e21](https://github.com/santec-corporation/PySantec/commit/8507e21d6c2300899c81f8ee92114471f3026c6d))  
  - DLLs now load once at package startup in `drivers/__init__.py` with safeguards.
- Explicit resource listing (commit: [777b760](https://github.com/santec-corporation/PySantec/commit/777b7601f647ec999c0e5b630bff223140fcdfa1))  
  - `InstrumentManager` now caches discovered resources.  
  - Significantly reduces repeated discovery times.
- Updated examples & documentation (commit: [0ae0f30](https://github.com/santec-corporation/PySantec/commit/0ae0f30debd8201a3e6fca495c1182e1c4989a10))  
  - Revised README with Windows-only support notice.
- Windows-only support enforcement (commit: [bedcddd](https://github.com/santec-corporation/PySantec/commit/bedcddd387d8897508cad5d2d278a536f328a674))  
  - Added a platform check in `pysantec/drivers/dll_manager.py` that raises an error if imported on non-Windows OS.

### Platform Support
- ✅ Windows 10/11  
- ❌ Linux/macOS (explicitly blocked with helpful error message)

---

## [0.1.0] — 2025-08-20

### Added

- **Initial release of PySantec**
- Core `InstrumentManager` class for:
  - Instrument detection
  - Connection management
  - Resource validation
- Support for:
  - **TSL** — Tunable Semiconductor Laser
  - **MPM** — Multi Port Optical Power Meter
  - **DAQ** — NI Data Acquisition Devices
- DLL management system (Santec proprietary instrument DLLs)
- Example scripts:
  - Basic usage (`examples/basic_usage/`)
  - Instrument control workflows (`examples/instrument_control/`)
- Initial unit test suite (~85% coverage)
- Full type hints and docstrings

### Infrastructure

- Project structure with modular layout
- CI/CD setup using GitHub Actions
- Testing framework (`pytest`)
- Code style enforcement with `flake8`

### Documentation

- Main project `README.md`
- Instrument control usage guides
- Example directory documentation
- Developer and contribution setup instructions

---

[0.2.0]: https://github.com/santec-corporation/pysantec/releases/tag/v0.2.0
[0.1.1]: https://github.com/santec-corporation/pysantec/releases/tag/v0.1.1
[0.1.0]: https://github.com/santec-corporation/pysantec/releases/tag/v0.1.0
