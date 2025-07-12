from kivy.properties import NumericProperty

from .GaugeViewModel import GaugeViewModel 

class SemicircleGaugeViewModel(GaugeViewModel):

	value = NumericProperty(0)
	angle = NumericProperty(1)

	def __init__(self, signal, should_alarm, conversion, min_value, max_value,  **kwargs):
		super().__init__(signal, should_alarm, conversion, **kwargs)
		self.min_value = min_value
		self.max_value = max_value
		self.value_range = max_value - min_value

		self.min_angle = 0
		self.max_angle = 270
		self.angle_range = self.max_angle - self.min_angle 

		self.fake_new_angle = 0 

	# This is pretty much the same here... why can't it be in the base view model? Would it ever change? All the magic happens in the conversion
	def set_value(self, can_frame):
		new_value = self.conversion.convert(can_frame, self.signal)

		# Angle
		# force it between the swing
		if self.fake_new_angle == 0:
			self.fake_new_angle = 270
		else:
			self.fake_new_angle = 0

		# clamped = max(self.min_value, self.fake_new_angle)
		clamped = max(self.min_value, new_value)
		percent = (clamped - self.min_value) / self.value_range
		angle = percent * self.max_angle
		print(f'Value: {clamped}; %: {percent}; Angle: {angle}')
		self.angle = -angle

		# Text
		self.value = new_value

		super().set_alarm(self.value)
