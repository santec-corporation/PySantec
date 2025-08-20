<p align="right"> <a href="https://www.santec.com/en/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>

<h1 align="left"> PySantec </h1>

**Python wrapper for Santec Insertion Loss and Polarization Dependent Loss Swept Test System.**

[![Python Versions](https://img.shields.io/pypi/pyversions/pysantec.svg)](https://pypi.python.org/pypi/pysantec)
[![License](https://img.shields.io/github/license/santec-corporation/pysantec)](LICENSE)

---

## 🧩 Overview

**PySantec** provides a high-level Python interface for controlling Santec instruments and NI DAQ devices, enabling automated optical measurements with ease. 
It simplifies:

- Communication with **TSL** (Tunable Semiconductor Laser)
- Management of **MPM** (Multi-Port Optical Power Meter)
- Integration with **NI DAQ** devices
- Execution of **IL (Insertion Loss)** and **PDL (Polarization Dependent Loss)** test routines

---

## 📦 Installation

Install via pip:

```bash
pip install pysantec
```

You must also install pythonnet (used to interface with Santec DLLs):

```bash
pip install pythonnet
```

⚠️ PythonNet (clr) only works on Windows with CPython, not PyPy or other runtimes.

---

### Dependencies

- Windows 10+ 
- Python 3.7+
- Santec instrument DLLs (must be properly set up in PATH)
- pythonnet (clr) — required for loading Santec DLLs
- [NI-488.2](https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html) for GPIB devices
- [NI-VISA](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html) for GPIB communication
- [NI-DAQmx](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html) for DAQ devices
- Optional: NI-MAX for configuring/test-running connected devices

## ⚡ Quick Start
```python
from pysantec import InstrumentManager

# Initialize instrument manager
manager = InstrumentManager()

# List available resources
resources = manager.list_resources()
print(resources)

# Connect to instruments
tsl = manager.connect_tsl('GPIB1::3::INSTR')        # Replace with your TSL GPIB address
mpm = manager.connect_mpm('GPIB1::17::INSTR')       # Replace with your MPM GPIB address
daq = manager.connect_daq('Dev1')       # Replace with your DAQ device name

# Basic laser operation
tsl.set_wavelength(1550.0)
tsl.set_power(2.0)

# Basic MPM operation
mpm.set_wavelength(1550.0)

# Basic DAQ operation
print(daq.is_sampling)
```

## 📁 Project Structure
```pgsql
pysantec/
├── drivers/                        # DLL management
│   └── dll_manager.py
├── instruments/                    # High-level instrument control
│   ├── instrument_manager.py
│   ├── base_instrument.py
│   ├── tsl_instrument.py
│   ├── mpm_instrument.py
│   ├── daq_instrument.py
│   └── wrapper/
│       ├── enumerations/
│       │   ├── connection_enums.py
│       │   ├── tsl_enums.py
│       │   └── mpm_enums.py
│       ├── santec/
│       │   └── santec_wrapper.py
│       ├── exceptions.py
│       ├── santec_communication_wrapper.py
│       └── instrument_wrapper.py
└── tests/                          # Unit tests
```

## 🧪 Examples

Example scripts are available in the `examples/` directory:

### 🔹 Basic Usage

- `examples/basic_usage/list_resources.py`
- `examples/basic_usage/connect_instruments.py`

### 🔹 Instrument Control

- `examples/instrument_control/tsl_control.py`
- `examples/instrument_control/mpm_control.py`
- `examples/instrument_control/daq_control.py`


## 🎛 Supported Instruments
| Instrument Type | Models                               |
|------------------|-------------------------------------|
| TSL (Laser)      | TSL-550, TSL-570, TSL-710, TSL-770  |
| MPM (Power Meter) | MPM-210, MPM-210H, MPM-220         |
| DAQ (NI)         | Compatible with NI-DAQmx            | 

## ✅ Testing

To run the test suite:

```bash
pytest tests/
```

## 🤝 Contributing

We welcome contributions! To contribute:

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to your fork
- Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- National Instruments – for NI-VISA, NI-488.2 and NI-DAQmx support

## 📘 Documentation is under development — contributions are welcome!