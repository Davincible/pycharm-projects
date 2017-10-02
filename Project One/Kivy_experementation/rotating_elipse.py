import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
import math


class MyWidget(Widget):
    """My Widget represents a circle and a rotating ellipse
    """
    angle = NumericProperty(0)
    width_ball = NumericProperty(40)
    height_ball = NumericProperty(40)
    ball_size = ReferenceListProperty(width_ball, height_ball)
    width_ellipse = NumericProperty(100)
    height_ellipse = NumericProperty(20)
    ellipse_size = ReferenceListProperty(width_ellipse, height_ellipse)


    def on_touch_down(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

    def on_touch_move(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

class MyGame(Widget):
    pass

class Rotating_ElipseApp(App):
    def build(self):
        window = MyGame()
        return window

if __name__ == '__main__':
    application = Rotating_ElipseApp()
    application.run()