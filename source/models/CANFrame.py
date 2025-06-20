from dataclasses import dataclass

@dataclass(frozen=True)
class CANFrame:
	pid: str
	data: bytearray