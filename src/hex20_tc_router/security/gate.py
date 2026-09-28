"""HEX20 Milestone 5 - onboard security gate.

Pipeline:
3-letter command -> rotor-like hex encoding -> HMAC + counter
                -> onboard verification -> command release
"""

from __future__ import annotations

from dataclasses import dataclass

from .authenticator import verify_auth_tag
from .encoder import decode_three_letter
from .replay_guard import ReplayGuard


@dataclass
class SecurityResult:
    accepted: bool
    reason: str
    command: str | None = None


class SecurityGate:
    def __init__(self, secret: str) -> None:
        self.secret = secret
        self.replay_guard = ReplayGuard()

    def verify(self, encoded_command: str, counter: int, auth_tag: str) -> SecurityResult:
        if not verify_auth_tag(self.secret, encoded_command, counter, auth_tag):
            return SecurityResult(False, "AUTHENTICATION_FAILED")

        if not self.replay_guard.accept(counter):
            return SecurityResult(False, "REPLAY_OR_OLD_COUNTER")

        try:
            command = decode_three_letter(encoded_command, self.secret)
        except ValueError:
            return SecurityResult(False, "INVALID_COMMAND_ENCODING")

        return SecurityResult(True, "SECURITY_OK", command)
