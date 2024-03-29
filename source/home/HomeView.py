import kivy

from kivy.uix.boxlayout import BoxLayout
from source.shared.NavController import NavController
from source.dash.DashView import DashView  
from source.settings.SettingsView import SettingsView  

# Topmost view, basically just a containter for navigation between 
# Dash and Settings etc. 
class HomeView(BoxLayout):
	def __init__(self, **kwargs):
		super(HomeView, self).__init__(**kwargs)

		self.nav_controller = NavController()
		dash = DashView(name="Dash")
		settings = SettingsView(name="Settings")
		self.nav_controller.register_screen(dash)
		self.nav_controller.register_screen(settings)

		self.add_widget(self.nav_controller)
