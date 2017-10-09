import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.clock import Clock

build_file = Builder.load_file("JustAnotherTestFile.kv")

class RootWidget(BoxLayout):
    two = NumericProperty(200)
    #float_size = ReferenceListProperty()


class MyApp(App):
    def build(self):
        window = RootWidget()
        #return build_file
        Clock.schedule_once(lambda *args: Clock.schedule_interval(lambda *args: print(MyApp.get_running_app().root.size), 1), 2)
        return window

if __name__ == '__main__':
    MyApp().run()