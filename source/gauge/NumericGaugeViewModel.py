import time 
import threading

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import Property, StringProperty, BooleanProperty
import reactivex as rx
from reactivex import operators as ops

from source.shared.DisposeBag import DisposeBag
from source.shared.CANProvider import CANProvider 

class NumericGaugeViewModel(EventDispatcher):

	value = StringProperty('')
	alarm = BooleanProperty(False)

	def __init__(self, signal, threshold, conversion, **kwargs):
		super(NumericGaugeViewModel, self).__init__(**kwargs)
		self.threshold = threshold
		self.conversion = conversion
		self.signal = signal
		self.can_provider = CANProvider.shared()
		self.start_subscription()

	def start_subscription(self):
		self.subscription = self.can_provider.subscribe_to_pid(self.signal.pid) \
			.subscribe(
				on_next = lambda value: Clock.schedule_once(lambda dt: self.set_value(value))
			)
		DisposeBag.shared().add(self.subscription)

	def set_value(self, can_frame):
		# self.value = self.conversion(can_frame, self.signal)
		print(can_frame)
		value = self.conversion.convert(can_frame, self.signal)
		self.value = str(value)
		if isinstance(value, (int, float)):
			self.alarm = value >= self.threshold
		print(value)
