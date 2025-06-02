from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

from source.shared.Constants import BUTTON_HEIGHT
from source.shared.Fonts import FONT_BOLD_ITALIC, FONT_SIZE_BUTTON
from source.shared.Images import BUTTON_BACKGROUND, BUTTON_BACKGROUND_DOWN, BUTTON_BACKGROUND_SLICE


class DashButton(BoxLayout):
	def __init__(self, label, binding, **kwargs):
		super(DashButton, self).__init__(orientation='horizontal', **kwargs)

		self.button = Button(text=label, size_hint_y=None, height=BUTTON_HEIGHT, font_name=FONT_BOLD_ITALIC, font_size=FONT_SIZE_BUTTON)
		
		self.button.background_normal = BUTTON_BACKGROUND
		self.button.background_down = BUTTON_BACKGROUND_DOWN
		self.button.border= BUTTON_BACKGROUND_SLICE
		self.button.background_color = (1, 1, 1, 1)

		self.button.bind(on_release=binding)

		self.add_widget(Widget())
		self.add_widget(self.button)
		self.add_widget(Widget())