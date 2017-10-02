import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.clock import Clock
import math


class MyWidget(Widget):
    """My Widget represents a circle and a rotating ellipse
    """
    angle = NumericProperty(0)
    width_ball = NumericProperty(400)
    height_ball = NumericProperty(400)
    ball_size = ReferenceListProperty(width_ball, height_ball)
    width_ellipse = NumericProperty(50)
    height_ellipse = NumericProperty(50)
    ellipse_size = ReferenceListProperty(width_ellipse, height_ellipse)
    direction = True
    speed = 10


    def on_touch_down(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

    def on_touch_move(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

    def move_ellipse(self, *args):
        if self.angle < -90:
            self.direction = False

        elif self.angle > 90:
            self.direction = True

        if self.direction:
            self.angle -= self.speed

        elif not self.direction:
            self.angle += self.speed


class MyGame(Widget):
    widget_var = MyWidget()


class Rotating_EllipseApp(App):

    def build(self):
        window = MyGame()
        # widget_var = MyWidget()
        trigger = lambda *args: Clock.schedule_interval(App.get_running_app().root.ids['widget_1'].move_ellipse, 0.0001)
        Clock.schedule_once(trigger, 0.01)

        return window


if __name__ == '__main__':
    application = Rotating_EllipseApp()
    application.run()