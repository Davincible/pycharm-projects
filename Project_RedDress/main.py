"""
    Made by: David Brouwer
    Author email address: david.brouwer.99@gmail.com
    Author GitHub: https://github.com/Davincible

    Main file of the game.

    Date of first comment: 28th of November, 2017

    This GUI is predicated on the Kivy framework, for installation instructions please see https://kivy.org

    Used KivyMD fork: https://github.com/Davincible/custom_uix
"""

import kivy
kivy.require('1.10.0')

# kivy uix imports
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FallOutTransition
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import FocusBehavior

# kivymd imports
from kivymd.theming import ThemeManager
from kivymd.dialog import MDDialog

# kivy console from other module in package
from kivyconsole import KivyConsole

# other kivy imports
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty, ReferenceListProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.base import Builder
from kivy.app import App
from kivy.config import Config

# other imports
import urllib3
from os.path import join, exists
from os import makedirs
import time

# load the kv file
Builder.load_file('reddress_visuals.kv')

# debugging
if platform == 'win':
    print("DEV mode turned on")
    DEBUG = True
else:
    DEBUG = True


class MainScreenManagerClass(ScreenManager):
    """the main screen manager class"""
    pass


class MainScreenClass(Screen):
    """login screen shown on startup"""

    #  properties for the background texture
    texture_ = Image(source="resources/RedDress_Texture.jpg").texture
    texture_.wrap = 'repeat'
    nx = NumericProperty(0)
    ny = NumericProperty(0)

    line_points_one = ListProperty()
    line_points_two = ListProperty()

    table_value_height = NumericProperty(dp(60))

    unschedule = False
    scheduled = False

    def __init__(self, **kwargs):
        super(MainScreenClass, self).__init__(**kwargs)
        self.bind(size=self.update_texture_size)

    def update_texture_size(self, *args):
        # update the texture coordinates, used for the repetition of the texture
        self.nx = float(self.width) / self.texture_.width
        self.ny = float(self.height) / self.texture_.height

    def set_line_points(self, *args):
        #  get the points (coordinates) for the seperator lines of the table on the dashboard
        left_top = self.ids.left_top
        right_top = self.ids.right_top
        left_bottom = self.ids.left_bottom
        right_bottom = self.ids.right_bottom

        self.line_points_one = [left_top.x, left_top.y, right_top.right, right_top.y]
        self.line_points_two = [left_top.right, left_bottom.y, left_top.right, left_top.top]

    def reveal_package(self):
        """schedule or unschedule the blinking"""
        if not self.scheduled:
            Clock.schedule_interval(self.ping_leds, 2)
            self.scheduled = True
        else:
            self.unschedule = True

    def ping_leds(self, *args):
        """call the blink server to send a request to the ESP12 microprocessor to blink the led ring"""
        if self.unschedule:
            self.unschedule = False
            self.scheduled = False
            return False

        # the provided api key is out of date and no longer used
        api_key = None
        with open('blynk_api_key.txt') as file:
            api_key = file.readline()

        if api_key:
            # on every api key the LED ring will go around once
            url = "http://blynk-cloud.com/{}/update/V1?value=1".format(api_key)
            browser = urllib3.PoolManager()
            request = browser.request('GET', url)

    def goto_login(self):
        """go back to the login screen"""
        App.get_running_app().root.current = 'LoginScreen'


