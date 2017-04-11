import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from main import morse

class gui_layout(BoxLayout):
    Height_One = StringProperty('40dp')
    morse_object = morse()

    def when_pressed(self, input):
        pass

    def convert_text(self, input):
        self.display.text = ''
        self.morse_object.external_input(input)
        #self.display.text = self.morse_object.return_input()
        self.morse_object.convert()
        output_list = self.morse_object.output_code()
        print(output_list)
        self.morse_object.returncode()

        for i in range(len(output_list)):
            self.display.text += output_list[i] + '\n'

        self.input_box.text = ''
class interfaceApp(App):

    def build(self):
        return gui_layout()

interfaceApp().run()