import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.button import Label

class HelloKivyApp(App):

    def build(self):
        return Label()

helloKivy = HelloKivyApp()

helloKivy.run()