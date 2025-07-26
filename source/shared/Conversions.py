# Conversions from the value in a CAN frame to a human readable output

from abc import ABC, abstractmethod
from dataclasses import dataclass
import struct

@dataclass
class Conversion(ABC):

	@abstractmethod
	def _conversion(self, data):
		pass

	def convert(self, can_frame, signal): 
		data = self._extract_bytes(can_frame, signal)
		return self._conversion(data)

	# Extracts the relevant bytes from the bytearray inside can_frame
	#
	# Note, does not check the value of any bytes or bits. Just returns the smallest chunk of data that is common to all signals - a range of bytes. 
	# It's up to the individual conversion to extract the actual value from the bytes. The reason for this is some signals take up multiple full bytes, 
	# - for example RPM spans 2 bytes - while others span a single bit - for example brake switch. So the minimum this function will return is a single 
	# byte, and the brake conversion method will inspect the individual bit, and the RPM conversion will inspect the range of bits. 
	def _extract_bytes(self, can_frame, signal): 

		"""
		OK, so: it's not a single signal per BYTE, it could even be a single signal per BIT. So our value of 8 for the brake light switch
		is only that becuase it's bit 3 of byte 1: 00001000 is 8. So if any other bit != 0 the value of byte 1 will 
		no longer be 8.

		So we need to do bitwise operations either here OR in the conversion step. Probably the conversion step. Extract data should just return
		the relevant bytes, then _conversion does the bitwise operation (if neccessary) and finally returns the value. Probs rename this function
		to extract_bytes

		Next steps: 
		x Bitwise operations 
		x Alarm as lambda instead of numeric value in gauges 
		x Base gauge view model? 
		- Create a dial gauge
		- Create slightly more useful gauges, just boost and something else simple
		- Investigate SSM
		- Investigate low speed CAN 
		- Investigate arduino based engine bay sensor suite connected to Pi via UART 
			- Oil pressure
			- Oil temp 
			- Charge air temp? If it's not on the CANBUS or SSM already
		"""

		offset = signal.offset
		end = signal.offset + signal.size
		return can_frame.data[offset:end]

class CONVERSION_TEST(Conversion):
	def _conversion(self, data): 
		# number = int.from_bytes(data, byteorder='big', signed=True)
		number = struct.unpack('>d', data)[0]
		return number * 100

class CONVERSION_POS_NEG(Conversion):
	def _conversion(self, data):
		number = int.from_bytes(data, byteorder='big', signed=True)  
		return 'positive' if number >= 0 else 'negative'

class CONVERSION_BRAKES(Conversion):
	def _conversion(self, data):
		number = int.from_bytes(data, byteorder='big', signed=False)
		is_on = (number >> 3) & 1
		return 'on' if is_on else 'off'

class CONVERSION_PASSTHROUGH_INT(Conversion):
	def _conversion(self, data):
		number = int.from_bytes(data, byteorder='big', signed=True)
		return number
