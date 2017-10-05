import kivy
# kivy.require('1.10.0')

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior

class MyLayout(BoxLayout):
    pass

class custom_ball_widgetApp(App):
    def build(self):
        window = MyLayout()
        return window

if __name__ == '__main__':
    application = custom_ball_widgetApp()
    application.run()