class LoginScreenClass(Screen):
    #  properties for the background texture
    texture_ = Image(source="resources/RedDress_Texture.jpg").texture
    texture_.wrap = 'repeat'
    nx = NumericProperty(0)
    ny = NumericProperty(0)

    #  other properties
    textfield_height = dp(70)
    force_refresh = False

    #  base variables for object reference
    textfield_username = ObjectProperty(None)
    textfield_password = ObjectProperty(None)
    terminal = ObjectProperty(None)
    terminal_dialog = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginScreenClass, self).__init__(**kwargs)
        self.bind(size=self.update_texture_size)
        self.terminal = KivyConsole()

    def update_texture_size(self, *args):
        self.nx = float(self.width) / self.texture_.width
        self.ny = float(self.height) / self.texture_.height

    #  an event handler for when the enter button on the login screen has been pressed
    def _enter_button(self):
        username = self.textfield_username.text.strip().lower()
        password = self.textfield_password.text.strip().lower()

        if username == 'root':
            self.create_terminal_dialog()
        elif username == 'root_':
            self.force_refresh = True
            self.create_terminal_dialog()
        elif ((username == self.terminal.game_username and password == self.terminal.game_password) or (username == 'enter')) \
                and (DEBUG or self.terminal.hacked_account):
            time.sleep(.1)
            App.get_running_app().root.current = 'MainScreen'
            print("Successfully logged in")
        elif username:
            self.textfield_password.show_error(msg="Please enter a valid password")
        else:
            self.textfield_username.show_error()
            print("Username:", self.terminal.game_username, "Password:", self.terminal.game_password)

    #  creates a dialog with a terminal emulator in it, and opens it
    def create_terminal_dialog(self):
        self.textfield_username.reset_textbox()
        if not self.terminal or self.force_refresh:
            self.terminal = KivyConsole()

        if not self.terminal_dialog or self.force_refresh:
            self.terminal_dialog = ModalView(size_hint=(.9, .6), pos_hint={'center_x': .5, 'center_y': .669})
            self.terminal_dialog.add_widget(self.terminal)
            self.terminal.bind(on_exit=self.terminal_dialog.dismiss)
            self.terminal.bind(on_circuitbreaker=self.start_circuitbreaker)
        self.terminal_dialog.open()
        self.terminal.focus = True

    #  dismiss the terminal dialog, and go to the CircuitBreaker game screen
    def start_circuitbreaker(self, *args):
        self.terminal_dialog.dismiss()
        # App.get_running_app().root.transition = RiseInTransition()
        App.get_running_app().root.current = 'VLSI_CircuitBreaker'


class VLSI_CircuitBreakerClass(Screen, FocusBehavior):
    #  properties for the background texture
    texture_ = Image(source="resources/green_code_texture_04.jpg").texture
    texture_.wrap = 'repeat'
    nx = NumericProperty(0)
    ny = NumericProperty(0)

    #  other properties
    button_opacity = NumericProperty(.7)
    side_button_height = NumericProperty(.7)

    #  object reference properties
    base_widget = ObjectProperty(None)  # reference to the base of the circuit breaker game
    loginscreen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(VLSI_CircuitBreakerClass, self).__init__(**kwargs)
        self.bind(size=self.update_texture_size)
        Clock.schedule_once(lambda dt: self.base_widget.bind(on_hacked=self.complete))

    def complete(self, *args):
        source = 'resources/circuit_complete.png'
        texture = Image(source=source)
        height = dp((texture.texture_size[1] * self.width) / texture.texture_size[0])
        complete_popup = ModalView(size_hint=(1, None), height=height, background=source,
                                   background_color=[0, 0, 0, .35], auto_dismiss=False, pos_hint={'center_y': .65})
        complete_popup.open()
        Clock.schedule_once(lambda dt: self.back_home(popup=complete_popup), 7)

    def back_home(self, popup, *args):
        popup.dismiss()
        self.loginscreen.terminal.hacked_circuit = True
        # App.get_running_app().root.transition = FallOutTransition()
        App.get_running_app().root.current = 'LoginScreen'
        App.get_running_app().root.ids.LoginScreen.terminal_dialog.open()

    def update_texture_size(self, *args):
        self.nx = float(self.width) / self.texture_.width
        self.ny = float(self.height) / self.texture_.height

    def on_enter(self, *args):
        self.focus = True
        self.base_widget.on_enter()


class RedDressApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Brown'

    def __init__(self, **kwargs):
        super(RedDressApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
        log_path = join(App.get_running_app().user_data_dir, 'logs')
        if not exists(log_path):
            makedirs(log_path)
        Config.set('kivy', 'log_dir', log_path)

    def on_keyboard(self, window, key, *args):
        #  enter = 13
        #  tab = 9

        # esc on pc, back on android
        if key == 27:
            return True

    def build(self):
        Window.softinput_mode = 'below_target'
        Window.bind(on_keyboard=self.on_keyboard)

        if platform != 'android':
            Window.size = (394 * 1.7, 700 * 1.7)
        return MainScreenManagerClass()

    def on_keyboard(self, window, key, *args):
        home_screens = ['BottomLayout_landscape', 'BottomLayout_portrait']
        #  enter = 13
        #  tab = 9

        # esc on pc, back on android
        if key == 27:  # disable the app quiting on press of the return key
            return True


if __name__ == '__main__':
    RedDressApp().run()