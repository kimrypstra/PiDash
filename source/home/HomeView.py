import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen 
from source.dash.DashView import DashView  
from source.settings.SettingsView import SettingsView  

# Topmost view, basically just a containter for navigation between 
# Dash and Settings etc. 
class HomeView(Widget):
	def __init__(self, **kwargs):
		super(HomeView, self).__init__(**kwargs)

		self.screen_manager = ScreenManager()
		
		screen_one = DashView()
		screen_two = SettingsView()

		self.screen_manager.add_widget(screen_one)
		self.screen_manager.add_widget(screen_two)

		self.add_widget(self.screen_manager)