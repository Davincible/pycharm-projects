class code_table():
    def __init__(self):
        self.CODE = {'A': '.-', 'B': '-...', 'C': '-.-.',
                'D': '-..', 'E': '.', 'F': '..-.',
                'G': '--.', 'H': '....', 'I': '..',
                'J': '.---', 'K': '-.-', 'L': '.-..',
                'M': '--', 'N': '-.', 'O': '---',
                'P': '.--.', 'Q': '--.-', 'R': '.-.',
                'S': '...', 'T': '-', 'U': '..-',
                'V': '...-', 'W': '.--', 'X': '-..-',
                'Y': '-.--', 'Z': '--..',

                '0': '-----', '1': '.----', '2': '..---',
                '3': '...--', '4': '....-', '5': '.....',
                '6': '-....', '7': '--...', '8': '---..',
                '9': '----.'
                }

        self.CODE_REVERSED = {value: key for key, value in self.CODE.items()}

    def return_morse(self, letter, extra_space = bool):
        if extra_space == True:
            return self.CODE[letter] + '  '
        else:
            return self.CODE[letter]

    def return_letter(self, morse):
        return self.CODE_REVERSED[morse]
