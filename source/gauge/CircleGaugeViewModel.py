from kivy.properties import NumericProperty

from .GaugeViewModel import GaugeViewModel 

MIN_ANGLE = 0
MAX_ANGLE = 270

class CircleGaugeViewModel(GaugeViewModel):

	value = NumericProperty(0)
	angle = NumericProperty(1)

	def __init__(self, signal, should_alarm, conversion, min_value, max_value,  **kwargs):
		super().__init__(signal, should_alarm, conversion, **kwargs)
		self.min_value = min_value
		self.max_value = max_value
		self.value_range = max_value - min_value

		self.angle_range = MAX_ANGLE - MIN_ANGLE

	def set_value(self, can_frame):
		converted_value = self.conversion.convert(can_frame, self.signal)

		clamped = min(self.max_value, max(self.min_value, converted_value))
		percent = (clamped - self.min_value) / self.value_range
		angle = percent * MAX_ANGLE
		print(f'Value: {clamped}; %: {percent}; Angle: {angle}')
		self.angle = -angle

		self.value = converted_value

		super().set_alarm(self.value)
