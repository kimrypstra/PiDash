class CANProvider: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self):
		self.can_service = MockCANService()

	def subscribe_to_pid(self, pid):
		# For now, just emit the stream. Later, filter on the pid
		# self.stream = self.can_service.stream
		return self.can_service.subscribe_to_pid(pid)

import math
from threading import Thread

import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops, scheduler

from .Constants import GAUGE_SAMPLE_RATE
from ..models.CANFrame import CANFrame

class MockCANService: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared


	def __init__(self):  
		# self.configure_observables()
		self.open_socket()


	def open_socket(self):
		print("Opening socket")
		# Later we will actually open a connection to the CAN hat 
		# For now we just set up a stream of constantly changing numbers 

		numbers = [math.sin(math.radians(x)) for x in range(360)]
		number_stream = rx.from_iterable(numbers)
		self.stream = number_stream.pipe(
				ops.repeat(),
				ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
				ops.sample(GAUGE_SAMPLE_RATE),
				ops.map(lambda i: CANFrame(pid=1, value=i)) # later, pid will be provided by the actual CAN frame
			)

	def subscribe_to_pid(self, pid):
		return self.stream.pipe(
				ops.filter(lambda CANFrame: CANFrame.pid == pid)
			)
