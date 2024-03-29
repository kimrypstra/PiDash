import kivy

from kivy.uix.button import Button
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen 
from source.dash.DashView import DashView  
from source.settings.SettingsView import SettingsView  

# Topmost view, basically just a containter for navigation between 
# Dash and Settings etc. 
class HomeView(BoxLayout):
	def __init__(self, **kwargs):
		super(HomeView, self).__init__(**kwargs)

		self.screen_manager = ScreenManager()
		
		dash = DashView()
		settings = SettingsView()

		self.screen_manager.add_widget(dash)
		self.screen_manager.add_widget(settings)

		self.add_widget(self.screen_manager)
