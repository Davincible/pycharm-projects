import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class GridApp(App):

    def build(self):
        return GridLayout()

GridApp().run()