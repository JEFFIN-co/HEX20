from __future__ import annotations
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st
from hex20_tc_router.processing.end_to_end_processor import COMMAND_MAP, SECRET, EndToEndProcessor, build_ground_frame

st.set_page_config(page_title="HEX20 TC Operations", page_icon="🛰️", layout="wide")
st.title("Telecommand Operations Center")
st.caption("Ground → Secure Uplink → Frame → Security → APID → PUS")

if "processor" not in st.session_state: st.session_state.processor = EndToEndProcessor(SECRET)
if "history" not in st.session_state: st.session_state.history = []
if "counter" not in st.session_state: st.session_state.counter = 1
processor = st.session_state.processor

with st.sidebar:
    st.header("Command Console")
    labels = {"HKR":"HKR — Housekeeping","MEM":"MEM — Memory","FUN":"FUN — Function Management","CON":"CON — Connection"}
    command = st.selectbox("Telecommand", list(COMMAND_MAP), format_func=lambda x: labels[x])
    tamper = st.checkbox("Simulate authentication tampering")
    crc_fault = st.checkbox("Simulate CRC fault")
    header_fault = st.checkbox("Simulate header mismatch")
    send = st.button(" TRANSMIT TELECOMMAND", width="stretch")
    if send:
        counter = st.session_state.counter
        frame = build_ground_frame(command, counter, SECRET, tamper_crc=crc_fault, tamper_tag=tamper, service_override=6 if header_fault else None)
        started = time.perf_counter(); result = processor.process_stream(frame)[0]; elapsed=(time.perf_counter()-started)*1000
        st.session_state.history.insert(0, {"time":time.strftime("%H:%M:%S"),"command":command,"counter":counter,"result":"ACCEPTED" if result.accepted else "REJECTED","stage":result.stage,"reason":result.reason,"latency_ms":round(elapsed,4)})
        st.session_state.counter += 1
    if st.button(" Clear Event Log", width="stretch"):
        st.session_state.history=[]; st.session_state.counter=1; st.session_state.processor=EndToEndProcessor(SECRET); st.rerun()

c=processor.counters
cols=st.columns(6)
for col,label,key in zip(cols,["Streams","Frames","Routed","Security Rejects","Replay Rejects","Routing Rejects"],["streams","frames","routed","security_rejects","replay_rejects","routing_rejects"]): col.metric(label,c[key])
st.divider()
left,right=st.columns([1.35,1])
with left:
    st.subheader(" Telecommand Event Log")
    if st.session_state.history:
        st.dataframe(st.session_state.history,width="stretch",hide_index=True)
    else: st.info("No telecommands transmitted yet.")
with right:
    st.subheader(" Security Status")
    if c["security_rejects"]==0: st.success("SECURITY GATE: NOMINAL")
    else: st.warning(f"SECURITY EVENTS: {c['security_rejects']}")
    st.write("**Authentication:** HMAC-SHA256")
    st.write("**Freshness:** Monotonic counter")
    st.write("**Replay protection:** Enabled")
    st.write("**Header consistency:** Enabled")
st.divider()
st.subheader(" Current Processing Chain")
st.code("""GROUND COMMAND\n      ↓\n3-Letter Keyed Encoding\n      ↓\nHMAC + Counter\n      ↓\nUPLINK\n      ↓\nFrame Synchronizer\n      ↓\nCRC Validation\n      ↓\nSpace Packet\n      ↓\nSECURITY GATE\n      ↓\nAuthenticated Header Check\n      ↓\nAPID ROUTER\n      ↓\nPUS HANDLER\n      ↓\nHOUSEKEEPING / ACTION""", language="text")
st.caption("Prototype dashboard for demonstration. The embedded secret is for development only.")
