"""
Basic Pixel Perfect Point Collision in kivy

Overriding the Image's [collide_point] method to use the underlying [core.image.Image]'s
[read_pixel] method and access the alpha information of the colliding pixel.
The [keep_data: True] statement is essential, before assigning (loading) a texture.
A deviation from the [size_hint: None, None] and [size: self.texture_size], along with
the use of [allow_stretch] and other size modifications, could probably be allowed,
by using the [norm_image_size] property, but the scaling and rotation of a ScatterLayout
(as in the current example) works fine as is.
Also note that the image's local [y] coordinate is inverse as far as [read_pixel] is
concerned.
(Could it be the reason why this approach doesn't seem to work with atlases?)

Thanks to niavlys for his 3/14/14 post:
(https://groups.google.com/forum/#!topic/kivy-users/BnjrZT0NkhU)
and to tshirtman for his:
(7/24/14 https://groups.google.com/forum/#!topic/kivy-dev/dpT7yqs_Mq0)

unjuan 2015
"""

from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.utils import platform, get_hex_from_color
from kivy.core.window import Window


Builder.load_string('''
<RootLayout>:
    CustomImage:
        keep_data: True
        size_hint: 1, None
        size: self.image_size # self.texture_size
        pos_hint: {'center_x': .5, 'center_y': .5}
        source: 'VLSI-Circuit-Breaker-2.0-Level_1.png' # 'Asset 1test.png'
        opacity: .3
        
        canvas.before:
            Color:
                rgb: 1, 0, 0
            Rectangle:
                size: self.size
                pos: self.pos
            
                
''')


class CustomImage(Image):
    image_size = ListProperty([0, 0])
    def __init__(self, **kwargs):
        # ################################### un-comment for a python-only version
        # kwargs.setdefault('keep_data', True)
        # kwargs.setdefault('size_hint', (None,None))
        super(CustomImage, self).__init__(**kwargs)
        # self.pos_hint = {'center_x': .5, 'center_y': .5}
        # self.opacity = .3
        #######################################################################
        self.bind(size=self.update_image_size)

    def update_image_size(self, *args):
        try:
            x = self.width
            y = (self.texture_size[1] * x) / self.texture_size[0]
            self.image_size = [x, y]
        except:
            pass


    def collide_point(self, x, y):
        from colorsys import rgb_to_hsv
        # Do not want to upset the read_pixel method, in case of a bound error
        try:
            # color = self._coreimage.read_pixel(x - self.x, self.height - (y - self.y))
            x_ = ((x - self.x) / self.width ) * self.texture_size[0]
            y_ = ((self.height - (y - self.y)) / self.height ) * self.texture_size[1]
            color = self._coreimage.read_pixel(x_, y_)
        except:
            color = 0, 0, 0, 0
            # print('read pixel error')
        hsv = rgb_to_hsv(*color[:-1])
        if hsv[-1] > .22:
            print("Detected border")
        else:
            print('Dark green')
        print('hsv:', hsv, '\n')
        #print("Color in clicked pixel:", [float("%.3f" % x) for x in color[:2]], '\n')
        if color[-1] > 0:
            return True
        return False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 1
        else:
            self.opacity = .3


class RootLayout(ScatterLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        # ################################### un-comment for python-only version
        # cimage = CustomImage()
        # cimage.source = 'wolf.png'
        # cimage.size = cimage.texture.size
        # self.add_widget(cimage)
        ###########################################################################


class CollTestApp(App):
    def build(self):
        if platform != 'android':
            Window.size = (394, 700)
        return RootLayout()


if __name__ == '__main__':
    CollTestApp().run()