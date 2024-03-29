from collections import deque
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition

class NavController(BoxLayout):

	def __init__(self, **kwargs):
		super(NavController, self).__init__(**kwargs)
		self.stack = deque()
		self.screens = []
		self.screen_manager = ScreenManager()
		self.add_widget(self.screen_manager)

	def register_screen(self, screen):
		self.screen_manager.add_widget(screen)
		self.screens.append(screen.name)
		screen.set_nav_controller(self)
		if len(self.stack) == 0: 
			self.stack.append(screen.name)

	def back(self): 
		if len(self.stack) != 0:
			self.screen_manager.transition = SlideTransition(direction = 'right')
			self.stack.pop()
			self.screen_manager.current = self.stack[-1]

			print(f"Back stack: {self.stack}")

	def push(self, name):  
		if name in self.screens:
			self.screen_manager.transition = SlideTransition(direction = 'left')
			self.stack.append(name)
			self.screen_manager.current = name 

			print(f"Back stack: {self.stack}")