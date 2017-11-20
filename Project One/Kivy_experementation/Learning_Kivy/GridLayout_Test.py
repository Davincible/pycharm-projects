import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App

class GridLayoutClass(GridLayout):
    pass


class GridLayout_TestApp(App):
    def build(self):
        self.window = GridLayoutClass()
        return self.window

if __name__ == '__main__':
    GridLayout_TestApp().run()