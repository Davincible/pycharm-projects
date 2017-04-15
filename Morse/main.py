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
        self.error_index = []

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

        for char in self.Input:

            if char != ' ':
                try:
                    first_flag = False
                    space_flag = False
                    try:
                        self.output[wordcount] += self.codetable.return_morse(self.Input[char_count], False)
                    except IndexError:
                        self.output.append(self.codetable.return_morse(self.Input[char_count], False))
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

    def output_code(self):
        return self.output, self.error_index
        #for i in range(len(self.output)):
         #    return self.output[i] # kan je return wel in een for loop zetten?

    def returncode(self):
        for i in range(len(self.output)):
            print(self.output[i])

if __name__ == '__main__':
    convertcode = morse()
    convertcode.setinput()
    convertcode.convert()
    convertcode.returncode()



