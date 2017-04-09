#
# David Brouwer
# david.brouwer.99@gmail.com
#
# Convert a user input to morse code
#####################################################

from code_table import code_table

class morse():
    def __init__(self):
        self.Input = ''
        self.output = []
        self.codetable = code_table()

    def setinput(self):
        self.Input = input('What do you want to convert to morse?: ')
        self.Input = self.Input.upper()

    def convert(self):
        wordcount = 0
        char_count = 0
        space_flag = False # a flag to prevent multiple spaces from adding more than one word

        for char in self.Input:
            if char != ' ':
                space_flag = False
                try:
                    self.output[wordcount] += self.codetable.return_morse(self.Input[char_count])
                except IndexError:
                    self.output.append(self.codetable.return_morse(self.Input[char_count]))
                char_count += 1
            else:
                if space_flag == 0:
                    wordcount += 1
                    char_count += 1
                    space_flag = True
                else:
                    char_count += 1
                    continue

    def returncode(self):
        for i in range(len(self.output)):
            print(self.output[i])

convertcode = morse()
convertcode.setinput()
convertcode.convert()
convertcode.returncode()



