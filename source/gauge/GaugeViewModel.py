import time 
import threading

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import Property, BooleanProperty
import reactivex as rx
from reactivex import operators as ops

from source.shared.DisposeBag import DisposeBag
from source.shared.CANProvider import CANProvider 

from abc import ABC, abstractmethod

# Base class for gauges. 
#
# Override `value` with a specific type of `Property` acceptable by your gauge. 
class GaugeViewModel(EventDispatcher, ABC):

	value = Property(None)
	alarm = BooleanProperty(False)

	def __init__(self, signal, should_alarm, conversion, **kwargs):
		super().__init__(**kwargs)
		self.should_alarm = should_alarm
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

	def set_alarm(self, new_value):
		if self.should_alarm is not None:
			self.alarm = self.should_alarm(new_value)

	@abstractmethod
	def set_value(self, can_frame):
		pass
