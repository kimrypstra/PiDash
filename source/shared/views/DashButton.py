from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

from source.shared.Constants import BUTTON_HEIGHT
from source.shared.Fonts import FONT_BOLD_ITALIC, FONT_SIZE_BUTTON


class DashButton(BoxLayout):
	def __init__(self, label, binding, **kwargs):
		super(DashButton, self).__init__(padding=50, **kwargs)

		self.button = Button(text=label, size_hint_y=None, height=BUTTON_HEIGHT, font_name = FONT_BOLD_ITALIC, font_size = FONT_SIZE_BUTTON)
		self.button.background_normal = ''
		self.button.background_color = (0, 0, 0, 0)
		self.button.bind(on_press=binding)

		self.add_widget(self.button)