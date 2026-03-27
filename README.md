<p style="text-align: right;">
  <a href="https://www.santec.com/en/" target="_blank" rel="noreferrer">
    <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" width="250" height="45"/>
  </a>
</p>

<h1>PySantec</h1>

**Python wrapper for the Santec Insertion Loss and Polarization Dependent Loss Swept Test System.**

[![Python Versions](https://img.shields.io/pypi/pyversions/pysantec.svg)](https://pypi.python.org/pypi/pysantec)
[![License](https://img.shields.io/github/license/santec-corporation/pysantec)](LICENSE)

> [!NOTE]
> ⚠️ PySantec is currently under active development.
> Features and APIs may change without prior notice.

---

## Overview

**PySantec** is a high-level Python interface for controlling Santec instruments and NI DAQ devices, designed to simplify automated optical measurements.

It enables:

- Seamless communication with **TSL** (Tunable Semiconductor Laser)
- Efficient control of **MPM** (Multi-Port Optical Power Meter)
- Integration with **NI DAQ** devices
- *(Under development)* Execution of **IL (Insertion Loss)** and **PDL (Polarization Dependent Loss)** tests

---

## Platform & Requirements

PySantec depends on Santec’s .NET-based libraries and requires a Windows environment.

### System Requirements

- **Operating System:** Windows 10 or later  
- **Python:** 3.10, 3.11, 3.12, or 3.13 (**64-bit only**)  
- **.NET Framework:** 4.6.2 *(included by default on modern Windows systems)*  
- **Santec DLLs:** Installed via the Santec Swept Test System (IL/PDL) software  

### Download Required Software

Download the latest **STS IL/PDL Software (.NET)** from Santec:

👉 https://downloads.santec.com

### Dependencies

- **NI-488.2** – Required for GPIB device support  
  👉 https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html  

- **NI-VISA** – Required for GPIB communication  
  👉 https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html  

- **NI-DAQmx** – Required for DAQ device integration  
  👉 https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html  

- **Python.NET (CLR)** – Enables loading of Santec .NET DLLs  
  👉 https://pythonnet.github.io/  

    Install Python.NET via pip:
    ```bash
    pip install pythonnet
    ```
- **TSL USB Driver:** Required **only when connecting to Santec TSL devices via USB**  
  Available from the same Santec downloads page.

### Important Notes

#### Windows-Only Support
PySantec relies on Santec’s **.NET Framework DLLs** and is therefore **not supported on Linux or macOS**.  
Attempting to import the package on non-Windows platforms will raise an error.

#### 64-bit Requirement
Santec’s DLLs are compiled for a **64-bit architecture**.  
You must use a **64-bit version of Python**—32-bit Python is not supported and will result in DLL load failures.

#### .NET Framework Dependency
PySantec requires **.NET Framework 4.6.2 or later**.  
This version (or newer, such as 4.7.2 / 4.8) is typically **preinstalled on Windows 10 and Windows 11**, so no additional installation is usually required.

### USB Device Support
If you plan to connect to **Santec TSL devices via USB**, you must install the **TSL USB driver**.  
This is not required for other connection methods.

### Quick Checklist

Before using PySantec, confirm:

- ✔ Running on Windows  
- ✔ Using 64-bit Python (3.10–3.13)
- ✔ Santec STS IL/PDL software installed  
- ✔ NI-488.2, NI-VISA, NI-DAQmx drivers installed.
- ✔ Python.NET (CLR) Python package installed.
- ✔ *(If using USB)* TSL USB driver installed  

---

## Installation

Install the package via pip:

```bash
pip install pysantec
```

---

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

---

## Examples

Example scripts are available in the `examples/` directory.

For detailed usage and walkthroughs, see:  
👉 [Examples Documentation](examples/README.md)

---

## Supported Instruments

| Instrument Type       | Supported Models                   |
|-----------------------|------------------------------------|
| **TSL (Laser)**       | TSL-550, TSL-570, TSL-710, TSL-770 |
| **MPM (Power Meter)** | MPM-210, MPM-210H, MPM-220         |
| **DAQ (NI)**          | Devices compatible with NI-DAQmx   |

---

## Testing

To run the test suite:

```bash
pytest tests/
```

---

## Contributing

We welcome contributions! To contribute:

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to your fork
- Create a Pull Request

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

We gratefully acknowledge the following technologies and organizations that support this project:

- **National Instruments**  
  For providing essential hardware communication and control libraries, including **NI-VISA**, **NI-488.2**, and **NI-DAQmx**.

- **Python.NET**  
  For enabling seamless integration between Python and the .NET Common Language Runtime (CLR), allowing efficient interoperability across platforms.

---

## About the Santec Swept Test System

### What is STS IL/PDL?

The **Swept Test System (STS)** is a photonic measurement solution developed by 
Santec Corporation for characterizing wavelength-dependent properties of passive optical components.

It is specifically designed to measure:
- **Insertion Loss (IL)**
- **Polarization Dependent Loss (PDL)**

### System Components

The STS is composed of two key instruments:

- **Tunable Light Source (TSL)**  
  A high-performance tunable semiconductor laser that enables precise wavelength sweeping.

- **Multi-Port Power Meter (MPM)**  
  A sensitive, multi-port power meter used to accurately capture optical power across wavelengths.

Together, these components enable fast, reliable, and highly accurate optical characterization.

### Learn More

For additional details about the Swept Test System, visit:  
👉 [Santec STS Product Page](https://inst.santec.com/products/componenttesting/sts)

---

## Documentation is under development — contributions are welcome!
