from kivy.app import App
from kivy.clock import Clock

from source.shared.CANProvider import CANProvider 
from source.shared.DisposeBag import DisposeBag

class SettingsViewModel: 

	def set_nav_controller(self, nav_controller):
		self.nav_controller = nav_controller

	def on_back(self, *kwargs): 
		self.nav_controller.back()

	def on_exit(self, *kwargs):
		CANProvider.shared().shutdown()
		dispose_bag = DisposeBag.shared()
		dispose_bag.dispose()
		Clock.schedule_once(self.stop_app, 1)

	def stop_app(self, *kwargs):
		App.get_running_app().stop()