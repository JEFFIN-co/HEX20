"""CRC utilities for the HEX20 prototype.

Prototype convention: CRC-16/CCITT-FALSE.
Confirm the competition/mission-specific PCS convention before claiming
standards compliance.
"""

def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

def append_crc(data: bytes) -> bytes:
    return data + crc16_ccitt(data).to_bytes(2, "big")

def verify_crc(data_with_crc: bytes) -> bool:
    if len(data_with_crc) < 2:
        return False
    expected = crc16_ccitt(data_with_crc[:-2])
    received = int.from_bytes(data_with_crc[-2:], "big")
    return expected == received
