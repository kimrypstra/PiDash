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

	def __init__(self, pid, threshold, conversion, **kwargs):
		super(NumericGaugeViewModel, self).__init__(**kwargs)
		self.threshold = threshold
		self.conversion = conversion
		self.pid = pid
		self.can_provider = CANProvider.shared()
		self.start_subscription()

	def start_subscription(self):
		self.subscription = self.can_provider.subscribe_to_pid(self.pid) \
			.subscribe(
				on_next = lambda value: Clock.schedule_once(lambda dt: self.set_value(value))
			)
		DisposeBag.shared().add(self.subscription)

	def set_value(self, can_frame):
		self.value = self.conversion(can_frame)
		self.alarm = can_frame.value >= self.threshold
