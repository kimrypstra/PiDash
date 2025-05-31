# First, force full screen mode 
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'show_cursor', '0')

# Then start the app
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