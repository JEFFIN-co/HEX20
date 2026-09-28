def handle(packet, metrics):
    return {
        "success": True,
        "message": (
            f"HK counters: received={metrics.received}, "
            f"rejected={metrics.rejected}, "
            f"frames_accepted={metrics.frames_accepted}, "
            f"frames_rejected={metrics.frames_rejected}, "
            f"packets_accepted={metrics.packets_accepted}, "
            f"packets_rejected={metrics.packets_rejected}"
        ),
    }
