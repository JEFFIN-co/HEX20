from dataclasses import dataclass

@dataclass
class Metrics:
    received: int = 0
    rejected: int = 0
    frames_accepted: int = 0
    frames_rejected: int = 0
    packets_accepted: int = 0
    packets_rejected: int = 0

    def snapshot(self):
        return {
            "telecommands_received": self.received,
            "telecommands_rejected": self.rejected,
            "frames_accepted": self.frames_accepted,
            "frames_rejected": self.frames_rejected,
            "packets_accepted": self.packets_accepted,
            "packets_rejected": self.packets_rejected,
        }
