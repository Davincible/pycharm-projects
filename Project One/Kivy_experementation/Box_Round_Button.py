import kivy

from kivy.uix.widget import Widget
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color
from kivy.clock import Clock

class CustomButton(ButtonBehavior, FloatLayout):


    # set dynamic spacing
    base_layout_width = NumericProperty(0)
    base_layout_height = NumericProperty(0)
    button_width = NumericProperty(0)
    button_height = NumericProperty(0)
    button_pos_x = NumericProperty(0)
    button_pos_y = NumericProperty(0)
    text = StringProperty('default')
    color = ListProperty([0, 0, 0, 1])
    font_size = NumericProperty('30sp')


    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

        with self.canvas:
            Color(1, 0, 0, 1)
            Rectangle(pos=map(lambda x: x+ 50, self.pos), size=(100, 100))
            print('red created')



    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.button_width / 2

    def callback(*args):
          print("i'm being pressed")

    def update_size(self, *args):
        self.base_layout_width, self.base_layout_height = self.size
        self.button_width = self.button_height = min(self.base_layout_width, self.base_layout_height)
        self.button_pos_x = self.center_x - 0.5 * self.button_width
        self.button_pos_y = self.center_y - 0.5 * self.button_height

class WindowLayout(BoxLayout):
    source_ = ''

    def _update_source(self, x):
        # self.source_ = 'C:/Users/David.MIDDENAARDE/Pictures/Textures/football.png'
        self.ids.image_button.source = 'C:/Users/David.MIDDENAARDE/Pictures/Textures/football.png'
        print('updated source')

    def __init__(self, **kwargs):
        super(WindowLayout, self).__init__(**kwargs)

        Clock.schedule_once(self._update_source, 5)
        # self.bind(self.source_=self.ids.image_button.source.setter())

class Box_Round_ButtonApp(App):
    def build(self):
        window = WindowLayout()

        return window

if __name__ == '__main__':
    app = Box_Round_ButtonApp()
    app.run()
