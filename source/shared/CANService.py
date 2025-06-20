import math

from can import Bus, Listener, Notifier, BufferedReader
import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops, scheduler
from reactivex.subject import Subject 

from .Constants import GAUGE_SAMPLE_RATE
from ..models.CANFrame import CANFrame

class CANService: 
	_shared = None

	kill_switch = Subject()
	can_subject = Subject()

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self):  
		self.connect()

	def connect(self):
		print("Connecting to CAN interface")
		self.bus = Bus(channel='can0', bustype='socketcan')
		self.bus.set_filters([{"can_id": 0x514, "can_mask": 0x7FF}]) # Temporarily only allow 514 through. Set this in the subscribe func if it works
		self.reader = BufferedReader()
		self.notifier = Notifier(self.bus, [self.reader])

		self.reader_poller = rx.interval(GAUGE_SAMPLE_RATE).pipe(
		    ops.map(lambda _: self.reader.get_message(timeout=0.0)),
		    ops.filter(lambda msg: msg is not None),
		    ops.share()
		).subscribe(on_next=self.on_message_received)

		self.stream = self.can_subject.pipe(
			ops.take_until(self.kill_switch),
			ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
			ops.sample(GAUGE_SAMPLE_RATE),
			ops.share()
		)

	def on_message_received(self, msg):
		print(f"ID: {hex(msg.arbitration_id)} Data: {msg.data}")
		self.can_subject.on_next(CANFrame(pid=msg.arbitration_id, data=msg.data))

	# Returns a subscription to the common stream filtered for the provided id 
	def subscribe_to_pid(self, pid):
		return self.stream.pipe(
			ops.filter(lambda frame: frame.pid == pid)
		)

	def shutdown(self):
		# Kill the main stream so subscriptions can be disposed cleanly 
		self.kill_switch.on_next(True)
		# Kill the CAN connection
		self.notifier.stop()
		self.bus.shutdown()

class MockCANService: 
	_shared = None

	kill_switch = Subject()

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self):  
		self.connect()

	def connect(self):
		print("Faking it")
		# Later we will actually open a connection to the CAN hat 
		# For now we just set up a stream of constantly changing numbers 
		numbers = [math.sin(math.radians(x)) for x in range(360)]
		number_stream = rx.from_iterable(numbers)
		self.stream = number_stream.pipe(
				ops.repeat(),
				ops.take_until(self.kill_switch),
				ops.subscribe_on(scheduler.ThreadPoolScheduler(1)),
				ops.sample(GAUGE_SAMPLE_RATE),
				ops.map(lambda i: CANFrame(pid=1, data=int(i * 10).to_bytes(length=2, byteorder='big', signed=True))), # later, pid will be provided by the actual CAN frame
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