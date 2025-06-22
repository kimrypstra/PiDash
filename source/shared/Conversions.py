# Conversions from the value in a CAN frame to a human readable output

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Conversion(ABC):

	@abstractmethod
	def _conversion(self, data):
		pass

	def convert(self, can_frame, signal): 
		data = self._extract_bytes(can_frame, signal)
		return self._conversion(data)

	# Extracts the relevant bytes from the bytearray inside can_frame
	def _extract_bytes(self, can_frame, signal): 

		"""
		OK, so: it's not a single signal per BYTE, it could even be a single signal per BIT. So our value of 8 for the brake light switch
		is only that becuase it's bit 3 of byte 1: 00001000 is 8. So if any other bit != 0 the value of byte 1 will 
		no longer be 8.

		So we need to do bitwise operations either here OR in the conversion step. Probably the conversion step. Extract data should just return
		the relevant bytes, then _conversion does the bitwise operation (if neccessary) and finally returns the value. Probs rename this function
		to extract_bytes

		Next steps: 
		- Bitwise operations 
		- Alarm as lambda instead of numeric value in gauges 
		- Base gauge view model? 
		- Create slightly better gauges, just boost and something else simple
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
		number = int.from_bytes(data, byteorder='big', signed=True)
		return number

class CONVERSION_POS_NEG(Conversion):
	def _conversion(self, data):
		number = int.from_bytes(data, byteorder='big', signed=True)  
		return 'positive' if number >= 0 else 'negative'

class CONVERSION_BRAKES(Conversion):
	def _conversion(self, data):
		number = int.from_bytes(data, byteorder='big', signed=False)
		on = (number >> 3) & 1
		return 'on' if on else 'off'
