import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen 

class DashView(Screen):
	def __init__(self, **kwargs):
		super(DashView, self).__init__(**kwargs)

		layout = BoxLayout()
		layout.add_widget(Label(text="Dash"))

		self.add_widget(layout)