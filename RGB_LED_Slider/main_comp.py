import kivy, gpiozero
kivy.require('1.9.1')

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import *
from gpiozero import PWMLED

class CustomSliderWidget(BoxLayout):
    Value_Slider_One = '0'
    Value_Slider_Two = '0'
    Value_Slider_Three = '0'
    slider_min = NumericProperty(0)
    slider_max = NumericProperty(1)
    fontsize = NumericProperty(50)
    sliderheight = StringProperty('40dp')
    led_red = PWMLED(17)
    led_green = PWMLED(22)
    led_blue = PWMLED(27)

    def setvalue_one(self, *args):
        self.textboxone.text = str(int(args[1]))
        led_red.value = int(args[1])

    def setvalue_two(self, *args):
        self.textboxtwo.text = str(int(args[1]))
        led_green.value = int(args[1])

    def setvalue_three(self, *args):
        self.textboxthree.text = str(int(args[1]))
        led_green.value = int(args[1])

class WindowApp(App):
    def build(self):
        return CustomSliderWidget()

if __name__ == '__main__':
    window = WindowApp()
    window.run()
