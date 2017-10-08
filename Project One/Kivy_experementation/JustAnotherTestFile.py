import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import NumericProperty

build_file = Builder.load_file("JustAnotherTestFile.kv")

class RootWidget(Widget):
    two = NumericProperty(200)


class MyApp(App):
    def build(self):
        #return build_file
        return RootWidget()

if __name__ == '__main__':
    MyApp().run()