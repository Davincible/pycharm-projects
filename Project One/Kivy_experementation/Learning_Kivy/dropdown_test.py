import kivy
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.theming import ThemeManager
import kivymd

Builder.load_string("""
#:import Toolbar kivymd.toolbar
#:import uiximage kivy.uix.image
#:import MDLabel kivymd.label
#:import MDSeperator kivymd.card.MDSeparator
#:import MDTextField kivymd.textfields.MDTextField
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDCard kivymd.card.MDCard

<BigOne>:
    thebigone: thebigone
    size_hint_x: None
    width: dp(500)
    MDRaisedButton:
        id: thebigone
        text: 'The big one'
        size_hint: 1, None
        on_release: app.drop.open(self)

<MyDropdown>:
    canvas:
        Color:
            rgb: 1, 0, .3
        Rectangle:
            size: self.size
            pos: self.pos
        
    id: drop
    size_hint_x: None
    width: dp(450)
    on_select: app.get_running_app().root.ids.thebigone.text = args[1]
    auto_width: False
     
    MDRaisedButton:
        size_hint_y: None
        text: 'one'
        height: dp(100)
        on_release: drop.select('item1') 
    MDRaisedButton:
        size_hint_y: None
        text: 'two'
        height: dp(100)
        on_release: drop.select('item2')
    MDRaisedButton:
        text: 'three'
        height: dp(100)
        size_hint_y: None
        on_release: drop.select('item3')
    MDRaisedButton:
        text: 'four'
        height: dp(100)
        size_hint_y: None
        on_release: drop.select('item4')
    
""")

class BigOne(BoxLayout):
    pass


class MyDropdown(DropDown):
    pass


class WindowApp(App):
    theme_cls = ThemeManager()
    #
    def build(self):
        self.drop = MyDropdown()
        return BigOne()

if __name__ == '__main__':
    WindowApp().run()