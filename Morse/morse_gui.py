#
# April, 2017
#
# David Brouwer
# david.brouwer.99@gmail.com
#
# Convert a user input to morse code. This file contains the graphical side of this program.
#
# Run main.py to use a text-based interface
#
######################################################

# TODO: start conversion on enter, settings page to edit sound settings, save settings in external file

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from main import morse
import time
import threading


class gui_layout(BoxLayout):
    Height_One = StringProperty('40dp')
    morse_object = morse()
    done_converting = False
    conversion_started = False

    def when_pressed(self, input_1):
        T_main = threading.Thread(target=self.defthreads(input_1))
        T_main.start()

    def defthreads(self, input_1):
        T_convert = threading.Thread(target=self.convert_text(input_1))
        T_convert.start()
        T_sound = threading.Thread(target=self.sounds())
        T_sound.start()

    def convert_text(self, input):
        self.conversion_started = 1
        self.display.text = ''
        self.morse_object.external_input(input)
        # self.display.text = self.morse_object.return_input()
        self.morse_object.convert()

        output_list, error_list = self.morse_object.output_code()

        if error_list:
            self.display.text += 'Could not convert these characters:  '
            for e in range(len(error_list)):
                self.display.text += "'" + error_list[e] + "'  "
            self.display.text += '\n'

        for i in range(len(output_list)):
            self.display.text += output_list[i] + '\n'

        self.input_box.text = ''
        self.done_converting = True

    def sounds(self):
        while not self.done_converting:
            if not self.conversion_started:
                self.display.text = 'Please enter a message first'
        if self.conversion_started:
            self.morse_object.morse_sound()


class interfaceApp(App):

    def build(self):
        return gui_layout()

interfaceApp().run()