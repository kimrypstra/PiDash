import math

import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops, scheduler
from reactivex.subject import Subject 

from .Constants import GAUGE_SAMPLE_RATE
from ..models.CANFrame import CANFrame

class MockCANService: 
	_shared = None

	kill_switch = Subject()

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared


	def __init__(self):  
		self.open_socket()


	def open_socket(self):
		print("Opening socket")
		# Later we will actually open a connection to the CAN hat 
		# For now we just set up a stream of constantly changing numbers 
		numbers = [math.sin(math.radians(x)) for x in range(360)]
		number_stream = rx.from_iterable(numbers)
		self.stream = number_stream.pipe(
				ops.repeat(),
				ops.take_until(self.kill_switch),
				ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
				ops.sample(GAUGE_SAMPLE_RATE),
				ops.map(lambda i: CANFrame(pid=1, value=i)), # later, pid will be provided by the actual CAN frame
				ops.share()
			)

	def subscribe_to_pid(self, pid):
		return self.stream.pipe(
				ops.filter(lambda frame: frame.pid == pid)
			)

	def shutdown(self):
		# Later, this should close the socket 
		# For now, just kill the ops.repeat() stream so the subscriptions can dispose cleanly
		self.kill_switch.on_next(True)