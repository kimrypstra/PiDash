from kivy.properties import Property, StringProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle

from source.shared.Constants import COLOUR_RED, COLOUR_BLACK, GAUGE_FONT_SIZE

from ..shared.DisposeBag import DisposeBag

class NumericGauge(BoxLayout):

	def __init__(self, **kwargs):
		super(NumericGauge, self).__init__(**kwargs)

		self.view_model = NumericGaugeViewModel()
		self.view_model.bind(value = self.update_canvas)

		self.label = Label(
				text = 'initial', 
				font_name = 'res/fonts/TitilliumWeb-Black.ttf',
				font_size = GAUGE_FONT_SIZE
			)
		self.add_widget(self.label)

	def update_canvas(self, value, something):
		self.label.text = something
		with self.canvas.before:  # `before` ensures it’s drawn behind other elements
			self.canvas.before.add(COLOUR_RED if self.view_model.alarm else COLOUR_BLACK)
			self.rect = Rectangle(pos = self.pos, size = self.size)

from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import Property, StringProperty, BooleanProperty
from source.shared.CANProvider import CANProvider 
import reactivex as rx
from reactivex import operators as ops
import time 
import threading

class NumericGaugeViewModel(EventDispatcher):

	value = StringProperty('')
	alarm = BooleanProperty(False)

	def __init__(self, **kwargs):
		super(NumericGaugeViewModel, self).__init__(**kwargs)

		self.can_provider = CANProvider.shared()

		self.start_subscription()

	def start_subscription(self):
		self.subscription = self.can_provider.subscribe_to_pid(1) \
			.subscribe(
				on_next = lambda value: Clock.schedule_once(lambda dt: self.set_value(value))
			)

		DisposeBag.shared().add(self.subscription)

	def set_value(self, value):
		formatted = f'{value.value:.1f}'
		self.value = formatted 

		threshold = 0.5
		self.alarm = value.value > threshold