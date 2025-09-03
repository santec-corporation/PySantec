# SME Operation Examples

This directory contains examples demonstrating how to use the **PySantec** package to perform Single Measurement mode operations.

---

### SME Operation — `sme_operation.py`

Demonstrates how to detect and list all available instruments connected to your system:

- Connects to TSL and MPM instruments 
- Initializes the SME class
- Configures TSL parameters
- Configures MPM parameters
- Performs scan operation
- Fetches MPM channel logging data of a specific channel and module

---

### ⚙️ Usage Steps

Modify sme_operation.py with your actual instrument addresses:

- Replace 'GPIB2::3::INSTR' with your TSL's GPIB address
- Replace 'GPIB2::15::INSTR' with your MPM's GPIB address

Run the sme script example:

```bash
python sme_operation.py
```

### Resource Name Formats

| Type    | Format Example                                    |
|---------|---------------------------------------------------|
| GPIB    | `GPIBx::address::INSTR` (e.g., `GPIB1::3::INSTR`) |
| TCP/IP  | `TCPIPx::ip_address::port::SOCKET`                |

---