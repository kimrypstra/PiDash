from kivy.properties import Property, StringProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from source.shared.Colours import COLOUR_RED, COLOUR_BLACK
from source.shared.Fonts import FONT_BLACK, FONT_SEMIBOLD, FONT_SIZE_TITLE, FONT_SIZE_GAUGE

from .TextGaugeViewModel import TextGaugeViewModel

class TextGauge(BoxLayout):

	# Initialises an instance of StringGauge, intended for displaying arbitrary data as text.
	#
	# Args:
	# signal (int): The CAN id we want to display in this gauge
	# alarm (lambda): A labda returning a bool indicating whether the alarm is activated
	# conversion (CANFrame) -> str: A function that converts the data from the raw CAN frame into a value displayable in the gauge
	def __init__(self, signal, alarm, conversion, title, units, **kwargs):
		super(TextGauge, self).__init__(**kwargs)

		self.units = units

		v_stack = BoxLayout(orientation = 'vertical', padding = 50, spacing = 0)

		self.title_label = Label(
				text = title, 
				font_name = FONT_SEMIBOLD,
				font_size = FONT_SIZE_TITLE,
				# size_hint_y = 0.1,
			)
		v_stack.add_widget(self.title_label)

		self.label = Label(
				text = '', 
				font_name = FONT_BLACK,
				font_size = FONT_SIZE_GAUGE,
				# size_hint_y = 1
			)
		v_stack.add_widget(self.label)

		self.units_label = Label(
				text = units, 
				font_name = FONT_SEMIBOLD,
				font_size = FONT_SIZE_TITLE,
				# size_hint_y = 0.1
			)
		v_stack.add_widget(self.units_label)

		self.add_widget(v_stack)

		self.view_model = TextGaugeViewModel(signal, alarm, conversion)
		self.view_model.bind(value = self.update_label)
		self.view_model.bind(alarm = self.update_canvas)

	def update_label(self, view_model, value):
		self.label.text = value

	def update_canvas(self, view_model, value):
		with self.canvas.before: 
			self.canvas.before.add(COLOUR_RED if view_model.alarm else COLOUR_BLACK)
			self.rect = Rectangle(pos = self.pos, size = self.size)

