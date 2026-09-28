from dataclasses import dataclass
import time

@dataclass
class VerificationReport:
    apid: int
    service: int
    subtype: int
    success: bool
    message: str
    processing_ms: float

def verify_command(handler, packet):
    start = time.perf_counter()
    try:
        result = handler(packet)
        success = bool(result.get("success", True))
        message = result.get("message", "completed")
    except Exception as exc:
        success = False
        message = f"handler error: {exc}"
    elapsed_ms = (time.perf_counter() - start) * 1000

    return VerificationReport(
        apid=packet.apid,
        service=packet.service,
        subtype=packet.subtype,
        success=success,
        message=message,
        processing_ms=elapsed_ms,
    )
