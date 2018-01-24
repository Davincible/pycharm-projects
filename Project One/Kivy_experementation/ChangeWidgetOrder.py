from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.core.window import Window

from kivy.base import Builder

kv_file = """

ScrollView:
    GridLayout:
        id: main_layout
        cols: 1
        height: self.minimum_height
        size_hint_y: None
        canvas.before:
            Color:
                rgba: 1, .5, 0, .3
            Rectangle:
                size: self.size
                pos: self.pos
        
        Label:
            size_hint_y: None
            height: dp(125)
            text: "A"
            id: main_label
            
            canvas.before:
                Color:
                    rgba: 1, 0.5, 0, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
        
        Label:
            size_hint_y: None
            height: dp(125)
            text: "B"
        
        Label:
            size_hint_y: None
            height: dp(125)
            text: "B"
            
        Label:
            size_hint_y: None
            height: dp(125)
            text: "C"
            
        Label:
            size_hint_y: None
            height: dp(125)
            text: "D"

"""


class MainApp(App):
    def build(self):
        window = Builder.load_string(kv_file)
        Window.bind(on_keyboard=self.on_keyboard)

        return window

    def on_keyboard(self, window, key, *args):
        if key == 13:
            print("layout children:", self.root.ids.main_layout.children)
            print("main label:", self.root.ids.main_label)
            print("the index is", self.root.ids.main_layout.children.index(self.root.ids.main_label))
            return True
        elif key == 9:
            widget_id = self.root.ids.main_label
            layout_children = self.root.ids.main_layout.children
            index = layout_children.index(widget_id)
            layout_children.remove(widget_id)
            if index == 0:
                layout_children.insert(len(layout_children), widget_id)
            else:
                layout_children.insert(index - 1, widget_id)
            self.root.ids.main_layout.children = layout_children
            print("should've changed the order")
        else:
            print(key)

if __name__ == '__main__':
    MainApp().run()

