from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


# you can only add the button if it isn't there, else you get an has already a parent exception
class MyWidget(BoxLayout):
    pass

class dynamic_buttonApp(App):
    def build(self):
        my_widget = MyWidget()
        return my_widget


if __name__ == '__main__':
    dynamic_buttonApp().run()
