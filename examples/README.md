# 🔧 PySantec Examples

This directory provides example scripts for using the **PySantec** package to interface with Santec instruments/devices.

---

## 📘 Basic Usage Examples

Covers initial setup and connection:

- Listing available GPIB, USB, and NI DAQ resources
- Establishing connections to TSL (laser), MPM (power meter), and DAQ devices

See [`basic_usage/README.md`](basic_usage/README.md) for full instructions.

---

## 🧪 Instrument Control Examples

Demonstrates how to control individual instruments:

- **TSL**: Wavelength setting, output control, and sweep configuration
- **MPM**: Channel configuration, data logging, and power measurements
- **DAQ**: Analog input setup and data acquisition

See [`instrument_control/README.md`](instrument_control/README.md) for full examples.

---

## 📦 Requirements

- Platform: Windows 10+
- Python version 3.7+
- `pysantec` package installed
- Santec DLLs properly set up
- [NI-488.2](https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html) for GPIB devices
- [NI-VISA](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html) for GPIB communication
- [NI-DAQmx](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html) for DAQ devices
- Optional: NI-MAX for configuring/test-running connected devices

---

## 📝 License

This project is licensed under the [MIT License](/./LICENSE).
