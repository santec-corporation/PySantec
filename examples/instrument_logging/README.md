# Instrument Logging Examples

Examples in this directory describe how to fetch & print TSL and MPM logging data.

---

## Examples

### 1. Print TSL Wavelength Logging Data - `print_tsl_wavelength_logging_data.py`

Fetches the wavelength logging data from the TSL instrument and prints it on to the console.

**NOTE:** TSL logging data can only be read after performing a successful scan operation.

---

### 2. Print TSL Power Logging Data - `print_tsl_power_logging_data.py`

Fetches the power logging data from the TSL instrument and prints it on to the console.

Input Parameters:
- Scan speed (Optional value): Speed of the previous performed scan in nm/sec.
- Step wavelength (Optional value): Step wavelength of the previous performed scan in nm.

**NOTE:** TSL logging data can only be read after performing a successful scan operation.

---

### 3. Print MPM Channel Logging Data - `print_mpm_channel_logging_data.py`

Fetches the logging data of a specific channel of a module from the MPM instrument and prints it on to the console.

Input Parameters:
- Module number: 0 to 4
- Channel number: 1 to 4

**NOTE:** MPM channel logging data can only be read after performing a successful scan operation.

---

### 4. Print MPM Module Logging Data - `print_mpm_module_logging_data.py`

Fetches the logging data of all channels of a specific module from the MPM and prints it on to the console.

Input Parameters:
- Module number: 0 to 4

**NOTE:** MPM module logging data can only be read after performing a successful scan operation.

---