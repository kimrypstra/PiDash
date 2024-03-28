import kivy
kivy.require('2.1.0')

from kivy.app import App  
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from source.home.HomeView import HomeView

class PiDash(App): 
	def build(self):
		home_view = HomeView()
		layout = BoxLayout()
		layout.add_widget(home_view)

		return layout

if __name__ == '__main__':
	PiDash().run()