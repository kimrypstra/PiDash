import kivy
from kivy.app import App  
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from source.home.HomeView import HomeView

class PiDash(App): 
	def build(self):
		return HomeView()

if __name__ == '__main__':
	PiDash().run()