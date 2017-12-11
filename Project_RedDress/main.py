import kivy
kivy.require('1.10.0')

from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FallOutTransition
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import FocusBehavior

from kivymd.theming import ThemeManager
from kivymd.dialog import MDDialog

from kivyconsole import KivyConsole

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty, ReferenceListProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.base import Builder
from kivy.app import App

Builder.load_file('reddress_visuals.kv')
if platform == 'win':
    DEBUG = True
else:
    DEBUG = False


class MainScreenManagerClass(ScreenManager):
    pass


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

    def _enter_button(self):
        username = self.textfield_username.text.strip().lower()
        password = self.textfield_password.text.strip().lower()

        if username == 'root':
            self.create_terminal_dialog()
        elif username == 'root_':
            self.force_refresh = True
            self.create_terminal_dialog()
        elif (username == self.terminal.game_username and password == self.terminal.game_password) \
                and (DEBUG or self.terminal.hacked_account):
            print("Successfully logged in")
        else:
            self.textfield_username.show_error()


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
        height = (texture.texture_size[1] / self.width) * texture.texture_size[0] - 40
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

    def on_keyboard(self, window, key, *args):
        #  enter = 13
        #  tab = 9

        # esc on pc, back on android
        if key == 27:
            return True

    def build(self):
        Window.softinput_mode = 'below_target'

        if platform != 'android':
            Window.size = (394 * 1.7, 700 * 1.7)
        return MainScreenManagerClass()


if __name__ == '__main__':
    RedDressApp().run()