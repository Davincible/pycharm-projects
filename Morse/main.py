#
# April, 2017
#
# David Brouwer
# david.brouwer.99@gmail.com
#
# Convert a user input to morse code
#
# Run morse_gui.py for a graphical user interface.
#
######################################################

from code_table import code_table
import pygame
import time

class morse():
    def __init__(self):
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.init()
        pygame.init()

        self.Input = ''
        self.output = []
        self.codetable = code_table()
        self.error_index = []
        self.sounds = [(pygame.mixer.Sound('dit.wav')), (pygame.mixer.Sound('dah.wav'))]


    def setinput(self):
        self.Input = input('What do you want to convert to morse?: ')
        self.Input = self.Input.upper()

    def external_input(self, input):
        self.Input = input
        self.Input = self.Input.upper()

    def return_input(self):
        return self.Input

    def convert(self):
        wordcount = 0
        char_count = 0
        space_flag = False # a flag to prevent multiple spaces from adding more than one word
        first_flag = True # prevents adding new words if one or more spaces are the first characters in a string
        self.output = [] # reset the output, else the new output will be build upon the old. 
        self.error_index = [] # reset the error list at the beginning of every conversion

        for char in self.Input:

            if char != ' ':
                try:
                    first_flag = False
                    space_flag = False
                    try:
                        self.output[wordcount] += self.codetable.return_morse(self.Input[char_count], True)
                    except IndexError:
                        self.output.append(self.codetable.return_morse(self.Input[char_count], True))
                    char_count += 1

                except KeyError:
                    space_flag = True #why is this flag here?

                    if __name__ == '__main__':
                        print('Cannot convert this character to morse: ', self.Input[char_count])
                    else:
                            self.error_index.append(self.Input[char_count])
                    char_count += 1

            else:
                if space_flag == 0 and first_flag == 0:
                    wordcount += 1
                    char_count += 1
                    space_flag = True
                else:
                    char_count += 1
                    continue

    def morse_sound(self):
        last_z = 0
        last_i = 0

        for z in range(len(self.output)):

            if z > last_z:
                time.sleep(0.8)

            for i in range(len(self.output[z])):

                if self.output[z][i] == ' ':
                    time.sleep(0.2)
                if self.output[z][i] == '.':
                    self.sounds[0].play()
                    while pygame.mixer.get_busy() == True:
                        continue
                    time.sleep(0.1)

                elif self.output[z][i] == '-':
                    self.sounds[1].play()
                    while pygame.mixer.get_busy() == True:
                        continue
                    time.sleep(0.1)
                last_i = i
            last_z = z

    def output_code(self):
        return self.output, self.error_index
        #for i in range(len(self.output)):
         #    return self.output[i] # kan je return wel in een for loop zetten?

    def printcode(self):
        for i in range(len(self.output)):
            print(self.output[i])

    def printlist(self):
        print(self.output)

if __name__ == '__main__':
    convertcode = morse()
    convertcode.setinput()
    convertcode.convert()
    convertcode.printcode()
    convertcode.morse_sound()


