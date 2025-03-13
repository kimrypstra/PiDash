class SettingsViewModel: 

	def set_nav_controller(self, nav_controller):
		self.nav_controller = nav_controller

	def on_back(self, *kwargs): 
		self.nav_controller.back()