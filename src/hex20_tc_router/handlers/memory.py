def handle(packet, memory):
    # Prototype memory service: payload begins with READ or WRITE.
    command = packet.data.decode("ascii", errors="replace").strip()
    if command.upper().startswith("READ"):
        return {"success": True, "message": "memory read accepted"}
    if command.upper().startswith("WRITE"):
        return {"success": True, "message": "memory write accepted"}
    return {"success": False, "message": "unknown memory operation"}
