import kivy
kivy.require('1.10.0')

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

class Screen_OneClass(Screen):
    pass

class Screen_TwoClass(Screen):
    pass

class Screen_AClass(Screen):
    pass

class Screen_BClass(Screen):
    pass

class Screen_CClass(Screen):
    pass

class Screen_MainClass(Screen):
    pass

class ScreenManagerClass(ScreenManager):
    pass

class Learning_ScreenManagerApp(App):
    def build(self):
        return ScreenManagerClass()

if __name__ == '__main__':
    app = Learning_ScreenManagerApp()
    app.run()