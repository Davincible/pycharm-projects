from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty

KV = """
<CircularButton>:
    size_hint: 1, 1
    size: (min(self.width,self.height),min(self.width,self.height))
    
    canvas.before:
        Color:
            rgb: 1, 0, 0

        Rectangle:
            size: self.size
            pos: self.pos
    canvas:
        Color:
            rgba: ((1,1,1,1) if self.state == "normal" else (.5,.5,.5,1))
        Ellipse:
            source: 'C:/Users/David.MIDDENAARDE/Pictures/Textures/football.png'
            pos: self.pos
            size: root.size
"""

Builder.load_string(KV)


class CircularButton(ButtonBehavior, Widget):
    # x = y = NumericProperty(0)
    # size = ReferenceListProperty(x, y)
    #
    # def on_width(self, *args):
    #     x = y = min(self.width, self.height)
    #     self.size = (x, y)

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2


if __name__ == '__main__':
    from kivy.base import runTouchApp


    def callback(*args):
        print("i'm being pressed")


    runTouchApp(CircularButton(on_press=callback))