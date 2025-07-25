import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.dash.DashViewModel import DashViewModel
from source.gauge.TextGauge import TextGauge
from source.gauge.CircleGauge import CircleGauge
from source.shared.Constants import THRESHOLD_TEST, THRESHOLD_BRAKES, BUTTON_HEIGHT
from source.shared.views.DashButton import DashButton
from source.shared.Signals import SIGNAL_TEST, SIGNAL_BRAKES, SIGNAL_MAP
from source.shared.Conversions import CONVERSION_TEST, CONVERSION_BRAKES, CONVERSION_PASSTHROUGH_INT

NUM_OF_COLUMNS = 3

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		self.view_model = DashViewModel()

		layout = GridLayout()
		layout.cols = NUM_OF_COLUMNS
		layout.add_widget(CircleGauge(signal = SIGNAL_MAP, alarm = None, conversion = CONVERSION_PASSTHROUGH_INT(), title = 'MAP', units = 'psi', min_value = 0, max_value = 25))
		# layout.add_widget(CircleGauge(signal = SIGNAL_TEST, alarm = None, conversion = CONVERSION_TEST(), title = 'Boost', units = 'psi', min_value = 0, max_value = 100))
		layout.add_widget(TextGauge(signal = SIGNAL_BRAKES, alarm = lambda value: value == "on", conversion = CONVERSION_BRAKES(), title = 'Brakes', units = 'on/off'))

		# Spacer
		layout.add_widget(BoxLayout(size_hint_y = None))

		button = DashButton(label="Settings", binding=self.view_model.on_settings)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)