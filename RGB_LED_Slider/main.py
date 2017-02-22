import kivy
kivy.require('1.9.1')

try:
    import gpiozero
    from gpiozero import PWMLED
    print('Import of gpiozero succesfull')
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
        led_red = PWMLED(17) #17
        led_green = PWMLED(22) #22
        led_blue = PWMLED(27) #27
        print("successfully declared PWM LEDs")

    except NameError:
        pass

    def setvalue_one(self, *args):
        self.textboxone.text = str(float(format(args[1], '.5f')))
        
        value_output = float(args[1])
        try:
            self.led_red.value = value_output
            print('Changed the value of the Red LED')
        except AttributeError:
            print('Value change not succesful ', value_output)

    def setvalue_two(self, *args):
        self.textboxtwo.text = str(float(format(args[1], '.5f')))
        try:
            self.led_green.value = float(args[1])
            print('Changed the value of the Green LED')
        except AttributeError:
            pass

    def setvalue_three(self, *args):
        self.textboxthree.text = str(float(format(args[1],'.5f')))
        try:
            self.led_blue.value = float(args[1])
            print('Changed the value of the Blue LED')
        except AttributeError:
            pass

class WindowApp(App):
    def build(self):
        return CustomSliderWidget()

if __name__ == '__main__':
    window = WindowApp()
    window.run()
