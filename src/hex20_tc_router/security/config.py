"""HEX20 Milestone 5 - local security configuration.

Do not commit real mission secrets to source control.
This demo uses an environment variable and provides a development default.
"""

from __future__ import annotations
import os

ENV_NAME = "HEX20_TC_SECURITY_KEY"
DEMO_SECRET = "HEX20-DEMO-CHANGE-ME"


def get_security_key() -> str:
    return os.getenv(ENV_NAME, DEMO_SECRET)
