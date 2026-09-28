from __future__ import annotations
from pathlib import Path
import yaml

from ..handlers import housekeeping, memory, function_management, connection, default

HANDLERS = {
    "housekeeping": housekeeping.handle,
    "memory": memory.handle,
    "function_management": function_management.handle,
    "connection": connection.handle,
}

class APIDRouter:
    """Configurable APID -> PUS service/subtype router."""
    def __init__(self, config_path: str | Path, metrics=None):
        self.metrics = metrics
        self.routes = self._load_routes(config_path)
        self.memory = bytearray(4096)

    @staticmethod
    def _load_routes(config_path: str | Path):
        data = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        return {int(k): v for k, v in data.get("routes", {}).items()}

    def route(self, packet):
        route = self.routes.get(packet.apid)
        if route is None:
            return default.handle(packet)
        if route["service"] != packet.service or route["subtype"] != packet.subtype:
            return {"success": False, "message": "service/subtype does not match configured APID route"}
        handler = HANDLERS.get(route["handler"])
        if handler is None:
            return default.handle(packet)
        if route["handler"] == "housekeeping":
            return handler(packet, self.metrics)
        if route["handler"] == "memory":
            return handler(packet, self.memory)
        return handler(packet)
