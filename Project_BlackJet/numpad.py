import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.utils import get_color_from_hex

Builder.load_string("""
#:import MDLabel kivymd.label

<MainLayout>:
    NumPad_Round:
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint_x: None
        width: 500
        
<Numpad_Round_Button>:
    size_hint: 1, 1
    size: 100, 100
    
    canvas:
        Color:
            rgba: root.color
        Line:
            width: 2.
            circle:
                (self.center_x, self.center_y, min(self.width, self.height)
                / 2)
        
        Color:
            rgba: root.color[:3] + [.2] if self.pressed else [0, 0, 0, 0]
        Ellipse:
            size: self.size
            pos: self.pos
                
    MDLabel:
        text: root.label_number
        size_hint: None, None
        size: self.texture_size[0], self.texture_size[1]
        font_size: root.height / 2
        # font_style: 'Display2'
        pos_hint: {'center_x': .5, 'center_y': .5}
        color: root.color
                
<NumPad_Round>:
    cols: 1
    spacer: 8
    size_hint_y: None
    height: self.minimum_height
    spacing: dp(12)
    
    BoxLayout:
        spacing: root.width / root.spacer
        height: self.children[0].width
        size_hint_y: None
        
        NumPad_Round_Button:
            label_number: '1'
            on_release: print(self.size)
        
        NumPad_Round_Button:
            label_number: '2'
        
        NumPad_Round_Button:
            label_number: '3'
    
    BoxLayout:
        spacing: root.width / root.spacer
        height: self.children[0].width
        size_hint_y: None
        
        NumPad_Round_Button:
            label_number: '4'
        
        NumPad_Round_Button:
            label_number: '5'
        
        NumPad_Round_Button:
            label_number: '6'
    
    BoxLayout:
        spacing: root.width / root.spacer
        height: self.children[0].width
        size_hint_y: None
        
        NumPad_Round_Button:
            label_number: '7'
        
        NumPad_Round_Button:
            label_number: '8'
        
        NumPad_Round_Button:
            label_number: '9'
    
    
    BoxLayout:
        spacing: root.width / root.spacer
        height: self.children[0].width
        size_hint_y: None
        
        Widget:
        
        NumPad_Round_Button:
            label_number: '0'
        
        Widget:
""")

class NumPad_Round(GridLayout):
    pass

class NumPad_Round_Button(ButtonBehavior, FloatLayout):
    color = ListProperty([.9, .9, .9, .9])
    label_number = StringProperty('3')
    color_hex = StringProperty("")
    pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(NumPad_Round_Button, self).__init__(**kwargs)
        self.register_event_type("on_color_hex")
        self.bind(on_press=self.activate_press, on_release=self.deactivate_press)

    def on_color_hex(self, hex=None):
        if not hex:
            hex = self.color_hex
        self.color = get_color_from_hex(hex)

    def activate_press(self, *args):
        self.pressed = True

    def deactivate_press(self, *args):
        self.pressed = False

if __name__ == '__main__':
    class MainLayout(FloatLayout):
        pass

    class NumPad_App(App):
        def build(self):
            return MainLayout()

    NumPad_App().run()