import kivy
kivy.require('1.10.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ListProperty

from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform, get_hex_from_color
import struct

class BaseLayoutClass(FloatLayout):
    pass

class BackgroundLayerClass(Widget):
    pass

class BorderLayerClass(Widget):
    pass

class CustomImageClass(Widget):
    image_size = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(CustomImageClass, self).__init__(**kwargs)
        self.background_ = Image(source='Asset 1test.png').texture
        self.bind(size=self.update_image_size)

    def update_image_size(self, *args):
        x = self.width
        y = (self.background_.size[1] * x) / self.background_.size[0]
        self.image_size = [x, y]

    def on_touch_down(self, touch):
        pos = [touch.pos[0]/self.width*self.background_.size[0], touch.pos[1]/self.height*self.background_.size[1]]
        pixel = self.background_.get_region(*pos, 1, 1)
        raw_pixel = pixel.pixels
        data = struct.unpack('4B', raw_pixel)
        adjusted = [float('%.3f' % (a/255)) for a in data]
        #print('raw pixel data', raw_pixel)
        print('unpacked data', data)
        print('adjusted', adjusted)
        print()
       # print('hex color', get_hex_from_color(adjusted))
        #print('pixel color:', [a / 255 for a in data], '\n')
        return False

class experiment_layer_collide_boundariesApp(App):
    def build(self):
        if platform != 'android':
            Window.size = (394, 700)

        return BaseLayoutClass()

if __name__ == '__main__':
    experiment_layer_collide_boundariesApp().run()
