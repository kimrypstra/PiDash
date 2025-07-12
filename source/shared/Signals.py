from dataclasses import dataclass 

# Represents a usable value that can be extracted from a CANFrame 
#
# pid: The id that carries the signal 
# offset: Where in the CANFrame's payload does this signal start? 
# size: How many bytes does this signal take up? 
# 
# For example, consider this output from cansniffer
#
# Time  | ID  | Payload 
# 00020 | 514 | 08 00 75 00 C8 DD 9D 00 ..u.....
#
# The first byte (08) carries the 'is the brake on' signal. The other bytes are some other things. 
# So we construct Signal(514, 0, 0) to represent 'is the brake on' signal.
@dataclass
class Signal: 
	pid: int 
	offset: int
	size: int

SIGNAL_TEST = Signal(0x1,0,8)
SIGNAL_BRAKES = Signal(0x514,0,1) # 08 = brake on, 00 = brake off 