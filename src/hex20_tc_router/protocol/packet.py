"""CCSDS-like Space Packet builder/decoder for the prototype."""
from dataclasses import dataclass

@dataclass
class SpacePacket:
    apid: int
    service: int
    subtype: int
    data: bytes
    sequence_count: int = 0

    VERSION = 0
    TYPE_TC = 1
    SEC_HEADER_FLAG = 1

    def encode(self) -> bytes:
        if not 0 <= self.apid <= 0x7FF:
            raise ValueError("APID must fit in 11 bits")
        if not 0 <= self.sequence_count <= 0x3FFF:
            raise ValueError("sequence_count must fit in 14 bits")
        if not (0 <= self.service <= 255 and 0 <= self.subtype <= 255):
            raise ValueError("service/subtype must be bytes")

        word1 = (
            (self.VERSION << 13)
            | (self.TYPE_TC << 12)
            | (self.SEC_HEADER_FLAG << 11)
            | self.apid
        )
        word2 = (0b11 << 14) | self.sequence_count
        data_field = bytes([self.service, self.subtype]) + self.data
        word3 = len(data_field) - 1

        return (
            word1.to_bytes(2, "big")
            + word2.to_bytes(2, "big")
            + word3.to_bytes(2, "big")
            + data_field
        )

    @classmethod
    def decode(cls, raw: bytes) -> "SpacePacket":
        if len(raw) < 8:
            raise ValueError("space packet too short")

        word1 = int.from_bytes(raw[0:2], "big")
        word2 = int.from_bytes(raw[2:4], "big")
        declared_minus_one = int.from_bytes(raw[4:6], "big")

        version = (word1 >> 13) & 0x7
        packet_type = (word1 >> 12) & 0x1
        sec_flag = (word1 >> 11) & 0x1
        apid = word1 & 0x7FF

        expected_total = 6 + declared_minus_one + 1
        if expected_total != len(raw):
            raise ValueError(
                f"data length mismatch: header says {expected_total}, got {len(raw)}"
            )

        if version != 0 or packet_type != 1 or sec_flag != 1:
            raise ValueError("invalid primary header")

        service, subtype = raw[6], raw[7]
        if service == 0 or subtype == 0:
            raise ValueError("service/subtype must be non-zero")

        return cls(
            apid=apid,
            service=service,
            subtype=subtype,
            data=raw[8:],
            sequence_count=word2 & 0x3FFF,
        )
