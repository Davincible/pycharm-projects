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

# TODO: use other sound library, settings page to edit sound settings, save settings in external file

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from main import morse
from kivy.uix.label import Label
import threading


class gui_layout(BoxLayout):
    Height_One = StringProperty('40dp')

    morse_object = morse()
    done_converting = False # a flag to check if the massage is encoded. The sounds waits for this flag to be true
    conversion_started = False # a flag to check if a message has been entered. Replay is not possible without a message
    switch_value = True # if the sound functionality is switched on or off, default is on
    error_flag = False # a flag to check if the sound function has thrown an error before, to reprint the message
    output_list = []
    error_list = []
    popupcontent = StringProperty('Each word will be separated by spaces.\n And each word will be separated by a newline.')
    Popupcontent = Label(text = 'Each word will be separated by spaces.\n And each word will be separated by a newline.')

    def when_pressed(self, input_1):
        print("switch state: ", self.sound_switch.active)
        T_main = threading.Thread(target=self.defthreads(input_1))
        T_main.start()

    def changevalue(self):
        if not self.sound_switch.active:
            self.switch_value = False

        else:
            self.switch_value = True

    def defthreads(self, input_1):
        T_convert = threading.Thread(target=self.convert_text(input_1))
        T_convert.start()

        if self.switch_value:
            T_sound = threading.Thread(target=self.sounds())
            T_sound.start()

    def convert_text(self, input):
        self.done_converting = False
        self.conversion_started = True
        self.display.text = ''

        if input:
            self.morse_object.external_input(input)
            self.morse_object.convert()
            self.output_list, self.error_list = self.morse_object.output_code()

            if self.error_list:
                self.display.text += 'Could not convert these characters:  '
                for e in range(len(self.error_list)):
                    self.display.text += "'" + self.error_list[e] + "'  "
                self.display.text += '\n'

            for i in range(len(self.output_list)):
                self.display.text += self.output_list[i] + '\n'

            self.done_converting = True

        else:
            self.done_converting = False
            #self.conversion_started = False

        self.input_box.text = ''


    def sounds(self):
        if not self.conversion_started:
            self.display.text = 'Please enter a message first'
            return

        while not self.done_converting: # wait for encoding to complete before playing a sound
            continue

        if self.switch_value: # only play the sound if it is switched on in the GUI
            # if self.conversion_started: # recheck if a message has been entered
                if self.error_flag:
                    # reprint the converted message if it was replaced by an error
                    self.error_flag = False
                    self.display.text = ''
                    for i in range(len(self.output_list)):
                        self.display.text += self.output_list[i] + '\n'
                self.morse_object.morse_sound()

            # else:
            #     self.display.text = 'Please enter a message first'
            #     self.error_flag = True
        else:
            self.display.text = 'Please turn the sound on first'
            self.error_flag = True

class help_popup(Popup):
    pass

class interfaceApp(App):

    def build(self):
        self.title = 'Morse Code Encoder'
        return gui_layout()

interfaceApp().run()