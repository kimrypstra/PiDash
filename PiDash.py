import sys

# First, force full screen mode 
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'resizable', '0')


# Hide mouse cursor if running on the Pi (well, any Linux machine but who cares)
import platform
if platform.system() == 'Linux':
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

	def __init__(self, mocked=False, **kwargs):
		super().__init__(**kwargs)
		self.mocked = mocked

	def build(self):
		return HomeView(mocked=self.mocked)

if __name__ == '__main__':
	mocked = '-mocked' in sys.argv
	print(f'Mocked: {sys.argv}')

	PiDash(mocked=mocked).run()