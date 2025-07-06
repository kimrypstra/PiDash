from kivy.properties import NumericProperty

from .GaugeViewModel import GaugeViewModel 

class SemicircleGaugeViewModel(GaugeViewModel):

	value = NumericProperty(0)
	angle = NumericProperty(1)

	def __init__(self, signal, should_alarm, conversion, **kwargs):
		super().__init__(signal, should_alarm, conversion, **kwargs)

	# This is pretty much the same here... why can't it be in the base view model? Would it ever change? All the magic happens in the conversion
	def set_value(self, can_frame):
		new_value = self.conversion.convert(can_frame, self.signal)
		self.value = float(new_value)
		self.angle = float(90)
		super().set_alarm(self.value)
