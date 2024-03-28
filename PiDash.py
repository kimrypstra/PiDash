import kivy
kivy.require('2.1.0')

from kivy.app import App  
from kivy.uix.label import Label

class PiDash(App): 
	def build(self):
		return Label(text="Hello there!")

if __name__ == '__main__':
	PiDash().run()