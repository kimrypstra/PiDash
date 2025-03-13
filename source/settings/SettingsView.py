import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.settings.SettingsViewModel import SettingsViewModel

class SettingsView(Screen):
	def __init__(self, **kwargs):
		super(SettingsView, self).__init__(**kwargs)

		self.view_model = SettingsViewModel()

		layout = BoxLayout()

		label = Label(text = "Settings")
		layout.add_widget(label)

		button = Button(text = "Back")
		button.bind(on_press = self.view_model.on_back)
		layout.add_widget(button)

		self.add_widget(layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)