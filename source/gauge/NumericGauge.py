from kivy.properties import Property, StringProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle

from source.shared.Constants import GAUGE_FONT_SIZE
from source.shared.Colours import COLOUR_RED, COLOUR_BLACK
from source.shared.Fonts import FONT_LARGE
from ..shared.DisposeBag import DisposeBag

class NumericGauge(BoxLayout):

	def __init__(self, pid, threshold, conversion, **kwargs):
		"""
		Initialises an instance of NumericGauge, indended for displaying numerical information _as numbers_
		like RPM, speed, or gear position etc. Not intended for graphical display of numerical information.
		I suppose you could also display text.

		Args:
			pid (int): The CAN id we want to display in this gauge
			threshold (float): A value above which the gauge turns red
			conversion (CANFrame) -> str: A function that converts the data from the raw CAN frame into a value displayable in the gauge
		"""
		super(NumericGauge, self).__init__(**kwargs)
		self.label = Label(
				text = 'initial', 
				font_name = FONT_LARGE,
				font_size = GAUGE_FONT_SIZE
			)
		self.add_widget(self.label)

		self.view_model = NumericGaugeViewModel(pid, threshold, conversion)
		self.view_model.bind(value = self.update_label)
		self.view_model.bind(alarm = self.update_canvas)

	def update_label(self, view_model, value):
		self.label.text = value

	def update_canvas(self, view_model, value):
		with self.canvas.before: 
			self.canvas.before.add(COLOUR_RED if view_model.alarm else COLOUR_BLACK)
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
