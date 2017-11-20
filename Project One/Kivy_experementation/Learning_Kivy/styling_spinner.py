import kivy
from kivy.lang.builder import Builder
Builder.load_string("""
                    #:import Factory kivy.factory.Factory

#:set color_button (0.784, 0.443, 0.216, 1)  # brown
#:set color_button_pressed (0.659, 0.522, 0.431, 1)  # darker brown
#:set color_font   (0.957, 0.890, 0.843, 1)  # off white
 
<MySpinnerOption@SpinnerOption>:
    background_color: color_button if self.state == 'down' else color_button_pressed
    background_down: 'atlas://data/images/defaulttheme/button'
    color: color_font
 
<MyThing>:
    Spinner:
        text: "First thing"
        values: ["First thing", "Second thing", "Third thing"]
        background_color: color_button if self.state == 'normal' else color_button_pressed
        background_down: 'atlas://data/images/defaulttheme/spinner'
        color: color_font
        option_cls: Factory.get("MySpinnerOption")
        size_hint: None, None""")

from kivy.app import App
from kivy.uix.widget import Widget
class MyThing(Widget):
    pass
class windowApp(App):
    def build(self):
        return MyThing()

windowApp().run()