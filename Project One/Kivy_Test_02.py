import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget


class CustomWidget(Widget):
    pass


class CustomWidgetApp(App):

    def build(self):
        return CustomWidget()

CustomWidgetApp().run()