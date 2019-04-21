from os.path import isfile
import random


class ROTCodec:
    """ Simple ROT bruteforcer to check if a certain string is ROT encoded """
    msg = ''
    output = {}
    dictionary = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def encode(self, cipher=None, msg=''):
        """ Rot encode, if no cipher specified by all 25 ciphers possible """
        self._load_dictionary()
        self._get_input(msg=msg)
        self._rotate(cipher)
        self._validate()
        self._output()

    def _load_dictionary(self, PATH="dictionary.txt"):
        """ Load dictionary file """
        if isfile(PATH):
            with open(PATH, 'r') as file:
                for line in file.readlines():
                    self.dictionary.append(line.strip())
        else:
            print("Dictionary file '{}' not found".format(PATH))

    def _validate(self):
        """ Validate the result against a dictionary file """
        # check every rotted output
        for rot in self.output:
            words = self.output[rot]['output'].split(' ')[2:]

            # get list of 100 words to check
            if len(words) < 100:
                to_check = words
            else:
                to_check = []
                for i in range(1, 100):
                    to_check.append(words[random.randrange(0, len(words) - 1)])

            # validate
            match_count = 0
            for word in to_check:
                if word.upper() in self.dictionary:
                    match_count += 1

            self.output[rot]['match_count'] = match_count

    def _output(self):
        """ Output the result """
        # print the result sorted by match count
        rot_output = [self.output[x] for x in self.output]
        rot_output.sort(key=lambda x: x['match_count'])
        for line in rot_output:
            print("Match count: {}, output: {}".format(line['match_count'], line['output']))

    def _get_input(self, msg=''):
        """ Get user input """
        if msg:
            self.msg = msg.lower()
        else:
            self.msg = input("What message do you want to ROT brute force? ").lower()

    def _rotate(self, cipher=None):
        """ Rotate the characters, aka apply rot cipher(s) """
        # set ciphers to rot
        to_rot = []
        if isinstance(cipher, list):
            to_rot = cipher
        elif isinstance(cipher, int):
            to_rot.append(cipher)
        else:
            to_rot = list(range(1, len(self.alphabet)))

        # perform rot operations
        for count in to_rot:
            rotted = "ROT {}: ".format(count)
            for char in self.msg:
                if char is not ' ':
                    old_index = self.alphabet.index(char)
                    new_index = ((old_index + count) % len(self.alphabet))
                    new_char = self.alphabet[new_index]
                    rotted += new_char
                else:
                    rotted += ' '
            self.output[count] = {'output': rotted}

if __name__ == '__main__':
    ROTCodec().encode()