from abc import ABC, abstractmethod
import logging
import math
import struct

from can import Bus, Listener, Notifier, BufferedReader
import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops, scheduler
from reactivex.subject import Subject 

from .Constants import GAUGE_SAMPLE_RATE
from ..models.CANFrame import CANFrame
from .DisposeBag import DisposeBag

class BaseCANService(ABC):
	_shared = None

	# Emit on _kill_switch to stop subscriptions, allowing subscribers to cleanly dispose
	_kill_switch = Subject()

	# Internal stream that carries all CAN traffic emitted from the bus. Do not subscribe to this, 
	# instead call subscribe_to_pid to receive a filtered subscription
	_can_stream = Subject()

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self): 
		self.connect()

	# Closes connection to the CANBUS and stops emission of CANFrames on subscriptions 
	@abstractmethod
	def shutdown(self):
		pass

	# Opens connection to the CANBUS
	@abstractmethod
	def connect(self):
		pass

	# Returns a subscription to the common stream filtered for the provided id 
	@abstractmethod
	def subscribe_to_pid(self, pid):
		pass


class CANService(BaseCANService, Listener): 

	def connect(self):
		print("Connecting to CAN interface")
		self.bus = Bus(channel='can0', bustype='socketcan')
		self.bus.set_filters([])
		self.notifier = Notifier(self.bus, [self])
		logging.getLogger("can").setLevel(logging.WARNING)

	def on_message_received(self, msg):
		print(f"ID: {hex(msg.arbitration_id)} Data: {msg.data}")
		self._can_stream.on_next(CANFrame(pid=msg.arbitration_id, data=msg.data))

	def subscribe_to_pid(self, pid):
		print(f"Subscribing to pid: {pid}")
		self.bus.set_filters([{"can_id": pid, "can_mask": 0x7FF}])
		return self._can_stream.pipe(
			ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
			ops.filter(lambda frame: frame.pid == pid),
			ops.distinct_until_changed(),
			ops.take_until(self._kill_switch),
		)

	def shutdown(self):
		# Kill the main stream so subscriptions can be disposed cleanly 
		self._kill_switch.on_next(True)
		# Kill the CAN connection
		self.notifier.stop()
		self.bus.shutdown()

class MockCANService(BaseCANService): 

	def connect(self):
		print("Connecting mocked service")
		numbers = [math.sin(math.radians(x)) for x in range(360)]
		self.number_stream = rx.from_iterable(numbers).pipe(
			ops.repeat(),
			ops.take_until(self._kill_switch),
			ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
			ops.sample(GAUGE_SAMPLE_RATE),
			# ops.map(lambda i: CANFrame(pid=0x1, data=int(i * 10000).to_bytes(length=8, byteorder='big', signed=True))),
			ops.map(lambda i: CANFrame(pid = 0x601, data = struct.pack('>d', i))),
			ops.share()
		).subscribe(on_next=self._can_stream.on_next)
		DisposeBag.shared().add(self.number_stream)

	def subscribe_to_pid(self, pid):
		return self._can_stream.pipe(
			ops.filter(lambda frame: frame.pid == pid)
		)

	def shutdown(self):
		self._kill_switch.on_next(True)