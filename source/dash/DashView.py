import kivy

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen 

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		layout = GridLayout()
		layout.cols = 2
		layout.add_widget(Label(text="Dash"))
		layout.add_widget(Label(text="Dash"))
		layout.add_widget(Label(text="Dash"))
		layout.add_widget(Button(text="Settings"))

		self.add_widget(layout)