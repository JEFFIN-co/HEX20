# HEX20 M11 Demonstration Checklist

## Before demo
- [ ] Activate Python virtual environment.
- [ ] Install M9 requirements.
- [ ] Confirm M9 dashboard launches with `python -m streamlit run hex20_m9_live_dashboard.py`.
- [ ] Keep M10 validation report and results open.

## Live demo
- [ ] Show processing chain.
- [ ] HKR → ACCEPT.
- [ ] MEM → ACCEPT.
- [ ] FUN → ACCEPT.
- [ ] CON → ACCEPT.
- [ ] Authentication tamper → SECURITY rejection.
- [ ] CRC fault → FRAME rejection.
- [ ] Header mismatch → ROUTING rejection.
- [ ] Explain replay guard and freshness counter.
- [ ] Show counters/event log.
- [ ] Show 1,000-command M10 validation evidence.

## Closing points
- Deterministic protocol/routing core.
- Security gate precedes command execution.
- Faults are rejected at the earliest applicable stage.
- Prototype timing is machine-dependent.
- Development security construction is not flight-qualified cryptography.
