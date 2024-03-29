import kivy

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen 
from source.dash.DashViewModel import DashViewModel

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		self.view_model = DashViewModel()

		layout = GridLayout()
		layout.cols = 2
		layout.add_widget(Label(text="Dash"))
		layout.add_widget(Label(text="Dash"))
		layout.add_widget(Label(text="Dash"))

		button = Button(text="Settings")
		button.bind(on_press=self.view_model.on_settings)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)