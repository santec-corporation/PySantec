# Basic Usage Examples

This directory contains basic examples demonstrating how to use the **PySantec** package to interact with Santec instruments and NI DAQ devices.

---

## Examples

### 1. List Resources — `list_resources.py`

Demonstrates how to detect and list all available instruments connected to your system:

- Lists **GPIB** instruments  
- Lists **USB** devices  
- Lists **NI DAQ** devices  
- Prints the DLL setup status  

#### 💡 Example Code
```python
import pysantec

instrument_manager = pysantec.InstrumentManager()
resources = instrument_manager.list_resources()
print(resources)
```

---

### 2. Connect Instruments — `connect_instruments.py`

Shows how to establish connections to different types of instruments:

- Connect to a TSL (Tunable Sweep Laser)
- Connect to an MPM (Multi-Port Optical Power Meter)
- Connect to a NI DAQ device

Get basic instrument information (IDN)

#### 💡 Example Code
```python
import pysantec

instrument_manager = pysantec.InstrumentManager()
tsl = instrument_manager.connect_tsl('GPIB1::3::INSTR')
mpm = instrument_manager.connect_mpm('GPIB1::17::INSTR')
daq = instrument_manager.connect_daq('Dev1')
```

---

### 3. TCPIP — `tcpip_connect.py`

Shows how to establish connections using Ethernet / LAN:

- Connect to a TSL using a TCPIP resource

Get basic instrument information (IDN)

#### 💡 Example Code
```python
import pysantec

# Define the resource details
ip_address = "192.168.10.101"
port_number = "5000"
tcpip_resource_address = f"TCPIP::{ip_address}::{port_number}::SOCKET"

# Connect to the instrument
tsl = instrument_manager.connect_tsl(tcpip_resource_address)
```

### ⚙️ Usage Steps

Run list_resources.py to identify available instruments:

```bash
python list_resources.py
```

Modify connect_instruments.py with your actual instrument addresses:

- Replace 'GPIB1::3::INSTR' with your TSL's GPIB address
- Replace 'GPIB1::17::INSTR' with your MPM's GPIB address
- Replace 'Dev1' with your NI DAQ device name

Run the connection example:

```bash
python connect_instruments.py
```

Run the tcpip connect example:

```bash
python tcpip_connect.py
```

### Resource Name Formats

| Type    | Format Example                                    |
|---------|---------------------------------------------------|
| GPIB    | `GPIBx::address::INSTR` (e.g., `GPIB1::3::INSTR`) |
| TCP/IP  | `TCPIPx::ip_address::port::SOCKET`                |
| NI DAQ  | `Devx` (e.g., `Dev1`)                             |

---