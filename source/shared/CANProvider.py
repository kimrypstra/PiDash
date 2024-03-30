class CANProvider: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self):
		self.can_service = MockCANService()
		self.subscribe_to_pid(1)

	def subscribe_to_pid(self, pid):
		# For now, just emit the stream. Later, filter on the pid
		self.stream = self.can_service.stream

import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops
import math
import threading  
from threading import Thread

class MockCANService: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared


	def __init__(self):  
		self.configure_observables()

	def configure_observables(self):
		numbers = [math.sin(x) for x in range(360)]
		number_stream = rx.from_iterable(numbers)
		# letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
		# letter_stream = rx.from_iterable(letters)

		# combined = rx.combine_latest(number_stream, letter_stream)
		# self.stream = combined
		background_thread = Thread()
		self.stream = number_stream.pipe(
			ops.repeat()
		)