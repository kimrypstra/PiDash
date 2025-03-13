from kivy.properties import Property, StringProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from ..shared.DisposeBag import DisposeBag

class NumericGauge(BoxLayout):

	def __init__(self, **kwargs):
		super(NumericGauge, self).__init__(**kwargs)

		self.view_model = NumericGaugeViewModel()
		self.view_model.bind(value = self.update_text)

		self.label = Label(text = 'initial')
		self.add_widget(self.label)

	def update_text(self, value, something):
		self.label.text = something

from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import Property, StringProperty 
from source.shared.CANProvider import CANProvider 
import reactivex as rx
from reactivex import operators as ops
import time 
import threading

class NumericGaugeViewModel(EventDispatcher):

	value = StringProperty('')

	def __init__(self, **kwargs):
		super(NumericGaugeViewModel, self).__init__(**kwargs)

		self.can_provider = CANProvider.shared()

		self.start_subscription()

	def start_subscription(self):
		self.subscription = self.can_provider.subscribe_to_pid(1) \
			.subscribe(
				on_next = lambda value: Clock.schedule_once(lambda dt: self.set_value(f'{value}'))
			)

		DisposeBag.shared().add(self.subscription)

	def set_value(self, value):
		self.value = value 