
class DashViewModel: 

	def set_nav_controller(self, nav_controller):
		self.nav_controller = nav_controller

	def on_settings(self, *kwargs):
		self.nav_controller.push('Settings')