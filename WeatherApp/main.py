import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *


class AddLocationForm(BoxLayout):
    Height_One = StringProperty('40dp')
    Button_Width = NumericProperty(25)
    TextBox_Width = NumericProperty(50)


class WeatherApp(App):
    #
    # pass
    def build(self):
        return AddLocationForm()

if __name__ == '__main__':
    WeatherApp().run()