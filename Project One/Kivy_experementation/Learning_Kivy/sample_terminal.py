import kivy
kivy.require('1.10.0')

from kivy.uix.gridlayout import GridLayout

from kivymd.theming import ThemeManager

from kivy.app import App


class terminal_baseClass(GridLayout):
    pass


class sample_terminalApp(App):
    theme_cls = ThemeManager()

    def build(self):
        return terminal_baseClass()

if __name__ == '__main__':
    sample_terminalApp().run()