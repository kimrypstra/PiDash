from kivy.graphics import InstructionGroup, Color, Ellipse, Line, Rotate, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.image import Image as CoreImage

from source.shared.Images import SEMICIRCLE_GAUGE_FACE, SEMICIRCLE_GAUGE_NEEDLE

from .SemicircleGaugeViewModel import SemicircleGaugeViewModel


class SemicircleGauge(AnchorLayout): 

	# Initialises an instance of SemicircleGauge, intended for displaying numerical data with a needle against a face with scale.
	#
	# Args:
	# signal (int): The CAN id we want to display in this gauge
	# alarm (lambda): A labda returning a bool indicating whether the alarm is activated
	# conversion (CANFrame) -> str: A function that converts the data from the raw CAN frame into a value displayable in the gauge
	def __init__(self, signal, alarm, conversion, title, units, **kwargs):
		super(SemicircleGauge, self).__init__(anchor_x = 'center', anchor_y = 'center', **kwargs)
		self.units = units

		self.face = Image(source = SEMICIRCLE_GAUGE_FACE, size_hint = (1.0, 1.0))
		self.add_widget(self.face)

		self.needle_texture = CoreImage(source = SEMICIRCLE_GAUGE_NEEDLE).texture
		self.needle_angle = 0
		self.needle_center = (self.center_x, self.center_y)

		with self.canvas:
			self.rot = Rotate(angle = self.needle_angle, origin = self.center)
			self.needle_rect = Rectangle(texture = self.needle_texture, size = self.needle_texture.size, pos = (self.center_x - self.needle_texture.width / 2, self.center_y - self.needle_texture.height / 2))

		self.view_model = SemicircleGaugeViewModel(signal, alarm, conversion)
		# self.bind(size = self.update_positions, pos = self.update_positions)
		self.view_model.bind(value = self.update_label)
		# self.view_model.bind(alarm = self.update_canvas)
		self.view_model.bind(angle = self.update_angle)
		self.bind(size=self.update_positions, pos=self.update_positions)

	def update_positions(self, *args):
		self.face.size = self.size
		self.face.pos = self.pos
		self.needle_center = self.center
		self.rot.origin = self.center
		self.needle_rect.pos = (self.center_x - self.needle_texture.width / 2,
								self.center_y - self.needle_texture.height / 2)

	def update_label(self, view_model, value):
		# self.label.text = value
		print(f'New value: {value}')

	def update_angle(self, view_model, value):
		self.needle_angle = value
		self.rot.angle = value
