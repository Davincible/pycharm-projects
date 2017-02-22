import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.widget import Widget

try:
    import gpiozero
    from gpiozero import PWMLED
except ImportError:
    print('Library gpiozero not imported')

try:
    class led_functionality(PWMLED):
        def __init__(self, pin):
            self.led = PWMLED(pin)

        def set_value(self, value):
            self.led.value = value
except NameError:
    pass

class WindowLayout(BoxLayout):
    #def __init__(self, **kwargs):
       # self.my = App.get_running_app()#.my
    #a = App.get_running_app().windowlayout

    # Declare LEDs
    try:
        RED = led_functionality(17)
        GREEN = led_functionality(22)
        BLUE = led_functionality(27)
    except NameError:
        pass

    # Colour Properties
    the_natural = (0.0, 0.50196, 0.50196)
    light_blue = (0.2, 1, 1)
    dark_blue = (0.2, 0.2, 1.0)
    orange = (1.0, 0.270588235, 0)
    purple = (0.498, 0, 1)
    bordeaux = (0.4, 0, 0.2)

    # Slider properties
    slidermin = NumericProperty(0)
    slidermax = NumericProperty(1)
    sliderstart = NumericProperty(0)

    def set_value_one(self, args):
        try:
            self.RED.set_value(args)
            self.sliderone.value_pos = args
        except AttributeError:
            pass

    def set_value_two(self, args):
        try:
            self.GREEN.set_value(args)
        except AttributeError:
            pass

    def set_value_three(self, args):
        try:
            self.BLUE.set_value(args)
        except AttributeError:
            pass

    def reset_all(self):
        try:
            self.RED.set_value(0)
            self.GREEN.set_value(0)
            self.BLUE.set_value(0)
        except AttributeError:
            pass

    def set_colour(self, values):
        try:
            self.RED.set_value(values[0])
            self.GREEN.set_value(values[1])
            self.BLUE.set_value(values[2])
        except AttributeError:
            pass



class UserInterfaceApp(App):

    windowlayout = WindowLayout()
   # my = WindowLayout()

    def build(self):
        return WindowLayout()

if __name__ == '__main__':
    UserInterfaceApp().run()