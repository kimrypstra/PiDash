import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.dash.DashViewModel import DashViewModel
from source.gauge.NumericGauge import NumericGauge
from source.shared.Constants import THRESHOLD_TEST, BUTTON_HEIGHT
from source.shared.views.DashButton import DashButton
from source.shared.PIDs import PID_TEST
from source.shared.Conversions import CONVERSION_TEST, CONVERSION_POS_NEG

NUM_OF_COLUMNS = 2

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		self.view_model = DashViewModel()

		layout = GridLayout(padding=5)
		layout.cols = NUM_OF_COLUMNS
		layout.add_widget(NumericGauge(PID_TEST, THRESHOLD_TEST, CONVERSION_TEST, 'Boost', 'psi'))
		layout.add_widget(NumericGauge(PID_TEST, THRESHOLD_TEST, CONVERSION_POS_NEG, 'Pos/neg', '+/-'))

		# Spacer
		layout.add_widget(BoxLayout(size_hint_y=None))

		button = DashButton(label="Settings", binding=self.view_model.on_settings)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)