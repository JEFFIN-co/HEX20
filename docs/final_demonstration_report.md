# HEX20 M11 — Final Demonstration Package

## Project
**Onboard Telecommand Reception & Routing — Secured Software Prototype**

## Purpose
Milestone 11 packages the completed prototype into a repeatable demonstration set. It consolidates the protocol, routing, security, end-to-end simulation, live dashboard and final validation work from Milestones 1–10.

## Demonstration flow

```text
Ground Command
      |
      v
[Security Envelope]
      |
      v
[Noisy Uplink Simulator]
      |
      v
[Frame Synchronization]
      |
      v
[Transfer Frame + CRC]
      |
      v
[Space Packet Decode]
      |
      v
[Security Gate: HMAC + Replay]
      |
      v
[APID / Service / Subtype Validation]
      |
      v
[PUS Handler]
      |
      v
[Telemetry + Counters + Dashboard]
```

## Supported demonstration commands

| Command | APID | Service | Subtype | Handler role |
|---|---:|---:|---:|---|
| HKR | 100 | 3 | 1 | Housekeeping |
| MEM | 101 | 6 | 2 | Memory |
| FUN | 102 | 8 | 128 | Function management |
| CON | 103 | 17 | 1 | Connection |

## Final validation campaign
The M10 campaign contains **1,000 deterministic scenarios**: 680 benign/acceptance cases and 320 fault or attack cases. The test classes cover valid commands, noise recovery, CRC faults, authentication tampering, header manipulation, unknown authenticated commands, malformed security envelopes, malformed packets and replay attempts.

The M10 report records the campaign methodology and its limitations. Exact timing values should be regenerated on the demonstration machine rather than treated as universal hardware measurements.

## Traceability

| ID | Requirement | Verification |
|---|---|---|
| HEX20-TC-001 | Receive noisy uplink stream | Frame synchronization recovers valid frames from surrounding noise (M3/M8/M10) |
| HEX20-TC-002 | Decode transfer frame | Transfer-frame fields are parsed and length checked (M1/M8) |
| HEX20-TC-003 | Validate CRC | Corrupted frames are rejected before routing (M1/M3/M8/M10) |
| HEX20-TC-004 | Extract space packet | Space Packet header/payload are decoded and validated (M1/M8/M10) |
| HEX20-TC-005 | Route APIDs | Configurable APID routing supports 32+ entries (M2/M7) |
| HEX20-TC-006 | Handle PUS services | HK/MEM/FUN/CON examples reach dedicated handlers (M2/M8/M9) |
| HEX20-TC-007 | Security authentication | Authenticated command envelope is verified before routing (M5/M7/M8/M10) |
| HEX20-TC-008 | Replay protection | Previously accepted counter/frame reuse is rejected (M5/M8/M10) |
| HEX20-TC-009 | Header binding | Authenticated command must match APID/service/subtype (M8/M10) |
| HEX20-TC-010 | Telemetry/metrics | Processing outcomes are observable through counters/dashboard (M4/M9) |
| HEX20-TC-011 | Prototype latency | Measure end-to-end software processing latency (M8/M10) |
| HEX20-TC-012 | Demonstration readiness | Provide repeatable demo, report, slides and traceability (M11) |

## Live dashboard
From the `hex20_m9_dashboard` directory, launch:

```powershell
python -m pip install -r hex20_m9_requirements.txt
python -m streamlit run hex20_m9_live_dashboard.py
```

Use the dashboard to transmit HKR, MEM, FUN and CON commands and deliberately trigger authentication, CRC and header failures.

## Presenter demo script

1. Start the dashboard.
2. Show the normal processing chain.
3. Send **HKR** and show ACCEPT/ROUTER.
4. Send **MEM** and show the memory handler path.
5. Send **FUN** and **CON** to show multiple PUS routes.
6. Enable authentication tampering and resend a command; show SECURITY rejection.
7. Enable CRC fault and resend; show FRAME rejection.
8. Enable header mismatch and resend; show ROUTING rejection.
9. Explain that replay protection rejects reuse of an already accepted freshness counter.
10. Open the M10 report and show the 1,000-command validation campaign.

## Evidence included
- M10 machine-readable JSON and CSV results
- M10 final validation report
- M9 live Streamlit dashboard
- M9 demo scenario runner
- Requirements-to-verification traceability
- Final presentation deck
- Final PDF technical report

## Engineering limitations
This remains a software prototype. It is not a flight-qualified implementation. The demonstration security secret is a development value. Production work requires mission-approved cryptography and key management, exact CCSDS/PUS profile validation, hardware-in-the-loop testing, deterministic hardware timing, persistent replay-state handling and formal verification/qualification as applicable.

## Milestone status
**M1–M10 complete; M11 packages the prototype for final demonstration and review.**
