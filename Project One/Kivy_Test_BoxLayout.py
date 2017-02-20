import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

class CustomWidget(BoxLayout):
    size_one = NumericProperty(50)

class BoxLayoutApp(App):

    def build(self):
        return CustomWidget()

BoxLayoutApp().run()

