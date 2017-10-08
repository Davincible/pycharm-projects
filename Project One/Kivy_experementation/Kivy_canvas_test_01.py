from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Color

# every single kivy widget(layouts) has a canvas that you can draw in.
class CanvasWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs) # thefuck does this do?

        with self.canvas:
            Color(0, 1, 0, 1)
            Rectangle(pos=(0, 100), size=(300, 100))
            Ellipse(pos=(0, 400), size=(300, 100))
            Line(points=[ 0, 0, 500, 600, 400, 300 ], close=True, width=3)


class main_app(App):
    def build(self):
        return CanvasWidget()

if __name__ == '__main__':
    main_app().run()