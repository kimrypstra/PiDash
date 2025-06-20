# Conversions from the value in a CAN frame to a human readable output

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Conversion(ABC):

	@abstractmethod
	def _conversion(self, data):
		pass

	def convert(self, can_frame, signal): 
		data = self.extractData(can_frame, signal)
		return self._conversion(data)

	def extractData(self, can_frame, signal): 
		# can_frame.data is a bytearray 
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
		number = int.from_bytes(data, byteorder='big')
		return 'on' if number >= 8 else 'off'
