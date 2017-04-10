import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from main import morse

class gui_layout(BoxLayout):
    Height_One = StringProperty('40dp')
    morse_object = morse()

    def convert_text(self, input):
        self.morse_ojbect.external_input(self.morse_object, input)
        self.morse_ojbect.convert(self.morse_ojbect)

class interfaceApp(App):
    pass

interfaceApp().run()