from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, PushMatrix, PopMatrix, Rotate, Rectangle, Ellipse
from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from .CircleGaugeViewModel import CircleGaugeViewModel
from source.shared.Colours import COLOUR_BLACK, COLOUR_RED
from source.shared.Constants import GAUGE_SAMPLE_RATE
from source.shared.Images import CIRCLE_GAUGE_FACE, CIRCLE_GAUGE_NEEDLE
from source.shared.Fonts import FONT_BLACK, FONT_SIZE_GAUGE

ANGLE_OFFSET = 45

class CircleGauge(AnchorLayout): 

	animated_angle = NumericProperty(0)

	# Initialises an instance of CircleGauge, intended for displaying numerical data with a needle against a face with scale.
	#
	# Args:
	# signal (int): The CAN id we want to display in this gauge
	# alarm (lambda): A lambda returning a bool indicating whether the alarm is activated
	# conversion (CANFrame) -> str: A function that converts the data from the raw CAN frame into a value displayable in the gauge
	def __init__(self, signal, alarm, conversion, title, units, min_value, max_value, **kwargs):
		super(CircleGauge, self).__init__(anchor_x = 'center', anchor_y = 'center', **kwargs)
		self.units = units

		self.face = Image(
			source = CIRCLE_GAUGE_FACE, 
			size_hint = (1.0, 1.0),
			keep_ratio = True,
			allow_stretch = False
			)
		self.add_widget(self.face)

		self.value_label = Label(
				text = '', 
				font_name = FONT_BLACK,
				font_size = FONT_SIZE_GAUGE,
			)
		self.add_widget(self.value_label)

		self.title_float = FloatLayout(size_hint=(None, None), size=(200, 0))
		self.title_label = Label(
				text = title,
				font_name = FONT_BLACK,
				font_size = FONT_SIZE_GAUGE,
				size_hint = (None, None),
				size = (200, 50),
				pos_hint = {'center_x': 0.5, 'y': 0.18}
			)
		self.title_float.add_widget(self.title_label)
		self.add_widget(self.title_float)

		self.needle_angle = 0
		self.needle_texture = CoreImage(CIRCLE_GAUGE_NEEDLE).texture

		with self.canvas:
			PushMatrix()
			self.rotate = Rotate(
				angle = self.needle_angle, 
				origin = self.center
			)
			self.needle_rect = Rectangle(
				texture = self.needle_texture, 
				size = (0, 0), 
				pos = (0, 0)
			)
			PopMatrix()

		self.bind(animated_angle=self._on_animated_angle)

		self.view_model = CircleGaugeViewModel(signal, alarm, conversion, min_value, max_value)

		self.view_model.bind(value = self.update_label)
		self.view_model.bind(angle = self.update_angle)
		self.view_model.bind(alarm = self.update_canvas)

		self.bind(pos=self.update_positions, size=self.update_size)
		Clock.schedule_once(self._force_update, 0)
		
	def _force_update(self, dt):
		if self.face.width == 0 or self.face.height == 0:
			# Try again next frame
			from kivy.clock import Clock
			Clock.schedule_once(self._force_update, 0)
			return

		self.update_size()
		self.update_positions()

	def get_rendered_face_size(self, face):
		tex_w, tex_h = face.texture.size
		w, h = face.size
		image_ratio = tex_w / tex_h

		if w == 0 or h == 0: 
			return (0, 0)

		widget_ratio = w / h

		if widget_ratio > image_ratio:
			rendered_height = h
			rendered_width = h * image_ratio
		else:
			rendered_width = w
			rendered_height = w / image_ratio

		return rendered_width, rendered_height

	def update_size(self, *args):
		rw, rh = self.get_rendered_face_size(self.face)
		self.face.size = self.size
		self.title_label.font_size = self.height * 0.15
		self.value_label.font_size = self.height * 0.15
		self.needle_rect.size = (rw, rh)
		self.title_float.size = self.size

	def update_positions(self, *args):
		self.rotate.origin = self.center
		self.face.pos = self.pos
		rw, rh = self.needle_rect.size
		self.needle_rect.pos = (
			self.center_x - rw / 2, 
			self.center_y - rh / 2
		)

	def update_label(self, view_model, value):
		self.value_label.text = f"{value:.1f}"

	def _on_animated_angle(self, instance, value):
		self.rotate.angle = value

	def update_angle(self, view_model, value):
		target_angle = value + ANGLE_OFFSET
		anim = Animation(animated_angle = target_angle, duration = GAUGE_SAMPLE_RATE, t = 'linear')
		anim.start(self)
		# self.needle_angle = target_angle
		# self.rotate.angle = value + ANGLE_OFFSET
		# self.needle_angle = value + ANGLE_OFFSET

	# def update_canvas(self, view_model, value):
	# 	with self.canvas.before: 
	# 		self.canvas.before.add(COLOUR_RED if view_model.alarm else COLOUR_BLACK)
	# 		self.rect = Rectangle(pos = self.pos, size = self.size)

	def update_canvas(self, view_model, value):
		self.canvas.before.clear()
		with self.canvas.before:
			if view_model.alarm:
				Color(1, 0, 0, 1)
				w, h = (self.width, self.height)
				self.circle = Ellipse(
					pos = (self.center_x - h / 2, self.center_y - h / 2),
					size = (h, h)
				)

			else: 
				Color(0, 0, 0, 1)
				self.rect = Rectangle(pos = self.pos, size = self.size)
