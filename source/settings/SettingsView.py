import kivy

from kivy.uix.label import Label
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen 

class SettingsView(Screen):
	def __init__(self, **kwargs):
		super(SettingsView, self).__init__(**kwargs)

		layout = BoxLayout()
		layout.add_widget(Label(text="Settings"))

		self.add_widget(layout)