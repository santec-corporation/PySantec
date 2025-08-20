# Instrument Control Examples

This directory contains examples demonstrating how to control individual Santec instruments using the PySantec package. These examples show common instrument operations and settings management.

---

## TSL (Tunable Semiconductor Laser) Examples - `tsl_instrument.py`

### Basic TSL Control
```python
from pysantec import InstrumentManager

# Connect to TSL
manager = InstrumentManager()
tsl = manager.connect_tsl('GPIB1::3::INSTR')

# Basic operations
tsl.set_wavelength(1550.0)  # Set wavelength in nm
tsl.set_power(6.0)          # Set output power in dBm
tsl.set_power_unit('dBm')   # Set power unit
tsl.output_on()             # Turn laser output on
```

### Sweep Configuration

```python
# Configure sweep parameters
tsl.set_sweep_wavelength_range(1540.0, 1560.0)  # Start, stop in nm
tsl.set_sweep_speed(20.0)                        # Speed in nm/s
tsl.set_sweep_mode('Continuous')                 # Set sweep mode
```


## MPM (Multi-Port Optical Power Meter) Examples - `mpm_instrument.py`

### Basic MPM Control

```python
# Connect to MPM
mpm = manager.connect_mpm('GPIB1::17::INSTR')

# Configure channels
mpm.set_wavelength(1550.0)           # Set wavelength in nm
mpm.set_averaging_time(0.1)          # Set averaging time in ms
mpm.set_range_mode('AUTO')           # Set range mode
mpm.zero_offset_all_channels()       # Perform zero offset
```

### Data Logging

```python
# Configure logging
mpm.set_logging_parameters(1000, 0.1)  # Points, interval
mpm.start_logging()
data = mpm.get_logging_data()
```


## DAQ Examples - `daq_instrument.py`

### Basic DAQ Control

```python
# Connect to DAQ
daq = manager.connect_daq('Dev1')

# Configure analog input
daq.configure_ai_channel('ai0', -10.0, 10.0)  # Channel, min V, max V
daq.start_ai_task()
data = daq.read_ai_samples(1000)              # Read 1000 samples
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

- Wavelength range: 1500-1630nm (typical)
- Power range: -20 to +13dBm (typical)
- Sweep speeds: 0.5 to 100nm/s

#### MPM Parameters

- Wavelength range: 800-1700nm (typical)
- Power range: +10 to -90dBm (typical)
- Averaging time: 0.01ms to 10s

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