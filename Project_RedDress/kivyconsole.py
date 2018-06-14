"""
    Made by: David Brouwer
    Author email address: david.brouwer.99@gmail.com
    Author GitHub: https://github.com/Davincible

    A terminal emulator in Kivy. The first half I got from somewhere on the internet
    (ashamed to say I don't know the source anymore), the other half I developed myself.

    Date of first comment: 28th of November, 2017

    This GUI is predicated on the Kivy framework, for installation instructions please see https://kivy.org

    Used KivyMD fork: https://github.com/Davincible/custom_uix
"""

# kivy uix imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

# other kivy imports
from kivy.base import runTouchApp
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import *
from kivy.utils import get_color_from_hex
from kivy.core.audio.audio_sdl2 import SoundSDL2
from kivy.metrics import sp
from kivy.clock import Clock

# other imports
import os
import threading
import sys
from random import randint
from time import sleep
from datetime import datetime
from os.path import join

# the kv file as string
Builder.load_string('''
<KivyConsole>:
    console_input: console_input
    scroll_view: scroll_view
    game_username: console_input.game_username
    game_password: console_input.game_password
    hacked_account: console_input.hacked_account
    ScrollView:
        id: scroll_view
        scroll_y: 0
        ConsoleInput:
            id: console_input
            scroll_view: scroll_view
            shell: root
            size_hint: (1, None)
            #font_name: root.font_name
            font_size: root.font_size
            foreground_color: root.foreground_color
            background_color: root.background_color
            height: max(self.parent.height, self.minimum_height)
            hacked_circuit: root.hacked_circuit
''')


def threaded(fn):
    """decorator to tread a function"""
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class Shell(EventDispatcher):
    # , 'on_stop', 'on_start', 'on_complete', 'on_error'
    __events__ = ('on_output', 'on_complete', 'on_exit', 'on_circuitbreaker')

    process = ObjectProperty(None)
    '''subprocess process
    '''

    @threaded
    def run_command(self, command, consoleinput=None, show_output=True, *args):
        consoleinput.busy = True
        skip_newline = False

        #  code to actually execute the command in the os
        """
        output = ''
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE)
        lines_iterator = iter(self.process.stdout.readline, "")
        for line in lines_iterator:
            line = str(line, 'utf-8')
            output += line
            if line == '':
                break

            if show_output:
                self.dispatch('on_output', line)
        """

        #  1st sqlmap command, to establish connection
        if command == consoleinput.game_commands[0]:
            #  only execude if circuit board has been hacked (see VLSI circuit board breaker game)
            if consoleinput.hacked_circuit:
                consoleinput.sqlmap_connected = True
                for line in consoleinput.sqlmap_output_01:
                    delay = randint(100000, 300000) / 100000
                    sleep(delay)
                    line = line.replace('time', datetime.now().strftime("%H:%M:%S"))
                    self.dispatch('on_output', line)
            else:
                self.dispatch('on_output', "Error: Permission Denied")

        #  2nd sqlmap command, to hack databse
        elif command == consoleinput.game_commands[1]:
            #  only execude if first sqlmap command has been executed before
            if consoleinput.sqlmap_connected:
                consoleinput.hacked_account = True
                for line in consoleinput.sqlmap_output_02:
                    delay = randint(10000, 300000) / 100000
                    sleep(delay)
                    line = line.replace('time', datetime.now().strftime("%H:%M:%S"))
                    self.dispatch('on_output', line)
            else:
                self.dispatch('on_output', "sqlmap error: no connection established")

        #  start VLSI_CircuitBreaker_2.0
        elif command == consoleinput.game_commands[2]:
            self.dispatch('on_circuitbreaker')
            skip_newline = True

        #  command to exit
        elif command == consoleinput.game_commands[3]:
            self.dispatch('on_exit')
            skip_newline = True

        #  play morse code
        elif command == consoleinput.game_commands[4]:
            consoleinput.morse_code.play()
            self.dispatch('on_output', "Playing morse code")

        # entered command not known
        else:
            print("Unknown command has been called")
            error_msg = "Error, unknown command: " + command
            self.dispatch('on_output', error_msg)

        consoleinput.busy = False
        if not skip_newline:
            self.dispatch('on_output', '\n')
        self.dispatch('on_complete')

    @threaded
    def stop(self, *args):
        if self.process:
            self.process.kill()


