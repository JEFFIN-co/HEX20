"""End-to-end secured onboard telecommand reception and routing."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import time

from ..protocol.frame import TransferFrame, FrameSynchronizer, decode_frame
from ..protocol.packet import SpacePacket
from ..routing.apid_router import APIDRouter
from ..telemetry.metrics import Metrics
from ..security.encoder import encode_three_letter
from ..security.authenticator import create_auth_tag
from ..security.gate import SecurityGate

SECRET = "HEX20-M8-END-TO-END-SECRET"
COMMAND_MAP = {
    "HKR": (100, 3, 1),
    "MEM": (101, 6, 2),
    "FUN": (102, 8, 128),
    "CON": (103, 17, 1),
}
ROUTER_PAYLOAD = {"HKR": b"", "MEM": b"READ", "FUN": b"", "CON": b""}

@dataclass
class E2EResult:
    accepted: bool
    stage: str
    reason: str
    command: str | None = None
    apid: int | None = None
    service: int | None = None
    subtype: int | None = None
    latency_ms: float = 0.0

class EndToEndProcessor:
    def __init__(self, secret: str = SECRET, routing_config: str | Path | None = None):
        self.secret = secret
        self.security = SecurityGate(secret)
        self.sync = FrameSynchronizer()
        if routing_config is None:
            routing_config = Path(__file__).resolve().parents[3] / "config" / "routing.yaml"
        self.metrics = Metrics()
        self.router = APIDRouter(routing_config, self.metrics)
        self.counters = {
            "streams": 0, "frames": 0, "routed": 0,
            "security_rejects": 0, "replay_rejects": 0,
            "packet_rejects": 0, "routing_rejects": 0,
            "crc_rejects": 0,
        }

    def process_stream(self, stream: bytes) -> list[E2EResult]:
        self.counters["streams"] += 1
        self.metrics.received += 1
        raw_frames = self.sync.feed(stream)
        if not raw_frames:
            self.counters["packet_rejects"] += 1
            self.metrics.rejected += 1
            return [E2EResult(False, "FRAME", "NO_VALID_FRAME")]
        results = []
        for raw in raw_frames:
            self.counters["frames"] += 1
            started = time.perf_counter()
            try:
                frame = decode_frame(raw)
                packet = SpacePacket.decode(frame.payload)
                self.metrics.frames_accepted += 1
                self.metrics.packets_accepted += 1
            except ValueError as exc:
                self.counters["packet_rejects"] += 1
                self.counters["crc_rejects"] += 1
                self.metrics.packets_rejected += 1
                self.metrics.rejected += 1
                results.append(E2EResult(False, "FRAME/PACKET", str(exc), latency_ms=(time.perf_counter()-started)*1000))
                continue
            try:
                envelope = packet.data.decode("ascii")
                fields = dict(x.split("=", 1) for x in envelope.split(";"))
                encoded, counter, tag = fields["HEX"], int(fields["CTR"]), fields["TAG"]
            except (UnicodeDecodeError, ValueError, KeyError):
                self.counters["security_rejects"] += 1
                self.metrics.rejected += 1
                results.append(E2EResult(False, "SECURITY", "MALFORMED_SECURITY_ENVELOPE", latency_ms=(time.perf_counter()-started)*1000))
                continue
            security_result = self.security.verify(encoded, counter, tag)
            if not security_result.accepted:
                self.counters["security_rejects"] += 1
                self.metrics.rejected += 1
                if security_result.reason == "REPLAY_OR_OLD_COUNTER":
                    self.counters["replay_rejects"] += 1
                results.append(E2EResult(False, "SECURITY", security_result.reason, latency_ms=(time.perf_counter()-started)*1000))
                continue
            command = security_result.command
            expected = COMMAND_MAP.get(command)
            if expected is None:
                self.counters["routing_rejects"] += 1
                self.metrics.rejected += 1
                results.append(E2EResult(False, "ROUTING", "UNKNOWN_AUTHENTICATED_COMMAND", command=command, latency_ms=(time.perf_counter()-started)*1000))
                continue
            if (packet.apid, packet.service, packet.subtype) != expected:
                self.counters["routing_rejects"] += 1
                self.metrics.rejected += 1
                results.append(E2EResult(False, "ROUTING", "AUTHENTICATED_HEADER_MISMATCH", command=command, apid=packet.apid, service=packet.service, subtype=packet.subtype, latency_ms=(time.perf_counter()-started)*1000))
                continue
            routed_packet = SpacePacket(apid=packet.apid, service=packet.service, subtype=packet.subtype, data=ROUTER_PAYLOAD.get(command, b""), sequence_count=packet.sequence_count)
            route = self.router.route(routed_packet)
            ok = bool(route.get("success"))
            if ok:
                self.counters["routed"] += 1
                reason = "END_TO_END_ROUTED"
            else:
                self.counters["routing_rejects"] += 1
                self.metrics.rejected += 1
                reason = route.get("message", "ROUTING_REJECTED")
            results.append(E2EResult(ok, "ROUTER", reason, command=command, apid=packet.apid, service=packet.service, subtype=packet.subtype, latency_ms=(time.perf_counter()-started)*1000))
        return results

def build_ground_frame(command: str, counter: int, secret: str = SECRET, *, apid_override=None, service_override=None, subtype_override=None, tamper_crc=False, tamper_tag=False, malformed_envelope=False) -> bytes:
    expected = COMMAND_MAP.get(command, (2047, 1, 1))
    apid, service, subtype = expected
    if apid_override is not None: apid = apid_override
    if service_override is not None: service = service_override
    if subtype_override is not None: subtype = subtype_override
    encoded = encode_three_letter(command, secret)
    tag = create_auth_tag(secret, encoded, counter)
    if tamper_tag: tag = "0" * 64
    envelope = "BAD" if malformed_envelope else f"HEX={encoded};CTR={counter};TAG={tag}"
    packet = SpacePacket(apid=apid, service=service, subtype=subtype, data=envelope.encode("ascii"), sequence_count=counter % 16384)
    raw = bytearray(TransferFrame(vcid=1, payload=packet.encode()).encode())
    if tamper_crc: raw[8] ^= 0x01
    return bytes(raw)
