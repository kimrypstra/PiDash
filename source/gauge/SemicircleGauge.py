from kivy.clock import Clock
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label

from source.shared.Images import SEMICIRCLE_GAUGE_FACE, SEMICIRCLE_GAUGE_NEEDLE

from .SemicircleGaugeViewModel import SemicircleGaugeViewModel
from source.shared.Colours import COLOUR_BLACK
from source.shared.Fonts import FONT_BLACK, FONT_SIZE_GAUGE

class SemicircleGauge(AnchorLayout): 

	# Initialises an instance of SemicircleGauge, intended for displaying numerical data with a needle against a face with scale.
	#
	# Args:
	# signal (int): The CAN id we want to display in this gauge
	# alarm (lambda): A labda returning a bool indicating whether the alarm is activated
	# conversion (CANFrame) -> str: A function that converts the data from the raw CAN frame into a value displayable in the gauge
	def __init__(self, signal, alarm, conversion, title, units, min_value, max_value, **kwargs):
		super(SemicircleGauge, self).__init__(anchor_x = 'center', anchor_y = 'center', **kwargs)
		self.units = units

		self.angle_offset = 45

		self.face = Image(
			source = SEMICIRCLE_GAUGE_FACE, 
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
		self.needle_texture = CoreImage(SEMICIRCLE_GAUGE_NEEDLE).texture

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

		self.view_model = SemicircleGaugeViewModel(signal, alarm, conversion, min_value, max_value)

		self.view_model.bind(value = self.update_label)
		self.view_model.bind(angle = self.update_angle)
	# 	# self.view_model.bind(alarm = self.update_canvas)

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

	def update_angle(self, view_model, value):
		self.rotate.angle = value + self.angle_offset
		self.needle_angle = value + self.angle_offset
