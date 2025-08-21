# Instrument Control Examples

This directory contains examples demonstrating how to control individual Santec instruments using the PySantec package. These examples show common instrument operations and settings management.

---

## TSL (Tunable Semiconductor Laser) Examples - `tsl_instrument.py`

### Basic TSL Control
```python
from pysantec import InstrumentManager
from pysantec.instruments import tsl_enums

# Connect to TSL
manager = InstrumentManager()
tsl = manager.connect_tsl('GPIB1::3::INSTR')

# Basic operations
tsl.set_wavelength(1550.0)  # Set wavelength in nm
tsl.set_power(6.0)          # Set output power in dBm
tsl.set_power_unit('dBm')   # Set power unit
tsl.set_ld_status(tsl_enums.LDStatus.ON)       # Turn laser on
```

### Sweep Configuration

```python
# Configure sweep parameters
tsl.set_scan_parameters(1540.0, 1560., 0.1, 10.0)  # Set scan parameters
```


## MPM (Multi-Port Optical Power Meter) Examples - `mpm_instrument.py`

### Basic MPM Control

```python
from pysantec import InstrumentManager
from pysantec.instruments import tsl_enums

# Connect to MPM
manager = InstrumentManager()
mpm = manager.connect_mpm('GPIB1::17::INSTR')

# Configure channels
mpm.set_wavelength(1550.0)           # Set wavelength in nm
mpm.set_averaging_time(0.1)          # Set averaging time in ms
mpm.set_range_mode('AUTO')           # Set range mode
mpm.perform_zeroing()                # Perform zero offset
```

## DAQ Examples - `daq_instrument.py`

### Basic DAQ Control

```python
from pysantec import InstrumentManager
from pysantec.instruments import tsl_enums

# Connect to DAQ
manager = InstrumentManager()
daq = manager.connect_daq('Dev1')

# Gets the sampling state of the DAQ
print(daq.is_sampling)

# Starts the sampling
daq.start_sampling()

# Gets the sampling state of the DAQ
print(daq.is_sampling)

# Stops the sampling
daq.stop_sampling()
```

---

### Usage Instructions

1. Ensure instruments are connected and powered on
2. Check instrument addresses:
   `python list_resources.py`
3. Modify examples with your instrument addresses:
   - Update GPIB addresses
   - Update channel numbers
   - Adjust parameters as needed
4. Run desired example:
   Example for TSL: `python tsl_instrument.py`


### Common Settings

#### TSL Parameters

- Wavelength range: 1260-1640nm (typical)
- Power range: -15 to +13dBm (typical)
- Sweep speeds: 1.0 to 200nm/s

#### MPM Parameters

- Wavelength range: 1250-1680nm (typical)
- Power range: +10 to -80dBm (typical)
- Averaging time: 0.01ms to 100s

#### DAQ Parameters

- Voltage range: ±10V (typical)
- Sample rate: Up to 250kS/s
- Resolution: 16-bit

### Error Handling

```python
try:
    tsl.set_wavelength(1550.0)
except pysantec.InstrumentError as e:
    print(f"Instrument error: {e}")
```

---

### 📦 Requirements

- `pysantec` package installed
- Santec DLLs properly set up
- NI-VISA for GPIB communication
- NI-DAQmx for DAQ devices