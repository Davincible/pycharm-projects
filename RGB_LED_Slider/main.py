import kivy
kivy.require('1.9.1')

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import *

class Slider():
    def __init__(self, identity):
        self.slider_value = identity.value
        id = identity

    def set_text(self):
        pass #return id.

class CustomSliderWidget(BoxLayout):
    Value_Slider_One = '0'
    Value_Slider_Two = '0'
    Value_Slider_Three = '0'
    fontsize = NumericProperty(50)
    sliderheight = StringProperty('40dp')

    def setvalue_one(self, *args):
        self.textboxone.text = str(int(args[1]))

    def setvalue_two(self, *args):
        self.textboxtwo.text = str(int(args[1]))

    def setvalue_three(self, *args):
        self.textboxthree.text = str(int(args[1]))



    # sliderONE = Slider('slider_one')
    # sliderTWO = Slider('slider_two')
    # sliderTHREE = Slider('slider_three')

    def SetSliderValue(self, num_slider, value):
        pass#self.Value_Slider_'num_slider' = value

class WindowApp(App):
    def build(self):
        return CustomSliderWidget()

#if "__name__" == '__main__':
window = WindowApp()
window.run()