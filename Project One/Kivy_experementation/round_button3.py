import kivy

from kivy.uix.widget import Widget
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.vector import Vector
from kivy.properties import NumericProperty

class CustomButton(ButtonBehavior, FloatLayout):

    base_layout_width = NumericProperty(0)
    base_layout_height = NumericProperty(0)
    button_width = NumericProperty(0)
    button_height = NumericProperty(0)
    button_pos_x = NumericProperty(0)
    button_pos_y = NumericProperty(0)


    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.button_width / 2

    def callback(*args):
          print("i'm being pressed")

    def update_size(self, *args):
        self.base_layout_width, self.base_layout_height = self.size
        self.button_width = self.button_height = min(self.base_layout_width, self.base_layout_height)
        self.button_pos_x = self.center_x - 0.5 * self.button_width
        self.button_pos_y = self.center_y - 0.5 * self.button_height

class Round_Button3App(App):
    def build(self):
        window = CustomButton()

        return window

if __name__ == '__main__':
    app = Round_Button3App()
    app.run()
