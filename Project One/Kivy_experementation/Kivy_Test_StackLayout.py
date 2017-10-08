import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.stacklayout import StackLayout

class StackLayoutApp(App):

    def build(self):
        return StackLayout()

instance = StackLayoutApp()
instance.run()