class ConsoleInput(TextInput):
    '''Displays Output and sends input to Shell. Emits 'on_ready_to_input'
       when it is ready to get input from user.
    '''

    shell = ObjectProperty(None)
    '''Instance of KivyConsole(parent) widget
    '''

    # the commands for the terminal
    game_commands = ["sqlmap -u http://stoomboot.sint/groteboek/admin/index.php?CatID=666 --dbs",
                     "sqlmap -u http://stoomboot.sint/groteboek/admin/index.php?CatID=666 --user-agent --level=3 -GET hoofd_piet",
                     'VLSI_Circuit_Circuit_Breaker_2.0',
                     'exit',
                     'morse']

    sqlmap_output_01_markup = ["[color=4F860E][time] [INFO] testing connection to the target URL[/color]",
                     "[color=4F860E][time] [INFO] testing if the target URL is stable. This can take a couple of seconds[/color]",
                     "[color=4F860E][time] [INFO] target URL is stable[/color]",
                     "[color=4F860E][time] [INFO] testing if GET parameter 'CatID' is dynamic[/color]",
                     "[color=4F860E][time] [INFO] confirming that GET parameter 'CatID' is dynamic[/color]",
                     "[color=4F860E][time] [INFO] GET parameter 'CatID' is dynamic[/color]",
                     "[color=4F860E][time] [INFO] heuristics detected web page charset 'ascii'[/color]",
                     "[color=86CD34][time] [INFO] heuristic (basic) test shows that GET parameter 'CatID' might be injectable (possible DBMS: 'MYSql')[/color]",
                     "[color=4F860E][time] [INFO] testing for SQl injection on GET parameter 'CatID'[/color]",
                     "[color=4F860E][time] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'[/color]",
                     "[color=C09916][time] [WARNING] reflective value(s) found and filtering out[/color]",
                     "[color=86CD34][time] [INFO] GET parameter 'CatID' is 'AND boolean-based blind - WHERE or HAVING clause' injectable[/color]"]

    #  just some bullshit to emulate a real terminal
    sqlmap_output_01 = ["[time] [INFO] testing connection to the target URL",
                        "[time] [INFO] testing if the target URL is stable. This can take a couple of seconds",
                        "[time] [INFO] target URL is stable",
                        "[time] [INFO] testing if GET parameter 'CatID' is dynamic",
                        "[time] [INFO] confirming that GET parameter 'CatID' is dynamic",
                        "[time] [INFO] GET parameter 'CatID' is dynamic",
                        "[time] [INFO] heuristics detected web page charset 'ascii'",
                        "[time] [INFO] heuristic (basic) test shows that GET parameter 'CatID' might be injectable (possible DBMS: 'MYSql')",
                        "[time] [INFO] testing for SQl injection on GET parameter 'CatID'",
                        "[time] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'",
                        "[time] [WARNING] reflective value(s) found and filtering out",
                        "[time] [INFO] GET parameter 'CatID' is 'AND boolean-based blind - WHERE or HAVING clause' injectable"]

    sqlmap_output_02 = ["[time] [INFO] the back-end dbms is MySql",
                        "[time] [INFO] heuristics detected web page charset 'ascii'",
                        "[time] [INFO] the SQL querry returned 1 table",
                        "[time] [INFO] retrieved table: user_data",
                        "[time] [INFO] the SQl querry returned 7 entries",
                        "[time] [INFO] retrieved: name             | {varchar(255)})",
                        "[time] [INFO] retrieved: role             | {varchar(255)}",
                        "[time] [INFO] retrieved: level            | {int(16)}",
                        "[time] [INFO] retrieved: residence        | {varchar(24)}",
                        "[time] [INFO] retrieved: password         | {varchar(1024)}",
                        "[time] [INFO] retrieved: gifts_deployed   | {int(32)}",
                        "[time] [INFO] retrieved: date_birth       | {date}",
                        "",
                        "+---------------------------------------+",
                        "|   name : hoofd_piet",
                        "|   role : manager",
                        "|   level : 8",
                        "|   residence : attic",
                        "|   password : 01pink_water!",
                        "|   gifts_deployed : 7476",
                        "|   date_birth : 10-10-1975",
                        "+---------------------------------------+",
                        "",
                        "[*] closing connection at time"]

    game_username = StringProperty('hoofdpiet')
    game_password = StringProperty("01pink_water!")
    command_history_back = []
    command_history_forward = ['']
    busy = False  # check if the terminal is busy handling command, blocking other user input
    sqlmap_connected = False  # flag to check if user executed first sqlmap command
    hacked_circuit = BooleanProperty(False)  # flag to check if user successfully hacked circuit (VLSI_Circuit_Breaker_2 game)
    hacked_account = BooleanProperty(False)  # flag to track if user executed both sqlmap commands
    scroll_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ConsoleInput, self).__init__(**kwargs)
        self._cursor_pos = 0  # position of the cursor before after prompt
        self.__init_console()
        self.base_position = 0
        self.register_event_type('on_output')
        self.register_event_type('on_complete')
        self.register_event_type('on_replace')
        # self.bind(text=self.scroll)
        sound_file = 'resources/morse.wav'
        sound_path = join(os.getcwd(), sound_file)
        self.morse_code = SoundSDL2(source=sound_path)

    def scroll(self, *args):
        try:
            self.scroll_view.scroll_y = 0
        except AttributeError:
            print("attribute error in scroll view")

    def __init_console(self, *args):
        """Create initial values for the prompt and shows it."""
        self.cur_dir = os.getcwd()
        self._hostname = 'kivy'
        try:
            if hasattr(os, 'uname'):
                self._hostname = os.uname()[1]
            else:
                self._hostname = os.environ.get('COMPUTERNAME', 'kivy')
        except Exception:
            pass
        self._username = os.environ.get('USER', '')
        if not self._username:
            self._username = os.environ.get('USERNAME', 'designer')
        self.focus = True
        self.prompt()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Override of _keyboard_on_key_down."""
        #  prevent text manipulation while running command
        if self.busy:
            return False

        self.validate_cursor_pos()
        Clock.schedule_once(lambda dt: self.validate_cursor_pos())
        text = self.text[self._cursor_pos:].strip()

        if keycode[0] == 13:
            # Enter -> execute the command
            if text:
                self.command_history_back.append(text)
                Clock.schedule_once(lambda dt: self._run_cmd(text))
                # self._run_cmd(text.strip())

            else:
                Clock.schedule_once(self.prompt)

        elif keycode[0] in [8, 127]:
            self.cancel_selection()
            if self.cursor_index() <= self._cursor_pos:
                return True

        elif keycode[0] == 99 and modifiers == ['ctrl']:
            self.shell.stop()

        #  if up key is pressed
        elif keycode[0] == 273:
            try:
                self.text = self.text[:self.base_position] + self.command_history_back[-1]
                if not self.text[-len(self.command_history_back[-1]):] == self.command_history_back[-1]:
                    self.text = self.text[:self.base_position] + self.command_history_back[-1]

                self.command_history_forward.append(self.command_history_back[-1])
                self.command_history_back.pop(-1)
            except IndexError:
                print("Index error in keypresss up handling")
            return True

        #  if down key is pressed
        elif keycode[0] == 274:
            try:
                self.text = self.text[:self.base_position:] + self.command_history_forward[-1]
                self.command_history_back.append(self.command_history_forward[-1])
                self.command_history_forward.pop(-1)
            except IndexError:
                print("Index  error in keypresss up handling")
            return True

        #  if tab key is pressed
        elif keycode[0] == 9:
            """algorithm to predict command, based on matched characters between valid commands and user input, 
            more or less like a linux terminal does when clicked on tab"""
            matches = 0  # track with how many commands the user input matches
            highest_char_match = 0  # track the highest amount of character matches with any valid command
            match = ''  # track the command with the highest char_match count

            for cmd in self.game_commands:
                current_char_match = 0  # track with how many characters the user input and command match
                for letter_index in range(len(text)):
                    if text[letter_index].lower() == cmd[letter_index].lower():
                        current_char_match += 1

                        if current_char_match == highest_char_match:
                            matches += 1
                        elif current_char_match > highest_char_match:
                            match = cmd
                            highest_char_match = current_char_match
                            matches = 1

                        if matches > 1:
                            temp_match = match.lower()
                            for letter_index_2 in range(len(cmd)):
                                try:
                                    if cmd[letter_index_2].lower() == temp_match[letter_index_2]:
                                        match = cmd[:letter_index_2 + 1]
                                except IndexError:
                                    break
                    else:
                        break

            if match:
                self.dispatch('on_replace', match)
            return True

        if self.cursor_index() < self._cursor_pos:
            return False

        return super(ConsoleInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers)

    def _run_cmd(self, cmd, *args):
        _posix = True
        if sys.platform[0] == 'w':
            _posix = False

        # commands = shlex.split(str(cmd), posix=_posix)
        commands = cmd
        self.shell.run_command(commands, consoleinput=self)

    def validate_cursor_pos(self, *args):
        try:
            if self.cursor_index() < self._cursor_pos + 1:
                self.cursor = self.get_cursor_from_index(self._cursor_pos + 1)
        except IndexError:
            print("Error in validate_cursor_pos fucntion")

    def prompt(self, second_call=False, *args):
        """Show the PS1 variable"""
        self.validate_length()
        if second_call:
            try:
                ps1 = "%s@%s: %s  " % (
                    self._username, self._hostname,
                    os.path.basename(str(self.cur_dir)))
                self._cursor_pos = self.cursor_index() + len(ps1)
                self.base_position = self._cursor_pos
                self.text += ps1
            except IndexError:
                print("Error in promt function")
        else:
            Clock.schedule_once(lambda dt: self.prompt(second_call=True))

    def on_replace(self, text, second_call=False):
        if second_call:
            try:
                self.text = self.text[:self._cursor_pos] + text
            except IndexError:
                print("Index error caught in on_replace")
        else:
            Clock.schedule_once(lambda dt: self.dispatch('on_replace', text, second_call=True))

    def on_output(self, text, second_call=None):
        if second_call:
            try:
                if text[:2] == '\n':
                    self.text += text
                else:
                    self.text += '\n' + text
            except IndexError:
                try:
                    print('Index Error caught:', len(self.text))
                except:
                    print("COULDNT PRINT LENGTH-----------")
        else:
            Clock.schedule_once(lambda dt: self.dispatch('on_output', text, second_call=True))
        self.validate_length()

    def validate_length(self):
        """text input becomes slower after a lot of characters, so to clean up:"""
        try:
            if len(self.text) > 5000:
                temp = self.text[self._cursor_pos:]
                self.text = ''
                self.dispatch('on_output', temp)
        except IndexError:
            print("Error in validate function")
            #self.prompt()

    def on_complete(self):
        self.prompt()


class KivyConsole(BoxLayout, Shell):

    console_input = ObjectProperty(None)
    '''Instance of ConsoleInput
       :data:`console_input` is an :class:`~kivy.properties.ObjectProperty`
    '''

    scroll_view = ObjectProperty(None)
    '''Instance of :class:`~kivy.uix.scrollview.ScrollView`
       :data:`scroll_view` is an :class:`~kivy.properties.ObjectProperty`
    '''

    # foreground_color = ListProperty((1, 1, 1, 1))
    foreground_color = get_color_from_hex('00c826')

    '''This defines the color of the text in the console

    :data:`foreground_color` is an :class:`~kivy.properties.ListProperty`,
    Default to '(.5, .5, .5, .93)'
    '''

    background_color = ListProperty((0, 0, 0, 1))
    '''This defines the color of the text in the console

    :data:`foreground_color` is an :class:`~kivy.properties.ListProperty`,
    Default to '(0, 0, 0, 1)'''

    font_name = StringProperty('data/fonts/DroidSansMono.ttf')
    '''Indicates the font Style used in the console

    :data:`font` is a :class:`~kivy.properties.StringProperty`,
    Default to 'DroidSansMono'
    '''

    font_size = NumericProperty(sp(14))
    '''Indicates the size of the font used for the console

    :data:`font_size` is a :class:`~kivy.properties.NumericProperty`,
    Default to '9'
    '''

    hacked_circuit = BooleanProperty(False)
    hacked_account = BooleanProperty(False)
    game_username = StringProperty('')
    game_password = StringProperty('')


    def __init__(self, **kwargs):
        super(KivyConsole, self).__init__(**kwargs)
        self.register_event_type('on_exit')
        # self.shell = Shell()
        # self.run_command = self.shell.run_command
        # self.shell.bind(on_output=self.console_input.on_output)
        # self.shell.bind(on_complete=self.console_input.on_output)

    def on_circuitbreaker(self, *args):
        pass

    def on_exit(self, *args):
        pass

    def on_output(self, output):
        '''Event handler to send output data
        '''
        self.console_input.dispatch('on_output', output)

    def on_complete(self):
        '''Event handler to send output data
        '''
        self.console_input.dispatch('on_complete')

if __name__ == '__main__':
    runTouchApp(KivyConsole())
