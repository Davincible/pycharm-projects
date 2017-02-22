import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

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

    # Declare LEDs
    try:
        RED = led_functionality(17)
        BLUE = led_functionality(22)
        GREEN = led_functionality(27)
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

    def set_value_one(self, *args):
        try:
            self.RED.set_value(args[1])
        except AttributeError:
            pass

    def set_value_two(self, *args):
        try:
            self.GREEN.set_value(args[1])
        except AttributeError:
            pass

    def set_value_three(self, *args):
        try:
            self.BLUE.set_value(args[1])
        except AttributeError:
            pass

    def reset_all(self):
        try:
            self.RED.value = 0
            self.GREEN.value = 0
            self.BLUE.value = 0
        except AttributeError:
            pass

    def set_colour(self, values):
        try:
            self.RED.value = values[0]
            self.GREEN.value = values[1]
            self.BLUE.value = values[2]
        except AttributeError:
            pass

class UserInterfaceApp(App):

    def build(self):
        return WindowLayout()

if __name__ == '__main__':
    UserInterfaceApp().run()