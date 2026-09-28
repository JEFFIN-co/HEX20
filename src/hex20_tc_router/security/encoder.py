"""HEX20 Milestone 5 - Enigma-inspired 3-letter command encoding.

This rotor-like layer is intentionally NOT treated as cryptographic security.
The real security check is HMAC authentication + freshness validation.
"""

from __future__ import annotations
import hashlib
import string

ALPHABET = string.ascii_uppercase


def _rotation(key: str, position: int) -> int:
    digest = hashlib.sha256(f"{key}:{position}".encode()).digest()
    return digest[0] % 26


def encode_three_letter(command: str, secret: str) -> str:
    """Encode exactly three A-Z letters into a six-character hex value."""
    command = command.strip().upper()
    if len(command) != 3 or any(c not in ALPHABET for c in command):
        raise ValueError("Command must contain exactly three A-Z letters.")

    values = []
    for i, ch in enumerate(command):
        plain = ord(ch) - 65
        mixed = (plain + _rotation(secret, i)) % 26
        values.append(mixed)

    # Pack the three base-26 values into one integer and render as hex.
    packed = values[0] * 26 * 26 + values[1] * 26 + values[2]
    return f"{packed:06X}"


def decode_three_letter(encoded_hex: str, secret: str) -> str:
    """Reverse the rotor-like transformation."""
    if len(encoded_hex) != 6:
        raise ValueError("Encoded command must be exactly 6 hex characters.")
    try:
        packed = int(encoded_hex, 16)
    except ValueError as exc:
        raise ValueError("Encoded command is not valid hexadecimal.") from exc

    if packed >= 26 ** 3:
        raise ValueError("Encoded command is outside the valid 3-letter range.")

    values = [
        packed // (26 * 26),
        (packed // 26) % 26,
        packed % 26,
    ]

    chars = []
    for i, value in enumerate(values):
        plain = (value - _rotation(secret, i)) % 26
        chars.append(chr(65 + plain))
    return "".join(chars)
