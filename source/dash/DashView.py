import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.dash.DashViewModel import DashViewModel
from source.gauge.TextGauge import TextGauge
from source.gauge.SemicircleGauge import SemicircleGauge
from source.shared.Constants import THRESHOLD_TEST, THRESHOLD_BRAKES, BUTTON_HEIGHT
from source.shared.views.DashButton import DashButton
from source.shared.Signals import SIGNAL_TEST, SIGNAL_BRAKES
from source.shared.Conversions import CONVERSION_TEST, CONVERSION_BRAKES

NUM_OF_COLUMNS = 2

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		self.view_model = DashViewModel()

		layout = GridLayout()
		layout.cols = NUM_OF_COLUMNS
		layout.add_widget(SemicircleGauge(signal = SIGNAL_TEST, alarm = None, conversion = CONVERSION_TEST(), title = 'Boost', units = 'psi'))
		layout.add_widget(TextGauge(signal = SIGNAL_BRAKES, alarm = lambda value: value == "on", conversion = CONVERSION_BRAKES(), title = 'Brakes', units = 'on/off'))

		# Spacer
		layout.add_widget(BoxLayout(size_hint_y = None))

		button = DashButton(label="Settings", binding=self.view_model.on_settings)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)