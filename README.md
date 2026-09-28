# HEX20 — Onboard Telecommand Reception & Routing

A software prototype for the HEX20 COSPAR Flight Software problem statement **“Onboard Telecommand Reception & Routing.”**

The system demonstrates an end-to-end onboard telecommand pipeline that receives commands from a noisy uplink, validates the transfer frame and space packet, authenticates the command, protects against replay, validates APID/service/subtype information, and routes the command to the appropriate handler.

## 🚀 Overview

```text
Ground Telecommand
        │
        ▼
   Noisy Uplink
        │
        ▼
Frame Synchronization
        │
        ▼
Transfer Frame Validation
        │
        ▼
    CRC Check
        │
        ▼
Space Packet Extraction
        │
        ▼
 Security Gate
 ┌──────┴──────┐
 │ HMAC/Auth   │
 │ Replay      │
 │ Freshness   │
 └──────┬──────┘
        │
        ▼
APID / Service / Subtype Validation
        │
        ▼
     PUS Router
        │
        ▼
 Command Handler
        │
        ▼
Telemetry / Housekeeping
        │
        ▼
   Live Dashboard
```

## 🎯 Objectives

- Receive telecommands from a noisy uplink stream.
- Detect and synchronize transfer frames.
- Validate transfer-frame headers.
- Verify CRC integrity.
- Extract and validate space packets.
- Route commands using configurable APIDs.
- Support PUS service/subtype handlers.
- Authenticate telecommands.
- Detect replayed commands.
- Reject malformed, corrupted, or mismatched commands.
- Maintain processing and housekeeping metrics.
- Provide a live Streamlit dashboard.
- Validate the complete pipeline through large-scale simulation.

## 🛰️ Supported Commands

| Command | APID | Service | Subtype | Purpose |
|---|---:|---:|---:|---|
| HKR | 100 | 3 | 1 | Housekeeping |
| MEM | 101 | 6 | 2 | Memory Management |
| FUN | 102 | 8 | 128 | Function Management |
| CON | 103 | 17 | 1 | Connection Management |

The routing design supports a configurable table with **32+ APID entries**.

## 🔐 Security Layer

The security gate is placed **before application routing**.

The prototype includes:

- Command authentication.
- HMAC-based integrity verification.
- Freshness/replay counter.
- Replay rejection.
- Authenticated command verification.
- APID/service/subtype consistency checking.
- Security rejection before application execution.

> **Important:** This is a research and demonstration prototype. It is not flight-qualified cryptography and does not provide a production spacecraft key-management system.

## 🧪 Fault Injection

The simulator can exercise:

- Random uplink noise.
- CRC corruption.
- Authentication/tag tampering.
- Replay attempts.
- Header mismatches.
- Unknown authenticated commands.
- Malformed security envelopes.
- Malformed packets.
- Unknown APIDs.
- Service/subtype mismatches.

Example:

```text
Authentication Tampering → SECURITY REJECT
CRC Fault                → FRAME REJECT
Header Mismatch          → ROUTING REJECT
Replay                   → SECURITY REJECT
Malformed Packet         → PACKET/FRAME REJECT
```

## 📊 Validation

The final prototype was exercised using a **1,000-command validation campaign** containing valid commands and multiple fault/security scenarios.

The campaign includes valid HKR/MEM/FUN/CON commands, noisy frames, CRC faults, authentication attacks, header manipulation, unknown commands, malformed security envelopes, malformed packets, and replay attempts.

Validation outputs are maintained under:

```text
validation/
├── results.csv
├── results.json
└── validation_report.md
```

The measurements are **local software-prototype measurements**, not spacecraft flight qualification.

## 🖥️ Live Dashboard

The project provides a Streamlit dashboard for live demonstration.

The dashboard can:

- Transmit HKR/MEM/FUN/CON commands.
- Display accepted/rejected commands.
- Show the processing stage.
- Simulate authentication tampering.
- Simulate CRC faults.
- Simulate header mismatches.
- Display security and routing events.
- Display counters and processing latency.
- Show the end-to-end processing chain.

## 📁 Project Structure

```text
hex20-telecommand-router/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│
├── src/
│   └── hex20_tc_router/
│       ├── protocol/
│       ├── routing/
│       ├── security/
│       ├── processing/
│       ├── simulation/
│       ├── telemetry/
│       ├── pus/
│       ├── handlers/
│       └── state/
│
├── app/
│   └── hex20_live_dashboard.py
│
├── tests/
│
├── validation/
│
└── scripts/
    ├── run_demo.ps1
    └── run_tests.ps1
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hex20-telecommand-router.git
cd hex20-telecommand-router
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## ▶️ Run the Live Demo

From the project root:

```powershell
.\scripts\run_demo.ps1
```

Or directly:

```powershell
$env:PYTHONPATH="$PWD\src"
python -m streamlit run app/hex20_live_dashboard.py
```

Open:

```text
http://localhost:8501
```

## 🧪 Run Tests

```bash
pytest
```

Or on Windows:

```powershell
.\scripts\run_tests.ps1
```

## 🎬 Recommended Demonstration

### 1. Valid command

```text
HKR → ACCEPT
```

### 2. Memory command

```text
MEM → ACCEPT
```

### 3. Authentication attack

Enable **Simulate authentication tampering**:

```text
HKR → SECURITY REJECT
```

### 4. CRC attack

Enable **Simulate CRC fault**:

```text
HKR → FRAME REJECT
```

### 5. Header manipulation

Enable **Simulate header mismatch**:

```text
HKR → ROUTING REJECT
```

This demonstrates both the normal processing path and the rejection behavior.

## 📈 Performance

Local prototype measurements demonstrated sub-millisecond processing latency for the tested command-processing pipeline.

Exact validation results are available in `validation/`.

These measurements depend on the development machine and software environment and should not be interpreted as spacecraft hardware timing qualification.

## ⚠️ Limitations

This project is a research/prototype implementation.

A production or flight implementation would require:

- Formal CCSDS/ECSS compliance verification.
- Flight-hardware timing validation.
- Hardware-in-the-loop testing.
- Fault-tolerance and radiation analysis.
- Formal security review.
- Production cryptographic key management.
- Extensive fault-injection campaigns.
- Spacecraft-specific interface integration.
- Formal verification where applicable.

## 🔭 Future Work

- Hardware-in-the-loop simulation.
- More complete CCSDS channel coding.
- Extended PUS service support.
- Secure key-management infrastructure.
- Distributed spacecraft simulation.
- Flight-computer benchmarking.
- Fault-tolerant redundant processing.
- Extended telemetry visualization.
- Automated continuous validation.

## 📜 Project Status

**Status: Prototype / Demonstration Ready**

The project currently provides:

- Protocol processing.
- CRC validation.
- Space packet extraction.
- APID routing.
- PUS service/subtype handling.
- Security authentication.
- Replay protection.
- Fault injection.
- End-to-end processing.
- Live dashboard.
- Automated validation.

## 👨‍💻 Project

**HEX20 — Onboard Telecommand Reception & Routing**

Developed as a software prototype for the HEX20 COSPAR Flight Software problem statement.

## 📄 License

Add the appropriate project license before public release.
