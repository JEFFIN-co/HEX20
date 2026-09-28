from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hex20_tc_router.processing.end_to_end_processor import build_ground_frame, SECRET
from hex20_tc_router.protocol.packet import SpacePacket
from hex20_tc_router.protocol.frame import TransferFrame

def build(kind: str, counter: int, replay_frame: bytes | None = None) -> bytes:
    if kind.startswith("VALID_"): return build_ground_frame({"VALID_HKR":"HKR","VALID_MEMORY":"MEM","VALID_FUNCTION":"FUN","VALID_CONNECTION":"CON"}[kind], counter, SECRET)
    if kind == "NOISE_PLUS_VALID": return b"\x00\xffNOISE" + build_ground_frame("HKR", counter, SECRET) + b"\x11NOISE"
    if kind == "CRC_FAULT": return build_ground_frame("HKR", counter, SECRET, tamper_crc=True)
    if kind == "BAD_AUTH": return build_ground_frame("HKR", counter, SECRET, tamper_tag=True)
    if kind == "HEADER_MISMATCH": return build_ground_frame("HKR", counter, SECRET, service_override=6)
    if kind == "UNKNOWN_AUTH_COMMAND": return build_ground_frame("ZZZ", counter, SECRET)
    if kind == "MALFORMED_SECURITY": return build_ground_frame("HKR", counter, SECRET, malformed_envelope=True)
    if kind == "MALFORMED_PACKET":
        packet=SpacePacket(apid=100,service=3,subtype=1,data=b"BAD",sequence_count=counter%16384); raw=bytearray(packet.encode()); raw[4:6]=(0).to_bytes(2,"big"); return TransferFrame(vcid=1,payload=bytes(raw)).encode()
    if kind == "REPLAY":
        if replay_frame is None: raise ValueError("REPLAY requires replay_frame")
        return replay_frame
    raise ValueError(kind)
