import kivy
kivy.require('1.9.1')

try:
    import gpiozero
    from gpiozero import PWMLED
except ImportError:
    print('Not on Pi')

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import *

class CustomSliderWidget(BoxLayout):
    Value_Slider_One = '0'
    Value_Slider_Two = '0'
    Value_Slider_Three = '0'
    slider_min = NumericProperty(0)
    slider_max = NumericProperty(1)
    fontsize = NumericProperty(50)
    sliderheight = StringProperty('40dp')

    try:
        led_red = PWMLED(12) #17
        led_green = PWMLED(23) #22
        led_blue = PWMLED(24) #27
    except NameError:
        pass

    def setvalue_one(self, *args):
        self.textboxone.text = str(float(format(args[1], '.5f')))
        try:
            led_red.value = float(args[1])
        except NameError:
            pass

    def setvalue_two(self, *args):
        self.textboxtwo.text = str(float(format(args[1], '.5f')))
        try:
            led_green.value = float(args[1])
        except NameError:
            pass

    def setvalue_three(self, *args):
        self.textboxthree.text = str(float(format(args[1],'.5f')))
        try:
            led_green.value = float(args[1])
        except NameError:
            pass

class WindowApp(App):
    def build(self):
        return CustomSliderWidget()

if __name__ == '__main__':
    window = WindowApp()
    window.run()
