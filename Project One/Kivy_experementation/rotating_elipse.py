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


    def on_touch_down(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

    def on_touch_move(self, touch):
        radians = math.atan2(touch.y - self.parent.center_y, touch.x)
        self.angle = math.degrees(radians)

    def move_ellipse(self, *args):
        print("move called", self.angle)

        # ins = App.get_running_app().window.widget_var

        if self.angle < -90:
            self.direction = False

        elif self.angle > 90:
            self.direction = True

        if self.direction == True:
            self.angle -= 4

        elif self.direction == False:
            self.angle += 4


class MyGame(Widget):
    widget_var = MyWidget()



class Rotating_ElipseApp(App):
    # window = MyGame()


    def build(self):
        window = MyGame()
        # widget_var = MyWidget()
        trigger = lambda *args: Clock.schedule_interval(App.get_running_app().root.ids['widget_1'].move_ellipse, 0.0001)
        Clock.schedule_once(trigger, 1)

        return window

if __name__ == '__main__':
    application = Rotating_ElipseApp()
    application.run()