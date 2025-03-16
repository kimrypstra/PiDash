import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.dash.DashViewModel import DashViewModel
from source.gauge.NumericGauge import NumericGauge
from source.shared.Constants import THRESHOLD_TEST
from source.shared.PIDs import PID_TEST
from source.shared.Conversions import CONVERSION_TEST, CONVERSION_POS_NEG

NUM_OF_COLUMNS = 2

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		self.view_model = DashViewModel()

		layout = GridLayout()
		layout.cols = NUM_OF_COLUMNS
		layout.add_widget(NumericGauge(PID_TEST, THRESHOLD_TEST, CONVERSION_TEST))
		layout.add_widget(NumericGauge(PID_TEST, THRESHOLD_TEST, CONVERSION_POS_NEG))
		layout.add_widget(Label(text="Dash"))

		button = Button(text="Settings")
		button.bind(on_press=self.view_model.on_settings)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)