# Changelog

All notable changes to **PySantec** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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

[0.1.0]: https://github.com/santec-corporation/pysantec/releases/tag/v0.1.0
