from kivy.properties import StringProperty

from .GaugeViewModel import GaugeViewModel 

class TextGaugeViewModel(GaugeViewModel):

	value = StringProperty('')

	def __init__(self, signal, should_alarm, conversion, **kwargs):
		super().__init__(signal, should_alarm, conversion, **kwargs)

	def set_value(self, can_frame):
		new_value = self.conversion.convert(can_frame, self.signal)
		self.value = str(new_value)
		super().set_alarm(self.value)
