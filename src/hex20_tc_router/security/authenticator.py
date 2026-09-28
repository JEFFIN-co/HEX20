"""HEX20 Milestone 5 - HMAC authentication for telecommand security."""

from __future__ import annotations
import hashlib
import hmac


def create_auth_tag(secret: str, encoded_command: str, counter: int) -> str:
    """Create a full SHA-256 HMAC tag over command + freshness counter."""
    if counter < 0:
        raise ValueError("Counter must be non-negative.")

    message = f"{encoded_command}:{counter}".encode("ascii")
    return hmac.new(
        secret.encode("utf-8"),
        message,
        hashlib.sha256,
    ).hexdigest()


def verify_auth_tag(
    secret: str,
    encoded_command: str,
    counter: int,
    received_tag: str,
) -> bool:
    expected = create_auth_tag(secret, encoded_command, counter)
    return hmac.compare_digest(expected, received_tag.lower())
