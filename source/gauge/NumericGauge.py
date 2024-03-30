from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import Property, StringProperty 

class NumericGauge(BoxLayout):

	def __init__(self, **kwargs):
		super(NumericGauge, self).__init__(**kwargs)

		self.view_model = NumericGaugeViewModel()
		self.view_model.bind(value = self.update_text)
		self.label = Label(text = 'initial')
		self.add_widget(self.label)

	def update_text(self, value, something):
		print(f'setting value {value}')
		self.label.text = something

from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import Property, StringProperty 
from source.shared.CANProvider import CANProvider 
import reactivex as rx
from reactivex.scheduler import ThreadPoolScheduler
from reactivex import operators as ops
import time 

class NumericGaugeViewModel(EventDispatcher):

	value = StringProperty('')

	def __init__(self, **kwargs):
		super(NumericGaugeViewModel, self).__init__(**kwargs)

		self.can_provider = CANProvider.shared()
		thread_pool_scheduler = ThreadPoolScheduler()
		self.subscription = self.can_provider.stream \
			.pipe (
				ops.subscribe_on(thread_pool_scheduler)
			) \
			.subscribe(
				on_next = lambda value: Clock.schedule_once(lambda dt: self.set_value(f'{value}'))
		)

	def set_value(self, value):
		print(value)
		self.value = value 