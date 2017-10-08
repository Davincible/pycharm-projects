import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class CustomWidget(Widget):
    two = NumericProperty(200)


class CustomWidgetApp(App):

    def build(self):
        return CustomWidget()

CustomWidgetApp().run()