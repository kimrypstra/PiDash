import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen 
from kivy.uix.widget import Widget 

from source.settings.SettingsViewModel import SettingsViewModel
from source.shared.views.DashButton import DashButton
from source.shared.Fonts import FONT_SEMIBOLD, FONT_SIZE_TITLE

class SettingsView(Screen):
	def __init__(self, **kwargs):
		super(SettingsView, self).__init__(**kwargs)

		self.view_model = SettingsViewModel()
		self.layout = BoxLayout(orientation = 'vertical', padding = 0, spacing = 30)

		label = Label(
			text = "Settings",
			font_name = FONT_SEMIBOLD,
			font_size = FONT_SIZE_TITLE,
		)
		label.size_hint_y = 0.2
		self.layout.add_widget(label)

		exit_button = DashButton(label="Quit", binding=self.view_model.on_exit)
		self.layout.add_widget(exit_button)

		back_button = DashButton(label="Back", binding=self.view_model.on_back)
		self.layout.add_widget(back_button)

		self.add_widget(self.layout)

	def set_nav_controller(self, nav_controller):
		self.view_model.set_nav_controller(nav_controller)