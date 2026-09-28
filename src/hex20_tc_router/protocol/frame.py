"""Prototype TC transfer-frame framing and noisy-stream extraction."""
from dataclasses import dataclass
from .crc import append_crc, verify_crc

START = b"\x1a\xcf"
TAIL = b"\xc0\xde"
HEADER_SIZE = 4
MAX_PAYLOAD = 4096

@dataclass
class TransferFrame:
    vcid: int
    payload: bytes
    version: int = 0
    frame_type: int = 1

    def encode(self) -> bytes:
        if not 0 <= self.vcid <= 255:
            raise ValueError("VCID must be a byte")
        if len(self.payload) > MAX_PAYLOAD:
            raise ValueError("payload too large")

        version_type = ((self.version & 0x3) << 6) | ((self.frame_type & 0x1) << 5)
        header = (
            bytes([version_type, self.vcid])
            + len(self.payload).to_bytes(2, "big")
        )
        return START + append_crc(header + self.payload) + TAIL

class FrameSynchronizer:
    """Extract complete valid frames from arbitrary/noisy byte streams."""

    def __init__(self):
        self.buffer = bytearray()

    def feed(self, chunk: bytes) -> list[bytes]:
        self.buffer.extend(chunk)
        frames = []

        while True:
            start = self.buffer.find(START)
            if start < 0:
                self.buffer[:] = self.buffer[-1:]
                break

            if start:
                del self.buffer[:start]

            if len(self.buffer) < 2 + HEADER_SIZE + 2 + 2:
                break

            header = self.buffer[2:6]
            version_type = header[0]
            payload_len = int.from_bytes(header[2:4], "big")
            version = (version_type >> 6) & 0x3
            frame_type = (version_type >> 5) & 0x1

            if payload_len > MAX_PAYLOAD or version != 0 or frame_type != 1:
                del self.buffer[:2]
                continue

            total = 2 + HEADER_SIZE + payload_len + 2 + 2
            if len(self.buffer) < total:
                break

            candidate = bytes(self.buffer[:total])

            if candidate[-2:] != TAIL:
                del self.buffer[:2]
                continue

            if not verify_crc(candidate[2:-2]):
                del self.buffer[:total]
                continue

            frames.append(candidate)
            del self.buffer[:total]

        return frames

def decode_frame(raw: bytes) -> TransferFrame:
    if not (raw.startswith(START) and raw.endswith(TAIL)):
        raise ValueError("bad frame delimiters")

    body_crc = raw[2:-2]
    if not verify_crc(body_crc):
        raise ValueError("CRC mismatch")

    version_type, vcid = body_crc[0], body_crc[1]
    payload_len = int.from_bytes(body_crc[2:4], "big")
    payload = body_crc[4:-2]

    if ((version_type >> 6) & 0x3) != 0:
        raise ValueError("invalid transfer-frame version")
    if ((version_type >> 5) & 1) != 1:
        raise ValueError("invalid transfer-frame type")
    if payload_len != len(payload):
        raise ValueError("transfer-frame data length mismatch")

    return TransferFrame(vcid=vcid, payload=payload)
