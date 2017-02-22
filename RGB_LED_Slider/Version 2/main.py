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
        pass
except NameError:
    pass

class WindowLayout(BoxLayout):
    slidermin = NumericProperty(0)
    slidermax = NumericProperty(1)
    sliderstart = NumericProperty(0)

class UserInterfaceApp(App):

    def build(self):
        return WindowLayout()

if __name__ == '__main__':
    UserInterfaceApp().run()